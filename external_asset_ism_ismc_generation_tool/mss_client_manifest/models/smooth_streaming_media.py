import xml.etree.ElementTree as ET
from typing import Optional

from external_asset_ism_ismc_generation_tool.common.base_model import BaseModel


class SmoothStreamingMedia(BaseModel):
    major_version: str
    minor_version: str
    duration: str
    time_scale: Optional[str]
    is_live: Optional[str]
    lookahead_count: Optional[str]
    dvr_window_length: Optional[str]
    stream_indexes: list
    protections: list

    def __init__(self, major_version: str = '2',
                 minor_version: str = '0',
                 duration: str = '0',
                 time_scale: Optional[str] = '10000000',  # Recommended value - maps to increments of 100ns
                 is_live: Optional[str] = None,
                 lookahead_count: Optional[str] = None,
                 dvr_window_length: Optional[str] = None):
        self.major_version = major_version
        self.minor_version = minor_version
        self.duration = duration
        self.time_scale = time_scale
        self.is_live = is_live
        self.lookahead_count = lookahead_count
        self.dvr_window_length = dvr_window_length
        self.stream_indexes = []
        self.protections = []

    def add_stream_index(self, stream_index):
        self.stream_indexes.append(stream_index)

    def add_protection(self, protection):
        self.protections.append(protection)

    def to_xml(self) -> ET.Element:
        smooth_streaming_media = ET.Element("SmoothStreamingMedia")
        smooth_streaming_media.set("MajorVersion", str(self.major_version))
        smooth_streaming_media.set("MinorVersion", str(self.minor_version))
        if self.time_scale:
            smooth_streaming_media.set("TimeScale", str(self.time_scale))
        smooth_streaming_media.set("Duration", str(self.duration))
        if self.is_live:
            smooth_streaming_media.set("IsLive", str(self.is_live))
        if self.lookahead_count:
            smooth_streaming_media.set("LookaheadCount", str(self.lookahead_count))
        if self.dvr_window_length:
            smooth_streaming_media.set("DVRWindowLength", str(self.dvr_window_length))

        for protection in self.protections:
            if protection:
                smooth_streaming_media.append(protection.to_xml())

        for stream_index in self.stream_indexes:
            if stream_index:
                smooth_streaming_media.append(stream_index.to_xml())

        return smooth_streaming_media
