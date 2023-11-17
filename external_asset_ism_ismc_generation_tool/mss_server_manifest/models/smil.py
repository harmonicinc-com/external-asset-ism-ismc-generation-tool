import xml.etree.ElementTree as ET
from typing import Optional

from external_asset_ism_ismc_generation_tool.common.base_model import BaseModel
from external_asset_ism_ismc_generation_tool.mss_server_manifest.models.body import Body
from external_asset_ism_ismc_generation_tool.mss_server_manifest.models.head import Head


class Smil(BaseModel):
    xmlns: str
    head: Optional[Head]
    body: Optional[Body]

    def __init__(self, xmlns: str = "http://www.w3.org/2001/SMIL20/Language"):
        self.xmlns = xmlns
        self.head = None
        self.body = None

    def to_xml(self) -> ET.Element:
        smil_element = ET.Element("smil")
        smil_element.set("xmlns", self.xmlns)
        if self.head:
            smil_element.append(self.head.to_xml())
        if self.body:
            smil_element.append(self.body.to_xml())

        return smil_element
