import xml.etree.ElementTree as ET
from typing import Optional

from external_asset_ism_ismc_generation_tool.common.base_model import BaseModel


class TextStream(BaseModel):
    src: str
    system_bitrate: Optional[str]
    system_language: Optional[str]
    params: list

    def __init__(self, src: str, system_bitrate: Optional[str] = None, system_language: Optional[str] = None, params: Optional[list] = None):
        self.src = src
        self.system_bitrate = system_bitrate
        self.system_language = system_language
        self.params = params or []

    def add_param(self, name: str, value: str, value_type: str):
        self.params.append({"name": name, "value": value, "valuetype": value_type})

    def to_xml(self) -> ET.Element:
        textstream_element = ET.Element("textstream")
        textstream_element.set("src", self.src)
        if self.system_bitrate:
            textstream_element.set("systemBitrate", str(self.system_bitrate))
        if self.system_language:
            textstream_element.set("systemLanguage", self.system_language)
        for param_data in self.params:
            param_element = ET.Element("param")
            param_element.set("name", param_data["name"])
            param_element.set("value", param_data["value"])
            param_element.set("valuetype", param_data["valuetype"])
            textstream_element.append(param_element)

        return textstream_element
