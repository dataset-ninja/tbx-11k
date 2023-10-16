Dataset **TBX11K** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/G/r/V0/hM2NS3XrP3qUr0sf1qztduBwHUNf7kumN4T1Tb2TIFn9929hyUyEAvLW7GJK2ZsTMnh2vmyRw5Gx986HnUYu7MUGXi43MQX8zPCa4IVHQFNVo5wTzQd5zxsUdbwH.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='TBX11K', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

