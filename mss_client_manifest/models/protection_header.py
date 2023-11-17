import xml.etree.ElementTree as ET

from external_asset_ism_ismc_generation_tool.common.base_model import BaseModel


class ProtectionHeader(BaseModel):
    system_id: str

    def __init__(self, system_id: str):
        self.system_id = system_id

    def to_xml(self) -> ET.Element:
        protection = ET.Element("ProtectionHeader")
        protection.set("SystemID", self.system_id)

        return protection
