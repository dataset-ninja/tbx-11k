As a serious infectious disease, tuberculosis (TB) is one of the major threats to human health worldwide, leading to millions of death every year. Although early diagnosis and treatment can greatly improve the chances of survival, it remains a major challenge, especially in developing countries. Computer-aided tuberculosis diagnosis (CTD) is a promising choice for TB diagnosis due to the great successes of deep learning. However, when it comes to TB diagnosis, the lack of training data has hampered the progress of CTD. To solve this problem, authors establish a large-scale TB dataset, namely Tuberculosis X-ray (**TBX11K**) dataset. This dataset contains 11200 X-ray images with corresponding bounding box annotations for TB areas, while the existing largest public TB dataset only has 662 X-ray images with corresponding image-level annotations. The proposed dataset enables the training of sophisticated detectors for high-quality CTD. Authors reform the existing object detectors to adapt them to simultaneous image classification and TB area detection. These reformed detectors are trained and evaluated on the proposed **TBX11K** dataset and served as the baselines for future research.

This dataset contains 11200(11700) X-ray images with corresponding bounding box annotations for tuberculosis (TB) areas. All images are with a size of 512x512. There are five main categories in this dataset, i.e., ***healthy***, ***sick_but_non-tb***, ***active_tb***, ***latent_tb***, and ***uncertain_tb***. Also dataset includes ***active_tb&latent_tb*** categorie. Authors split this dataset into ***train***, ***val***, and ***test*** sets, consisting of 6600, 1800, and 2800(3302) X-ray images, respectively.

![Dataset categories](https://i.ibb.co/m4tKLQR/Screenshot-from-2020-08-03-22-31-41.webp)

***active_tb&latent_tb*** refers to X-rays that contain active and latent TB simultaneously. ***active_tb*** and ***latent_tb*** refers to X-rays that only contain active TB or latent TB, respectively.
Labels for ***active_tb***:
- *ActiveTuberculosis*
- *PulmonaryTuberculosis*
***latent_tb***:
- *ObsoletePulmonaryTuberculosis*
 ***uncertain_tb*** refers to TB X-rays whose TB types cannot be recognized under today’s medical conditions. Uncertain TB X-rays are all put into the test set. 

![Distribution of the areas](https://i.ibb.co/JCFCK77/Screenshot-from-2020-08-04-09-57-05.webp)

This is the distribution of the areas of TB bounding boxes. The left and right values of each bin define its corresponding area range, and the height of each bin denotes the number of TB bounding boxes with an area within this range. Note that X-rays are in the resolution of about 3000 × 3000. However, the original 3000 × 3000 images will lead to a storage size of over 100GB, which is too large to deliver. On the other hand, authors found that the resolution of 512 × 512 is enough to train deep models for TB detection and classification. In addition, it is almost impossible to directly use the 3000 × 3000 X-ray images for TB detection due to the limited receptive fields of the existing CNNs. Therefore, authors decide to only release the X-rays with the resolution of 512 × 512. For a fair comparison, they recommend all researchers to use this resolution for their experiments.

Here are the answers from the dataset's authors to questions about how the GT labels were created:

- Are latent TB cases biologically confirmed? (by IFNg testing or tuberculin skin testing)

``` apa
Yes, they are. Both active and latent TB cases are biologically confirmed using the hospitals’ accurate clinical diagnosis technology, of course, in the image level.
```

- If the cases are biologically positive for active TB, but does has CXRs regions suspicious for latent TB only, are they labeled as latent TB or active TB?

``` apa
As clarified in section 3.1.3, the annotation is conducted under a double-check rule: “Specifically, each TB X-ray is first labeled by a radiologist who has 5-10 years of experience in TB diagnosis. Then, his box annotations are further checked by another radiologist who has >10 years of experience in TB diagnosis. They not only label bounding boxes for TB areas but also recognize the TB type (active or latent TB) for each box. The labeled TB types are double-checked to make sure that they are consistent with the image-level labels produced by the golden standard. If a mismatch happens, this X-ray will be put into the unlabeled data for re-annotation, and the annotators do not know which X-ray was labeled wrong before. If an X-ray is incorrectly labeled twice, we will tell the annotators the gold standard of this X-ray and ask them to discuss how to re-annotate it.” Therefore, the final TB type must be consistent with the golden standard.
``` 

- If the cases are biologically positive for active TB, but does not contain CXRs regions that are not suspicious for active TB, how are they labeled?

``` apa
The answer is similar to that of the above (2). The image-level labels are confirmed using the hospitals’ accurate clinical diagnosis technology and thus reliable. In our annotation process, our experienced radiologists did not happen to the situation that you said, after discussion, the annotation still cannot be consistent with the gold standard.
```

- How can the cases be both active TB and latent TB?

``` apa
Of course, one TB region is either active TB or latent TB. However, note that an X-ray would contain both active TB and latent TB regions. In our dataset, each TB box only has one label of being active or latent, but a TB X-ray would have both active TB and latent TB labels.
``` 

![Comparison with Other TB Datasets](https://i.ibb.co/dBXbCRW/Screenshot-from-2020-08-03-22-28-18.webp)

The proposed **TBX11K** dataset is much larger, better annotated, and more realistic than existing TB datasets, enabling the training of deep CNNs. First, unlike previous datasets [1, 2] that only contain several tens/hundreds of X-ray images, **TBX11K** has 11,200 images that are about 17× larger than the existing largest dataset, i.e., Shenzhen dataset [1], so that **TBX11K** makes it possible to train very deep CNNs. Second, instead of only having image-level annotations as previous datasets, TBX11K annotates TB areas using bounding boxes, so that the future CTD methods can not only recognize the manifestations of TB but also detect the TB areas to help radiologists for the definitive diagnosis. Third, TBX11K includes four categories of ***healthy***, ***active_tb***, ***latent_tb***, and ***sick_but_non-tb***, rather than the binary classification for TB or not in previous datasets, so that future CTD systems can adapt to more complex real-world scenarios and provide people with more detailed disease analyses.

The ground truth of the ***test*** set will not be released, because it is an online competition for computer-aided tuberculosis diagnosis. To promote the development of this field, we suggest you use the ***train*** set for training and the ***val*** set for validation when tuning your model. When you submit your results of the testing set to author's server, they suggest you training your model on the ***train*** + ***val*** set and testing on the ***test*** set.
