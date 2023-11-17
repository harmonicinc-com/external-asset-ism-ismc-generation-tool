import xml.etree.ElementTree as ET

from external_asset_ism_ismc_generation_tool.common.base_model import BaseModel

from external_asset_ism_ismc_generation_tool.mss_client_manifest.models.protection_header import ProtectionHeader


class Protection(BaseModel):
    protection_header: ProtectionHeader

    def __init__(self, protection_header: ProtectionHeader):
        self.protection_header = protection_header

    def to_xml(self) -> ET.Element:
        protection = ET.Element("Protection")
        protection.set("ProtectionHeader", self.protection_header.to_xml)

        return protection
