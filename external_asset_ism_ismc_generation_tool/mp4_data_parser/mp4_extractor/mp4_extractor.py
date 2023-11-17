from typing import Optional

from pymp4.parser import MP4, Box, Container

from external_asset_ism_ismc_generation_tool.common.logger.i_logger import ILogger
from external_asset_ism_ismc_generation_tool.common.logger.logger import Logger


class MP4Extractor:
    __logger: ILogger = Logger("MP4Extractor")

    @classmethod
    def redefine_logger(cls, logger: ILogger):
        cls.__logger = logger

    @staticmethod
    def extract_mp4_boxes(segment_data) -> Optional[list]:
        mp4_boxes: list = MP4.parse(segment_data)
        if not mp4_boxes:
            MP4Extractor.__logger.error(f'Error occurs during mp4 boxes extraction. Segment data: {segment_data}')
            return None

        if len(mp4_boxes) == 0:
            MP4Extractor.__logger.error("No mp4 boxes found")
            return None
        return mp4_boxes

    @staticmethod
    def get_box_type(box: Box) -> str:
        if hasattr(box, "type"):
            return box.type.decode()

        if hasattr(box, "format"):
            return box.format.decode()

        return ""

    @staticmethod
    def get_box_extended_type(box: Box) -> str:
        if MP4Extractor.get_box_type(box) != "uuid":
            return ""

        if hasattr(box, "extended_type"):
            return str(box.extended_type)

        return ""

    @staticmethod
    def get_mp4_sub_box(box: Box, box_name: str) -> Optional[Container]:
        if hasattr(box, "children"):
            sub_box = MP4Extractor.get_mp4_box(box.children, box_name)
            if sub_box:
                return sub_box

        if hasattr(box, "entries"):
            sub_box = MP4Extractor.get_mp4_box(box.entries, box_name)
            if sub_box:
                return sub_box

        return None

    @staticmethod
    def get_mp4_box(box_list: list, box_name: str) -> Optional[Container]:
        if box_list is None:
            return None

        for sub_box in box_list:
            if len(box_name) == 4:
                if MP4Extractor.get_box_type(sub_box) == box_name:
                    return sub_box

            if MP4Extractor.get_box_extended_type(sub_box) == box_name:
                return sub_box

        return None

    @staticmethod
    def get_all_mp4_boxes(box_list: list, box_name: str) -> Optional[list]:
        if box_list is None:
            return None

        return [sub_box for sub_box in box_list if MP4Extractor.get_box_type(sub_box) == box_name]

    @staticmethod
    def get_all_mp4_sub_boxes(box: Box, box_name: str) -> list:
        all_extracted = list()
        if hasattr(box, "children"):
            extracted = MP4Extractor.get_all_mp4_boxes(box.children, box_name)
            if extracted and type(extracted) is list:
                all_extracted.extend(extracted)

        if hasattr(box, "entries"):
            extracted = MP4Extractor.get_all_mp4_boxes(box.entries, box_name)
            if extracted and type(extracted) is list:
                all_extracted.extend(extracted)

        return all_extracted
