# Copyright (C) 2021 Intel Corporation
#
# SPDX-License-Identifier: MIT

import os
import json
import uuid
import random
import string
from collections import OrderedDict
import os.path as osp
import logging as log
from datetime import datetime
from itertools import chain

from datumaro.util.image import save_image, ByteImage
from datumaro.components.converter import Converter
from datumaro.components.dataset import ItemStatus
from datumaro.components.extractor import (AnnotationType, DatasetItem, LabelCategories)
from datumaro.util import cast

from .format import PointCloudPath


class PointCloudParser:
    _SUPPORTED_SHAPES = 'cuboid'

    def __init__(self, subset, context):

        self._annotation = subset
        self._object_keys = {}
        self._figure_keys = {}
        self._video_keys = {}
        self._context = context
        self._user = {}
        self._label_objects = []
        self._frames = {}

        key_id_data = {
            "tags": {},
            "objects": {},
            "figures": {},
            "videos": {}
        }
        self._key_id_data = key_id_data

        meta_data = {
            "classes": [],
            "tags": [],
            "projectType": "point_clouds"
        }
        self._meta_data = meta_data

        self._image_json = {
            "name": "",
            "meta": {
                "sensorsData": {
                    "extrinsicMatrix": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "intrinsicMatrix": [0, 0, 0, 0, 0, 0, 0, 0, 0]
                }
            }
        }

        self._frame_data = {}

        # self.generate_user()
        # self.generate_objects()
        self.generate_frames()

    def set_objects_key(self, object_id):

        if object_id in self._object_keys.keys():
            return
        self._object_keys[object_id] = str(uuid.uuid4())
        self._key_id_data["objects"].update({self._object_keys[object_id]: object_id})

    def set_figures_key(self, figure_id):
        if figure_id in self._figure_keys.keys():
            return
        self._figure_keys[figure_id] = str(uuid.uuid4())
        self._key_id_data["figures"].update({self._figure_keys[figure_id]: figure_id})

    def set_videos_key(self, video_id):
        if video_id in self._video_keys.keys():
            return
        self._video_keys[video_id] = str(uuid.uuid4())
        self._key_id_data["videos"].update({self._video_keys[video_id]: video_id})

    def get_object_key(self, object_id):
        return self._object_keys.get(object_id, None)

    def get_figure_key(self, figure_id):
        return self._figure_keys.get(figure_id, None)

    def get_video_key(self, video_id):

        return self._video_keys.get(video_id, None)

    def generate_frames(self):

        classes_info = []

        for data in self._annotation:
            if not self._user:
                self._user["name"] = data.attributes.get("name", "")
                self._user["createdAt"] = str(data.attributes.get("createdAt", datetime.now()))
                self._user["updatedAt"] = str(data.attributes.get("updatedAt", datetime.now()))

            if not self._label_objects:
                for label in data.attributes.get("labels", []):

                    classes = {
                        "id": int(label["label_id"]),
                        "title": label["name"],
                        "color": label["color"],
                        "shape": "cuboid_3d",
                        "geometry_config": {},
                        "hotkey": ""
                    }
                    self.set_objects_key(int(label["label_id"]))

                    label_object = {
                        "key": self.get_object_key(int(label["label_id"])),
                        "classTitle": label["name"],
                        "tags": [],
                        "labelerLogin": self._user["name"],
                        "createdAt": str(self._user["createdAt"]),
                        "updatedAt": str(self._user["updatedAt"])
                    }
                    classes_info.append(classes)
                    self._label_objects.append(label_object)

            frame_data = []
            if data.pcd:
                self._write_item(data, data.id)
                if not self.get_video_key(int(data.attributes['frame'])):
                    self.set_videos_key(int(data.attributes["frame"]))

            for item in data.annotations:
                if item.type == AnnotationType.cuboid:

                    self.set_figures_key(item.id)
                    figures = {
                        "key": self.get_figure_key(item.id),
                        "objectKey": self.get_object_key(int(item.attributes["label_id"])),
                        'geometryType': "cuboid_3d",
                        "geometry": {
                            "position": {
                                "x": item.points[0],
                                "y": item.points[1],
                                "z": item.points[2]
                            },
                            "rotation": {
                                "x": item.points[3],
                                "y": item.points[4],
                                "z": item.points[5]
                            },
                            "dimensions": {
                                "x": item.points[6],
                                "y": item.points[7],
                                "z": item.points[8]
                            }
                        },
                        "labelerLogin": self._user["name"],
                        "createdAt": self._user["createdAt"],
                        "updatedAt": self._user["updatedAt"]
                    }
                    frame_data.append(figures)

                    label_name = self._get_label(item.label).name
                    for attr_name, attr_value in item.attributes.items():
                        if attr_name in self._context._builtin_attrs:
                            continue
                        if isinstance(attr_value, bool):
                            attr_value = 'true' if attr_value else 'false'
                        if self._context._allow_undeclared_attrs or \
                                attr_name in self._get_label_attrs(item.label):
                            continue
                        else:
                            log.warning("Item %s: skipping undeclared "
                                        "attribute '%s' for label '%s' "
                                        "(allow with --allow-undeclared-attrs option)",
                                        item.id, attr_name, label_name)

            if frame_data:
                self._frame_data[int(data.attributes["frame"])] = frame_data

        data = list({v['id']: v for v in classes_info}.values())
        self._meta_data["classes"] = data

    def get_frames(self):
        return self._frames

    def _get_label(self, label_id):
        if label_id is None:
            return ""
        label_cat = self._annotation.categories().get(
            AnnotationType.label, LabelCategories())
        return label_cat.items[label_id]

    def _get_label_attrs(self, label):
        label_cat = self._annotation.categories().get(
            AnnotationType.label, LabelCategories())
        if isinstance(label, int):
            label = label_cat[label]
        return set(chain(label.attributes, label_cat.attributes)) - \
               self._context._builtin_attrs

    def _write_item(self, item, index):
        if not self._context._reindex:
            index = cast(item.attributes.get('frame'), int, index)
        image_info = OrderedDict([("id", str(index)), ])
        if isinstance(item.pcd, str) and osp.isfile(item.pcd):
            path = item.pcd.replace(os.sep, '/')
            filename= path.rsplit("/", maxsplit=1)[-1]
        else:
            filename = self._context._make_pcd_filename(item)
        image_info["name"] = filename
        self._frames.update({index: filename})

        if item.has_pcd:
            if self._context._save_images:
                self._context._image_dir = osp.join(self._context._default_dir, "pointcloud")

                related_dir = osp.join(self._context._default_dir, "related_images")
                related_dir = osp.join(related_dir, f"{filename.rsplit('.', maxsplit=1)[0]}_pcd" )

                self._context._save_pcd(item,
                                          osp.join(self._context._image_dir, filename))

                for rimage in item.related_images:

                    try:
                        name = rimage["name"]
                    except AttributeError:
                        name = "".join(random.choice(string.ascii_lowercase) for i in range(6))
                        name = f"{name}.jpg"

                    path = osp.join(related_dir, name)

                    path = osp.abspath(path)
                    os.makedirs(osp.dirname(path), exist_ok=True)

                    if isinstance(rimage["image"], ByteImage):
                        with open(path, 'wb') as f:
                            f.write(item.get_bytes())
                    else:
                        save_image(path, rimage["image"].data)

                    path = osp.join(related_dir, f"{name}.json")
                    self._image_json["name"] = name
                    with open(path, "w") as f:
                        json.dump(self._image_json, f, indent=4)
        else:
            log.debug("Item '%s' has no image info", item.id)

    def write_key_id_data(self, f):
        json.dump(self._key_id_data, f, indent=4)

    def write_meta_data(self, f):
        json.dump(self._meta_data, f, indent=4)

    def write_frame_data(self, f, key):
        frame = {
            "description": "",
            "key": self.get_video_key(int(key)),
            "tags": [],
            "objects": self._label_objects,
            "figures": {}
        }

        if self._frame_data.get(key):
            frame["figures"] = self._frame_data[key]

        json.dump(frame, f, indent=4)


class PointCloudConverter(Converter):
    DEFAULT_IMAGE_EXT = PointCloudPath.IMAGE_EXT

    @classmethod
    def build_cmdline_parser(cls, **kwargs):
        parser = super().build_cmdline_parser(**kwargs)
        parser.add_argument('--reindex', action='store_true',
            help="Assign new indices to frames (default: %(default)s)")
        parser.add_argument('--allow-undeclared-attrs', action='store_true',
            help="Write annotation attributes even if they are not present in "
                "the input dataset metainfo (default: %(default)s)")
        return parser

    def __init__(self, extractor, save_dir, reindex=False,
            allow_undeclared_attrs=False, **kwargs):
        super().__init__(extractor, save_dir, **kwargs)

        self._reindex = reindex
        self._builtin_attrs = PointCloudPath.BUILTIN_ATTRS
        self._allow_undeclared_attrs = allow_undeclared_attrs

    def apply(self):
        self._default_dir = osp.join(self._save_dir, PointCloudPath.DEFAULT_DIR)
        os.makedirs(self._default_dir, exist_ok=True)
        self._annotation_dir = osp.join(self._default_dir, PointCloudPath.ANNNOTATION_DIR)
        os.makedirs(self._annotation_dir, exist_ok=True)

        for _, subset in self._extractor.subsets().items():
            point_cloud = PointCloudParser(subset, self)

            for file_name in PointCloudPath.WRITE_FILES:

                with open(osp.join(self._save_dir, file_name), "w") as f:
                    if file_name == "key_id_map.json":
                        point_cloud.write_key_id_data(f)
                    elif file_name == "meta.json":
                        point_cloud.write_meta_data(f)

            frame_files = point_cloud.get_frames()
            for key, file_name in frame_files.items():
                with open(osp.join(self._annotation_dir, f"{file_name}.json"), "w") as f:
                    point_cloud.write_frame_data(f, key)

    @classmethod
    def patch(cls, dataset, patch, save_dir, **kwargs):
        for subset in patch.updated_subsets:
            cls.convert(dataset.get_subset(subset), save_dir=save_dir, **kwargs)

        conv = cls(dataset, save_dir=save_dir, **kwargs)
        images_dir = osp.abspath(osp.join(save_dir, PointCloudPath.POINT_CLOUD_DIR))
        for (item_id, subset), status in patch.updated_items.items():
            if status != ItemStatus.removed:
                item = patch.data.get(item_id, subset)
            else:
                item = DatasetItem(item_id, subset=subset)

            if not (status == ItemStatus.removed or not item.has_image):
                continue

            image_path = osp.join(images_dir, conv._make_image_filename(item))
            if osp.isfile(image_path):
                os.unlink(image_path)
