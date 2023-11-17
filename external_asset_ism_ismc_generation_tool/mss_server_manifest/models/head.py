import xml.etree.ElementTree as ET

from external_asset_ism_ismc_generation_tool.common.base_model import BaseModel


class Head(BaseModel):
    meta: list

    def __init__(self):
        self.meta = []

    def add_meta(self, name: str, content: str):
        self.meta.append({"name": name, "content": content})

    def to_xml(self) -> ET.Element:
        head_element = ET.Element("head")
        for meta_data in self.meta:
            meta_element = ET.Element("meta")
            meta_element.set("name", meta_data["name"])
            meta_element.set("content", meta_data["content"])
            head_element.append(meta_element)
        return head_element
