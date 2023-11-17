from external_asset_ism_ismc_generation_tool.common.base_model import BaseModel
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.audio_object_type import AudioObjectType


class EsdsDecoderSpecificInfo(BaseModel):
    object_type: AudioObjectType
    is_sbr_present: int
    is_ps_present: int

    def __init__(self, object_type: AudioObjectType, is_sbr_present: int, is_ps_present: int):
        self.object_type = object_type
        self.is_sbr_present = is_sbr_present
        self.is_ps_present = is_ps_present
