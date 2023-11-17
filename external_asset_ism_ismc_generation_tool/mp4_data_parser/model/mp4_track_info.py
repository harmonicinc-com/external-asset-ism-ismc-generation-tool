from typing import Optional

from external_asset_ism_ismc_generation_tool.common.base_model import BaseModel
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.track_type import TrackType


class Mp4TrackInfo(BaseModel):
    track_type: TrackType
    bit_rate: str
    track_id: int
    chunks: int
    four_cc: str
    chunk_datas: list
    blob_name: str
    codec_private_data: str
    width: Optional[int]
    height: Optional[int]
    bits_per_sample: Optional[int]
    audio_tag: Optional[str]
    channels: Optional[str]
    packet_size: Optional[str]
    sampling_rate: Optional[str]
    language: Optional[str]

    def __init__(self, track_type: TrackType,
                 bit_rate: str,
                 track_id: int,
                 chunks: int,
                 four_cc: str,
                 chunk_datas: list,
                 blob_name: str,
                 codec_private_data: str = "0",
                 width: Optional[int] = None,
                 height: Optional[int] = None,
                 bits_per_sample: Optional[int] = None,
                 audio_tag: Optional[str] = None,
                 channels: Optional[str] = None,
                 packet_size: Optional[str] = None,
                 sampling_rate: Optional[str] = None,
                 language: Optional[str] = None):
        self.track_type = track_type
        self.bit_rate = bit_rate
        self.track_id = track_id
        self.chunks = chunks
        self.four_cc = four_cc
        self.chunk_datas = chunk_datas
        self.blob_name = blob_name
        self.codec_private_data = codec_private_data
        self.width = width
        self.height = height
        self.bits_per_sample = bits_per_sample
        self.audio_tag = audio_tag
        self.channels = channels
        self.packet_size = packet_size
        self.sampling_rate = sampling_rate
        self.language = language

    def is_chunk_data_equal(self, other) -> bool:
        if not other:
            return False
        return self.chunk_datas == other.chunk_datas

    def __eq__(self, other):
        return self.track_id == other.track_id

    def __hash__(self):
        return hash(self.track_id)
