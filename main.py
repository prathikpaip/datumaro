import datetime
from PIL import Image

import numpy as np
from datumaro.components.extractor import (DatasetItem,
                                           Label, LabelCategories, AnnotationType, Cuboid3D,)
from datumaro.components.dataset import Dataset
import datumaro.components.extractor as datumaro

# import io
dataset = Dataset(categories={
    AnnotationType.label: LabelCategories.from_iterable(['car', 'bus'])
})

# dataset.put( DatasetItem(id="frame.pcd", annotations=[Cuboid(id=206, attributes={"occuluded": 0, "label_id": 0},
# group=0, points=[320.86325216401275, 979.1818473457872, 1.0426186731279325, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0,
# 0.0, 0.0, 0.0, 0.0, 0.0], label=0, z_order=0), Cuboid(id=207, attributes={"occuluded": 0, "label_id": 1}, group=0,
# points=[318.1927645999064, 974.65586694395, 1.297017197169112, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0,
# 0.0, 0.0, 0.0], label=1, z_order=0)],
#
#                         path=[],
#                         image=None,
#                         pcd=r"C:\Users\Anil HP LGHIVE2104\PycharmProjects\datumaro_latest\tests\assets\pointcloud_dataset\ds0\pointcloud\frame.pcd",
#                         related_images=[], attributes={'frame': 20, "name": "Anil", "createdAt": "", "updatedAt": "",
#                                                        "labels": [{"label_id": 0, "name": "car", "color": "#fa3253"},
#                                                                   {"label_id": 1, "name": "bus",
#                                                                    "color": "#83e070"}]}),
#       )

dataset.put(DatasetItem(id='frame_000000',
                        annotations=[Cuboid3D(id=206,
                                            attributes={"occuluded": 0, "label_id":33},
                                            group=0,
                                            points=[320.86325216401275, 979.1818473457872, 1.0426186731279325, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                            label=0,
                                            z_order=0),
                                     Cuboid3D(id=207,
                                            attributes={"occuluded": 0, "label_id": 34},
                                            group=0,
                                            points=[318.1927645999064, 974.65586694395, 1.297017197169112, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                            label=1,
                                            z_order=0)],
                        subset='key_id_map', path=[],
                        image=None, pcd=r"C:\Users\Anil HP LGHIVE2104\PycharmProjects\datumaro_m6_final\tests\assets\pointcloud_dataset\ds0\pointcloud\frame.pcd",
                        related_images=[], attributes={'frame': 0, "name": "Anil", "createdAt": "", "updatedAt": "",
                                                       "labels":[{"label_id": 33, "name": "car", "color": "#fa3253"},
                                                                 {"label_id": 34, "name": "bus", "color": "#83e070"}]})

            )
#
# dataset.put(DatasetItem(id='frame_000001',
#                         annotations=[Cuboid3D(id=208,
#                                             attributes={"occuluded": 0, "label_id": 34},
#                                             group=0,
#                                             points=[23.0462513639241, 8.753051951758222, -0.7804656836492239, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#                                             label=1,
#                                             z_order=0)],
#                         subset='key_id_map', path=[],
#                         image=None,
#                         pcd=r"C:\Users\Anil HP LGHIVE2104\PycharmProjects\datumaro_m6_final\tests\assets\pointcloud_dataset\ds0\pointcloud\kitti_0000000001.pcd",
#                         related_images=[{"name": "000000000.png", "save_path":None, "path":r"C:\Users\Anil HP LGHIVE2104\PycharmProjects\datumaro_m6_final\tests\assets\pointcloud_dataset\ds0\related_images\kitti_0000000001_pcd\0000000000.png"}],
#                         attributes={'frame': 1})
# )


# velodyne points
#

# image1 = Image.open()
# dataset.put(DatasetItem(id='frame_000000',
#             annotations=[Cuboid3D(id=0,
#                                 attributes={'occluded': 0},
#                                 group=0,
#                                 points=[-3.6271575019618414, 7.954996769991751, -1.0343550199580118, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#                                 label=0,
#                                 z_order=0),
#                          Cuboid3D(id=0,
#                                 attributes={'occluded': 0},
#                                 group=0,
#                                 points=[23.0169506240644, 8.343682404650442, -0.7699940133040206, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#                                 label=1,
#                                 z_order=0)],
#             subset='tracklets',
#             path=[],
#             image=None,
#             pcd=r"C:\Users\Anil HP LGHIVE2104\PycharmProjects\datumaro_latest\tests\assets\velodynepoints_dataset\velodyne_points\data\0000000000.bin",
#             related_images=[{"name": "0000000000.png", "save_path": "IMAGE_00", "path":r"C:\Users\Anil HP LGHIVE2104\PycharmProjects\datumaro_latest\tests\assets\velodynepoints_dataset\IMAGE_00\data\0000000000.png"},
#                             ],
#             attributes={'frame': 0}),
#             )
#
# dataset.put(DatasetItem(id='frame_000001',
#                         annotations=[Cuboid3D(id=0,
#                                             attributes={'occluded': 0},
#                                             group=0,
#                                             points=[0.39720775117329943, 7.286424562074529, -0.8997166481217596, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], label=1, z_order=0)],
#                         subset='tracklets',
#                         path=[],
#                         image=None,
#                         pcd=r"C:\Users\Anil HP LGHIVE2104\PycharmProjects\datumaro_latest\tests\assets\velodynepoints_dataset\velodyne_points\data\0000000001.bin",
#                         related_images=[{"name": "0000000001.png", "save_path": "IMAGE_00", "path":r"C:\Users\Anil HP LGHIVE2104\PycharmProjects\datumaro_latest\tests\assets\velodynepoints_dataset\IMAGE_00\data\0000000001.png"},
#                             ],
#                         attributes={'frame': 1}))
#
# dataset.put(DatasetItem(id='frame_000002',
#                         annotations=[Cuboid3D(id=0,
#                                             attributes={'occluded': 0},
#                                             group=0,
#                                             points=[13.54034048060633, -9.410120134481405, 0.24972983624747647, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], label=0, z_order=0)],
#                         subset='tracklets',
#                         path=[],
#                         image=None,
#                         pcd=r"C:\Users\Anil HP LGHIVE2104\PycharmProjects\datumaro_latest\tests\assets\velodynepoints_dataset\velodyne_points\data\0000000002.bin",
#                         related_images=[{"name": "0000000002.png", "save_path": "IMAGE_00",
#                                          "path": r"C:\Users\Anil HP LGHIVE2104\PycharmProjects\datumaro_latest\tests\assets\velodynepoints_dataset\IMAGE_00\data\0000000002.png"},
#                                         ],
#                         attributes={'frame': 2}
#                         )
# )


# dataset.put(DatasetItem(id=2, annotations=[
#   Label(id=0, label=1, name="car", color="#ffffff"),Label(id=1, label=0, name="bus", color="#fff000")]
# ))

dataset.export('test_dataset', 'point_cloud', save_images=True)


# from datumaro.components.dataset import Datasetq
#
# dataset = Dataset.import_from(r'C:\Users\Anil HP LGHIVE2104\PycharmProjects\datumaro\tests\assets\cvat_dataset\for_images', 'cvat')
#
# for data in dataset:
#     print(f"{data=}")

# dataset = Dataset.import_from(r"C:\Users\Anil HP LGHIVE2104\PycharmProjects\datumaro_latest\test_dataset", "point_cloud")
# dataset = Dataset.import_from(r'C:\Users\Anil HP LGHIVE2104\PycharmProjects\datumaro_latest\tests\assets\velodynepoints_dataset', 'velodyne_points')
#
# for data in dataset:
#     print(f"$$$$$$$$$$ -- - > {data=}")
