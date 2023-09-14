import os
from urllib.parse import unquote, urlparse

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from pycocotools.coco import COCO
from supervisely.io.fs import get_file_name, get_file_size
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(desc=f"Downloading '{file_name_with_ext}' to buffer...", total=fsize) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###

    dataset_path = "TBX11K"
    img_path = os.path.join(dataset_path, "imgs")
    batch_size = 50

    inst_test = os.path.join("TBX11K", "annotations", "json", "all_test.json")
    inst_train = os.path.join("TBX11K", "annotations", "json", "TBX11K_train.json")
    inst_val = os.path.join("TBX11K", "annotations", "json", "TBX11K_val.json")

    instances = {"test": inst_test, "train": inst_train, "val": inst_val}
    # instances = { "train": inst_train, "val": inst_val}

    tag_names = [
        "healthy",
        "sick_but_non-tb",
        "active_tb",
        "latent_tb",
        "active&latent_tb",
        "uncertain_tb",
    ]
    """
    more about:

    ***healthy***
    if "health" in img_path
    ***sick_but_non-tb***
    if "sick" in img_path
    ***active_tb***
    if label_name != "ObsoletePulmonaryTuberculosis"
    ***latent_tb***
    if label_name == "ObsoletePulmonaryTuberculosis"
    ***active&latent_tb***
    if "ObsoletePulmonaryTuberculosis" in labels and "PulmonaryTuberculosis" or "ActiveTuberculosis" in labels
    ***uncertain_tb***
    no data for test. Check README of orginal dataset.
    """

    instance_coco = COCO(inst_train)
    categories = instance_coco.cats

    def create_ann(image_path, img_dict):
        image_id = img_dict[image_path]
        labels = []
        tag_value = None
        img_height = images[image_id]["height"]
        img_wight = images[image_id]["width"]
        image_name = os.path.basename(image_path)
        if "s" in image_name:
            tag_value = "sick_but_non-tb"
        elif "h" in image_name:
            tag_value = "healthy"
        for label in annotations[image_id]:
            bbox = label["bbox"]
            cat_id = label["category_id"]
            label_name = categories[cat_id]["name"]
            if label_name == "ObsoletePulmonaryTuberculosis":
                tag_value = "latent_tb"
            else:
                tag_value = "active_tb"
            left, top, right, bottom = (
                bbox[0],
                bbox[1],
                bbox[2] + bbox[0],
                bbox[3] + bbox[1],
            )
            geometry = sly.Rectangle(top, left, bottom, right)
            obj_class = meta.get_obj_class(label_name)
            curr_label = sly.Label(geometry, obj_class)
            labels.append(curr_label)
        if len(labels) > 1:
            for label in labels:
                if (
                    label.obj_class.name == "ObsoletePulmonaryTuberculosis"
                    and tag_value == "active_tb"
                ):
                    tag_value = "active&latent_tb"
                elif (
                    label.obj_class.name != "ObsoletePulmonaryTuberculosis"
                    and tag_value == "latent_tb"
                ):
                    tag_value = "active&latent_tb"
        tags = [sly.Tag(tag_meta) for tag_meta in tag_metas if tag_meta.name == tag_value]
        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    obj_classes = [sly.ObjClass(categories[cat]["name"], sly.Rectangle) for cat in categories]

    tag_metas = [sly.TagMeta(name, sly.TagValueType.NONE) for name in tag_names]

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=obj_classes, tag_metas=tag_metas)
    api.project.update_meta(project.id, meta.to_json())

    dataset_test = api.dataset.create(project.id, "test", change_name_if_conflict=True)
    dataset_val = api.dataset.create(project.id, "val", change_name_if_conflict=True)
    dataset_train = api.dataset.create(project.id, "train", change_name_if_conflict=True)

    progress = sly.Progress("Create dataset {}".format("ds0"), 10000)

    def norm_path(path):
        new_path = ""
        path = path.split("/")
        for el in path:
            new_path = os.path.join(new_path, el)
        return os.path.join(img_path, new_path)

    for inst in instances:
        if inst == "val":
            dataset = dataset_val
        elif inst == "train":
            dataset = dataset_train
        else:
            dataset = dataset_test
        instance_coco = COCO(instances[inst])
        categories = instance_coco.cats
        images = instance_coco.imgs
        indexes = list(images)
        annotations = instance_coco.imgToAnns
        for index_batch in sly.batched(indexes, batch_size=batch_size):
            img_paths = [norm_path(images[i]["file_name"]) for i in index_batch]
            img_keys = [images[i]["id"] for i in index_batch]
            img_names_batch = [os.path.basename(img_path) for img_path in img_paths]
            img_dict = {img[0]: img[1] for img in zip(img_paths, img_keys)}
            img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_paths)
            img_ids = [im_info.id for im_info in img_infos]
            anns_batch = [create_ann(image_path, img_dict) for image_path in img_paths]
            api.annotation.upload_anns(img_ids, anns_batch)
            progress.iters_done_report(len(img_names_batch))
