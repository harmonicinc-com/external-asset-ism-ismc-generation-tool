from external_asset_ism_ismc_generation_tool.common.base_model import BaseModel


class Avcc(BaseModel):
    configuration_version: int
    profile: int
    profile_compatibility: int
    level: int
    nalu_length_size: int
    sequence_parameters: bytes
    picture_parameter: bytes

    def __init__(self,
                 configuration_version: int,
                 profile: int,
                 profile_compatibility: int,
                 level: int,
                 nalu_length_size: int,
                 sequence_parameters: bytes,
                 picture_parameter: bytes):
        self.configuration_version = configuration_version
        self.profile = profile
        self.profile_compatibility = profile_compatibility
        self.level = level
        self.nalu_length_size = nalu_length_size
        self.sequence_parameters = sequence_parameters
        self.picture_parameter = picture_parameter
