from external_asset_ism_ismc_generation_tool.common.base_model import BaseModel


class Hvcc(BaseModel):
    configuration_version: int
    general_profile_space: int
    general_profile: int
    general_tier_flag: int
    general_profile_compatibility_flags: int
    general_constraint_indicator_flags: int
    general_level: int
    min_spatial_segmentation: int
    parallelism_type: int
    chroma_format: int
    chroma_bit_depth: int
    luma_bit_depth: int
    average_frame_rate: int
    constant_frame_rate: int
    num_temporal_layers: int
    temporal_id_nested: int
    nalu_length_size: int
    nalu_list: list

    def __init__(self,
                 configuration_version: int,
                 general_profile_space: int,
                 general_profile: int,
                 general_tier_flag: int,
                 general_profile_compatibility_flags: int,
                 general_constraint_indicator_flags: int,
                 general_level: int,
                 min_spatial_segmentation: int,
                 parallelism_type: int,
                 chroma_format: int,
                 chroma_bit_depth: int,
                 luma_bit_depth: int,
                 average_frame_rate: int,
                 constant_frame_rate: int,
                 num_temporal_layers: int,
                 temporal_id_nested: int,
                 nalu_length_size: int,
                 nalu_list: list):
        self.configuration_version = configuration_version
        self.general_profile_space = general_profile_space
        self.general_profile = general_profile
        self.general_tier_flag = general_tier_flag
        self.general_profile_compatibility_flags = general_profile_compatibility_flags
        self.general_constraint_indicator_flags = general_constraint_indicator_flags
        self.general_level = general_level
        self.min_spatial_segmentation = min_spatial_segmentation
        self.parallelism_type = parallelism_type
        self.chroma_format = chroma_format
        self.chroma_bit_depth = chroma_bit_depth
        self.luma_bit_depth = luma_bit_depth
        self.average_frame_rate = average_frame_rate
        self.constant_frame_rate = constant_frame_rate
        self.num_temporal_layers = num_temporal_layers
        self.temporal_id_nested = temporal_id_nested
        self.nalu_length_size = nalu_length_size
        self.nalu_list = nalu_list
