from typing import List

from external_asset_ism_ismc_generation_tool.common.bit_reader import BitReader
from external_asset_ism_ismc_generation_tool.common.logger.i_logger import ILogger
from external_asset_ism_ismc_generation_tool.common.logger.logger import Logger
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.descriptor.descriptor import Descriptor
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.descriptor.descriptor_type import DescriptorType
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.descriptor.es_descriptor import ESDescriptor
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.descriptor.es_descriptor_decoder_config import ESDescriptorDecoderConfig
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.descriptor.es_descriptor_decoder_specific_info import \
    ESDescriptorDecoderSpecificInfo


class DescriptorParser:
    __logger: ILogger = Logger("DescriptorParser")

    @classmethod
    def redefine_logger(cls, logger: ILogger):
        cls.__logger = logger

    @staticmethod
    def parse(data: bytes) -> List[Descriptor]:
        descriptors = []
        reader = BitReader(data)
        while reader.tell() < len(data):
            tag = reader.get_bits(8)
            length = reader.get_bits(8)

            descriptor_type = DescriptorType(tag)
            DescriptorParser.__logger.info(f'Descriptor tag {tag} - type {descriptor_type} detected')
            if descriptor_type == DescriptorType.ES_DESCRIPTOR:
                DescriptorParser.__logger.info(f'Parse {descriptor_type}')
                es_id = reader.get_bits(16)
                bits = reader.get_bits(8)
                flags = (bits >> 5) & 7
                stream_priority = bits & 0x1F

                descriptors.append(ESDescriptor(tag=tag,
                                                es_id=es_id,
                                                flags=flags,
                                                stream_priority=stream_priority))

            elif descriptor_type == DescriptorType.ES_DESCRIPTOR_DECODER_CONFIG:
                DescriptorParser.__logger.info(f'Parse {descriptor_type}')
                object_type_indication = reader.get_bits(8)
                bits = reader.get_bits(8)
                stream_type = (bits >> 2) & 0x3F
                up_stream = bits & 2
                buffer_size = reader.get_bits(24)
                max_bitrate = reader.get_bits(32)
                avg_bitrate = reader.get_bits(32)
                descriptors.append(ESDescriptorDecoderConfig(tag=tag,
                                                             object_type_indication=object_type_indication,
                                                             stream_type=stream_type,
                                                             up_stream=up_stream,
                                                             buffer_size=buffer_size,
                                                             max_bitrate=max_bitrate,
                                                             avg_bitrate=avg_bitrate))

            elif descriptor_type == DescriptorType.ES_DESCRIPTOR_DECODER_SPECIFIC_INFO:
                DescriptorParser.__logger.info(f'Parse {descriptor_type}')
                decoder_specific_info = reader.read_bytes(length)
                descriptors.append(ESDescriptorDecoderSpecificInfo(tag=tag, decoder_specific_info=decoder_specific_info))

        return descriptors
