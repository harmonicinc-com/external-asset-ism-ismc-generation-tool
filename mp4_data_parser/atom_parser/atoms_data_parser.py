from typing import Optional

from construct import Container

from external_asset_ism_ismc_generation_tool.common.bit_reader import BitReader
from external_asset_ism_ismc_generation_tool.common.logger.i_logger import ILogger
from external_asset_ism_ismc_generation_tool.common.logger.logger import Logger
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.atom.avcc_atom import Avcc
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.atom.hvc1_atom import Hvc1
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.atom.hvcc_atom import Hvcc


class AtomsDataParser:
    __logger: ILogger = Logger("AtomsDataParser")

    @classmethod
    def redefine_logger(cls, logger: ILogger):
        cls.__logger = logger

    @staticmethod
    def parse_avcc(sample_info: Container) -> Optional[Avcc]:
        if sample_info:
            sample_info_data = sample_info[0]['data']
            configuration_version = sample_info_data[0]
            profile = sample_info_data[1]
            profile_compatibility = sample_info_data[2]
            level = sample_info_data[3]
            nalu_length_size = 1 + (sample_info_data[4] & 3)
            num_seq_params = sample_info_data[5] & 31
            sequence_param_length = int.from_bytes(sample_info_data[6:8], "big")
            sequence_parameters = sample_info_data[8:8 + sequence_param_length]
            current = 8 + sequence_param_length
            num_pic_params = sample_info_data[current]
            current += 1
            picture_param_length = int.from_bytes(sample_info_data[current:current + 2], "big")
            current = current + 2
            picture_parameter = sample_info_data[current:current + picture_param_length]
            return Avcc(configuration_version, profile, profile_compatibility, level, nalu_length_size, sequence_parameters, picture_parameter)

    @staticmethod
    def parse_hvc1_data(hvc1_data: bytes) -> Optional[Hvc1]:
        if hvc1_data:
            reader = BitReader(hvc1_data)
            predefined1 = reader.get_bits(16)
            reserved1 = reader.get_bits(16)
            predefined2 = reader.get_bits(12 * 8)
            width = reader.get_bits(16)
            height = reader.get_bits(16)
            horiz_resolution = reader.get_bits(32)
            vert_resolution = reader.get_bits(32)
            reserved2 = reader.get_bits(32)
            frame_count = reader.get_bits(16)
            compressor_name_full_size = 32 * 8
            compressor_name_length_size = 8
            compressor_name_length = reader.get_bits(compressor_name_length_size)
            compressor_name = reader.get_bits(compressor_name_length)
            reserved3 = reader.get_bits(compressor_name_full_size - compressor_name_length - compressor_name_length_size)
            depth = reader.get_bits(16)
            predefined3 = reader.get_bits(16)
            data = reader.read_bytes(len(hvc1_data) - reader.tell())

            return Hvc1(width=width,
                        height=height,
                        horiz_resolution=horiz_resolution,
                        vert_resolution=vert_resolution,
                        compressor_name=compressor_name,
                        data=data)

    @staticmethod
    def parce_hvcc_data(hvc1_data: bytes) -> Optional[Hvcc]:
        if not hvc1_data:
            return None
        _HVCC_ATOM_TYPE = 'hvcC'
        atom_header_size = 4
        atom_size = hvc1_data[0:4]
        atom_type = hvc1_data[4:8].decode("utf-8")
        start_byte = 8
        while atom_type != _HVCC_ATOM_TYPE:
            if len(hvc1_data) < 8:
                return None
            skip = atom_size - atom_header_size
            start_byte = 8 + skip
            atom_size = hvc1_data[start_byte: start_byte + 32]
            start_byte += 32
            atom_type = hvc1_data[start_byte: start_byte + 32].decode("utf-8")
            start_byte += 32

        data = hvc1_data[start_byte: len(hvc1_data)]
        configuration_version = data[0]
        general_profile_space = (data[1] >> 6) & 0x03
        general_tier_flag = (data[1] >> 5) & 0x01
        general_profile = (data[1]) & 0x1F
        general_profile_compatibility_flags = data[2:6]
        general_constraint_indicator_flags = int.from_bytes(data[6:12], byteorder='big')
        general_level = data[12]
        reserved1 = (data[13] >> 4) & 0x0F
        min_spatial_segmentation = int.from_bytes(data[13:14], byteorder='big') & 0x0FFF
        reserved2 = (data[15] >> 2) & 0x3F
        parallelism_type = data[15] & 0x03
        reserved3 = (data[16] >> 2) & 0x3F
        chroma_format = data[16] & 0x03
        reserved4 = (data[17] >> 3) & 0x1F
        luma_bit_depth = 8 + (data[17] & 0x07)
        reserved5 = (data[18] >> 3) & 0x1F
        chroma_bit_depth = 8 + (data[18] & 0x07)
        average_frame_rate = int.from_bytes(data[19:21], byteorder='big')
        constant_frame_rate = (data[21] >> 6) & 0x03
        num_temporal_layers = (data[21] >> 3) & 0x07
        temporal_id_nested = (data[21] >> 2) & 0x01
        nalu_length_size = 1 + (data[21] & 0x03)
        num_seq = data[22]

        current = 23
        nalus: list = []
        for i in range(0, num_seq):
            array_completeness = data[current] >> 7 & 0x01
            reserved = (data[current] >> 6) & 0x01
            nalu_type = data[current] & 0x3F
            current += 1

            nalu_count = int.from_bytes(data[current: current + 2], 'big')
            current += 2

            for j in range(0, nalu_count):
                nalu_length = int.from_bytes(data[current: current + 2], 'big')
                current += 2
                nalus.append(data[current:current + nalu_length])
                current += nalu_length

        return Hvcc(configuration_version,
                    general_profile_space,
                    general_profile,
                    general_tier_flag,
                    general_profile_compatibility_flags,
                    general_constraint_indicator_flags,
                    general_level,
                    min_spatial_segmentation,
                    parallelism_type,
                    chroma_format,
                    chroma_bit_depth,
                    luma_bit_depth,
                    average_frame_rate,
                    constant_frame_rate,
                    num_temporal_layers,
                    temporal_id_nested,
                    nalu_length_size,
                    nalus)
