import json
import os
from typing import Optional

from external_asset_ism_ismc_generation_tool.common.logger.i_logger import ILogger
from external_asset_ism_ismc_generation_tool.common.logger.logger import Logger


class Common:
    __logger: ILogger = Logger("Common")

    @classmethod
    def redefine_logger(cls, logger: ILogger):
        cls.__logger = logger

    @staticmethod
    def read_json(json_path):
        with open(os.path.basename(json_path), 'r') as json_f:
            return json.load(json_f)

    @staticmethod
    def is_file_exists(path):
        return os.path.isfile(path)

    @staticmethod
    def sort_attributes_in_xml(root):
        for el in root.iter():
            attrib = el.attrib
            if len(attrib) > 1:
                attributes = sorted(attrib.items())
                attrib.clear()
                attrib.update(attributes)

    @staticmethod
    def merge_dicts(dict_list: list[dict]) -> dict:
        merged_dict: Optional[dict] = None
        for dictionary in dict_list:
            if dictionary is not None:
                merged_dict = dictionary if not merged_dict else {**merged_dict, **dictionary}
        if merged_dict:
            return {key: value for key, value in merged_dict.items() if value is not None}
        else:
            return {}
