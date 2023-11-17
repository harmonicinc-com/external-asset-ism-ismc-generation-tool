import decimal
import xml.etree.ElementTree as ET
from typing import Optional

from external_asset_ism_ismc_generation_tool.common.base_model import BaseModel


class ChunkData(BaseModel):
    time_start: Optional[str]
    number: Optional[str]
    duration: Optional[decimal.Decimal]
    r: Optional[str]

    def __init__(self, time_start: Optional[str] = None, number: Optional[str] = None, duration: Optional[decimal.Decimal] = None, r: Optional[str] = None):
        self.time_start = time_start
        self.number = number
        self.duration = duration
        self.r = r

    def to_xml(self) -> ET.Element:
        chunk = ET.Element("c")
        if self.time_start:
            chunk.set("t", self.time_start)
        if self.number:
            chunk.set("n", self.number)
        if self.duration:
            chunk.set("d", str(round(self.duration)))
        if self.r:
            chunk.set("r", self.r)
        return chunk
