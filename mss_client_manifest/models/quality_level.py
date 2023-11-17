import xml.etree.ElementTree as ET
from typing import Optional

from external_asset_ism_ismc_generation_tool.common.base_model import BaseModel
from external_asset_ism_ismc_generation_tool.common.common import Common


class QualityLevel(BaseModel):
    index: str
    bitrate: str
    buffer_time: Optional[str]
    nominal_bitrate: Optional[str]
    hardware_profile: Optional[str]
    codec_private_data: str = "0"
    sampling_rate: Optional[str]
    max_height: Optional[str]
    max_width: Optional[str]
    channels: Optional[str]
    bits_per_sample: Optional[str]
    packet_size: Optional[str]
    audio_tag: Optional[str]
    four_cc: Optional[str]
    nal_unit_length_field: Optional[str]

    def __init__(self, index: str,
                 bitrate: str,
                 buffer_time: Optional[str] = None,
                 nominal_bitrate: Optional[str] = None,
                 hardware_profile: Optional[str] = None,
                 codec_private_data: str = "0",
                 sampling_rate: Optional[str] = None,
                 max_height: Optional[str] = None,
                 max_width: Optional[str] = None,
                 channels: Optional[str] = None,
                 bits_per_sample: Optional[str] = None,
                 packet_size: Optional[str] = None,
                 audio_tag: Optional[str] = None,
                 four_cc: Optional[str] = None,
                 nal_unit_length_field: Optional[str] = None):
        self.index = index
        self.bitrate = bitrate
        self.buffer_time = buffer_time
        self.nominal_bitrate = nominal_bitrate
        self.hardware_profile = hardware_profile
        self.codec_private_data = codec_private_data
        self.sampling_rate = sampling_rate
        self.max_height = max_height
        self.max_width = max_width
        self.channels = channels
        self.bits_per_sample = bits_per_sample
        self.packet_size = packet_size
        self.audio_tag = audio_tag
        self.four_cc = four_cc
        self.nal_unit_length_field = nal_unit_length_field

    def to_xml(self) -> ET.Element:
        quality_level = ET.Element("QualityLevel")
        if self.index:
            quality_level.set("Index", self.index)
        if self.bitrate:
            quality_level.set("Bitrate", self.bitrate)
        if self.buffer_time:
            quality_level.set("BufferTime", self.buffer_time)
        if self.nominal_bitrate:
            quality_level.set("NominalBitrate", self.nominal_bitrate)
        if self.hardware_profile:
            quality_level.set("HardwareProfile", self.hardware_profile)
        if self.codec_private_data:
            quality_level.set("CodecPrivateData", self.codec_private_data.upper())
        if self.max_height:
            quality_level.set("MaxHeight", self.max_height)
        if self.max_width:
            quality_level.set("MaxWidth", self.max_width)
        if self.sampling_rate:
            quality_level.set("SamplingRate", self.sampling_rate)
        if self.channels:
            quality_level.set("Channels", self.channels)
        if self.bits_per_sample:
            quality_level.set("BitsPerSample", self.bits_per_sample)
        if self.packet_size:
            quality_level.set("PacketSize", self.packet_size)
        if self.audio_tag:
            quality_level.set("AudioTag", self.audio_tag)
        if self.four_cc:
            quality_level.set("FourCC", self.four_cc.upper())
        if self.nal_unit_length_field:
            quality_level.set("NALUnitLengthField", self.nal_unit_length_field)
        Common.sort_attributes_in_xml(quality_level)
        return quality_level

    def __eq__(self, other):
        return self.bitrate == other.bitrate
