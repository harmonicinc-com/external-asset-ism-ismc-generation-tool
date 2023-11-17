import xml.etree.ElementTree as ET
from typing import Optional

from external_asset_ism_ismc_generation_tool.common.base_model import BaseModel


class Video(BaseModel):
    src: str
    system_bitrate: str
    params: list

    def __init__(self, src: str, system_bitrate: str, params: Optional[list] = None):
        self.src = src
        self.system_bitrate = system_bitrate
        self.params = params or []

    def add_param(self, name: str, value: str, value_type: str):
        self.params.append({"name": name, "value": value, "valuetype": value_type})

    def to_xml(self) -> ET.Element:
        video_element = ET.Element("video")
        video_element.set("src", self.src)
        video_element.set("systemBitrate", str(self.system_bitrate))
        for param_data in self.params:
            param_element = ET.Element("param")
            param_element.set("name", param_data["name"])
            param_element.set("value", param_data["value"])
            param_element.set("valuetype", param_data["valuetype"])
            video_element.append(param_element)

        return video_element
