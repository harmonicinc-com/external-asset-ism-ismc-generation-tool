from typing import Optional

from external_asset_ism_ismc_generation_tool.common.bit_reader import BitReader
from external_asset_ism_ismc_generation_tool.common.logger.i_logger import ILogger
from external_asset_ism_ismc_generation_tool.common.logger.logger import Logger
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.atom.esds_atom_decoder_specific_info import EsdsDecoderSpecificInfo
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.audio_object_type import AudioObjectType


class AudioAacDecoderSpecificInfoParser:
    __logger: ILogger = Logger("AudioAacDecoderSpecificInfoParser")

    @classmethod
    def redefine_logger(cls, logger: ILogger):
        cls.__logger = logger

    @staticmethod
    def parse_audio_decoder_specific_info(decoder_specific_info_data: bytes) -> Optional[EsdsDecoderSpecificInfo]:
        reader = BitReader(decoder_specific_info_data)
        decoder_specific_info_data_in_bits = len(decoder_specific_info_data) * 8
        object_type = AudioAacDecoderSpecificInfoParser.__parse_audio_object_type(reader, decoder_specific_info_data_in_bits)
        if object_type == AudioObjectType.ERROR_INVALID_FORMAT:
            AudioAacDecoderSpecificInfoParser.__logger.error(f'Cannot get audio object type from {decoder_specific_info_data.hex()}')
            return None
        sampling_frequency = AudioAacDecoderSpecificInfoParser.__parse_sampling_frequency(reader, decoder_specific_info_data_in_bits)
        if sampling_frequency == 0:
            AudioAacDecoderSpecificInfoParser.__logger.error(f'Cannot get audio sampling frequency from {decoder_specific_info_data.hex()}')
            return None
        if reader.current_bit() > decoder_specific_info_data_in_bits - 4:
            AudioAacDecoderSpecificInfoParser.__logger.error(f'Cannot get audio ES decoder specific info from {decoder_specific_info_data.hex()}')
            return None

        channel_count = reader.get_bits(4)
        if channel_count == 7:
            channel_count = 8
        elif channel_count > 7:
            channel_count = 0

        if object_type == AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_SBR or object_type == AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_PS:
            AudioAacDecoderSpecificInfoParser.__logger.info(f'Get audio specific info for object type: {object_type}')
            is_sbr_present = True
            is_ps_present = object_type == AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_PS
            resulted_object_type = AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_SBR
            resulted_sampling_frequency = AudioAacDecoderSpecificInfoParser.__parse_sampling_frequency(reader, decoder_specific_info_data_in_bits)
            if resulted_sampling_frequency == 0:
                return EsdsDecoderSpecificInfo(object_type=resulted_object_type,
                                               is_sbr_present=is_sbr_present,
                                               is_ps_present=is_ps_present)
            object_type = AudioAacDecoderSpecificInfoParser.__parse_audio_object_type(reader, decoder_specific_info_data_in_bits)
            if object_type == AudioObjectType.ERROR_INVALID_FORMAT:
                return EsdsDecoderSpecificInfo(object_type=resulted_object_type,
                                               is_sbr_present=is_sbr_present,
                                               is_ps_present=is_ps_present)
            if object_type == AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_ER_BSAC:
                if reader.current_bit() > decoder_specific_info_data_in_bits - 4:
                    return EsdsDecoderSpecificInfo(object_type=resulted_object_type,
                                                   is_sbr_present=is_sbr_present,
                                                   is_ps_present=is_ps_present)
                reader.get_bits(4)  # extensionChannelConfiguration(4)
        else:
            resulted_object_type = AudioObjectType.ERROR_INVALID_FORMAT
            resulted_sampling_frequency = 0
            is_sbr_present = False
            is_ps_present = False

        audio_object_type_list = [AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_AAC_MAIN,
                                  AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_AAC_SSR,
                                  AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_AAC_LC,
                                  AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_AAC_LTP,
                                  AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_AAC_SCALABLE,
                                  AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_TWINVQ,
                                  AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_ER_AAC_LC,
                                  AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_ER_AAC_LTP,
                                  AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_ER_AAC_SCALABLE,
                                  AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_ER_AAC_LD,
                                  AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_ER_TWINVQ,
                                  AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_ER_BSAC,
                                  AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_USAC
                                  ]

        if object_type in audio_object_type_list:
            AudioAacDecoderSpecificInfoParser.__logger.info(f'Get audio specific info for object type: {object_type}')
            is_parse_ga_specific_info = AudioAacDecoderSpecificInfoParser.__parse_ga_specific_info(reader, decoder_specific_info_data_in_bits, channel_count, object_type)
            if is_parse_ga_specific_info:
                if resulted_object_type != AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_SBR and reader.current_bit() < decoder_specific_info_data_in_bits - 16:
                    esds_decoder_specific_info = AudioAacDecoderSpecificInfoParser.__parse_extension(reader, decoder_specific_info_data_in_bits)
                    if esds_decoder_specific_info:
                        return esds_decoder_specific_info

        return EsdsDecoderSpecificInfo(object_type=object_type,
                                       is_sbr_present=is_sbr_present,
                                       is_ps_present=is_ps_present)

    @staticmethod
    def __parse_audio_object_type(reader: BitReader, dsi_data_size: int) -> AudioObjectType:
        if reader.current_bit() > dsi_data_size - 5:
            return AudioObjectType.ERROR_INVALID_FORMAT
        object_type = reader.get_bits(5)
        if object_type == 31:
            if reader.current_bit() > dsi_data_size - 6:
                return AudioObjectType.ERROR_INVALID_FORMAT
            object_type = 32 + reader.get_bits(6)
        return AudioObjectType(object_type)

    @staticmethod
    def __parse_sampling_frequency(reader: BitReader, dsi_data_size: int) -> int:
        _ERROR_FORMAT = 0
        _AAC_MAX_SAMPLING_FREQUENCY_INDEX = 12

        _AAC_SAMPLING_FREQ_TABLE = [
            96000, 88200, 64000, 48000,
            44100, 32000, 24000, 22050,
            16000, 12000, 11025, 8000,
            7350
        ]

        if reader.current_bit() > dsi_data_size - 4:
            return _ERROR_FORMAT

        sampling_frequency_index = reader.get_bits(4)
        if sampling_frequency_index == 0xF:
            if reader.current_bit() > dsi_data_size - 24:
                return _ERROR_FORMAT
            sampling_frequency = reader.get_bits(24)
        elif sampling_frequency_index <= _AAC_MAX_SAMPLING_FREQUENCY_INDEX:
            sampling_frequency = _AAC_SAMPLING_FREQ_TABLE[sampling_frequency_index]
        else:
            return _ERROR_FORMAT
        return sampling_frequency

    @staticmethod
    def __parse_ga_specific_info(reader: BitReader, dsi_data_size: int, channel_count: int, object_type: AudioObjectType) -> bool:
        if reader.current_bit() > dsi_data_size - 2:
            return False
        frame_length_flag = reader.get_bits(1) == 1
        depends_on_core_coder = reader.get_bits(1) == 1
        if depends_on_core_coder:
            if reader.current_bit() > dsi_data_size - 14:
                return False
            core_coder_delay = reader.get_bits(14)
        else:
            core_coder_delay = 0

        if reader.current_bit() > dsi_data_size - 1:
            return False

        extension_flag = reader.get_bits(1)
        if channel_count == 0:
            return False
        if object_type == AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_AAC_SCALABLE or object_type == AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_ER_AAC_SCALABLE:
            if reader.current_bit() > dsi_data_size - 3:
                return False
            reader.get_bits(3)  # layerNr

        if extension_flag:
            if object_type == AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_ER_BSAC:
                if reader.current_bit() > dsi_data_size - 16:
                    return False
                reader.get_bits(16)  # num_of_sub_frame (5), layer_length (11)
            if object_type == AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_ER_AAC_LC or \
                    object_type == AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_ER_AAC_SCALABLE or \
                    object_type == AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_ER_AAC_LD:
                if reader.current_bit() > dsi_data_size - 3:
                    return False
                reader.get_bits(3)  # aac_section_data_resilience_flag (1), aac_scale_factor_data_resilience_flag, aac_spectral_data_resilience_flag (1)
            if reader.current_bit() > dsi_data_size - 1:
                return False
            extension_flag = reader.get_bits(1)
            if extension_flag:
                return False

        return True

    @staticmethod
    def __parse_extension(reader: BitReader, dsi_data_size: int) -> Optional[EsdsDecoderSpecificInfo]:
        is_sbr_present = False
        is_ps_present = False
        if reader.current_bit() > dsi_data_size - 16:
            return None
        sync_extension_type = reader.get_bits(11)
        if sync_extension_type == 0x2b7:
            object_type = AudioAacDecoderSpecificInfoParser.__parse_audio_object_type(reader, dsi_data_size)
            if object_type == AudioObjectType.ERROR_INVALID_FORMAT:
                return None
            if object_type == AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_SBR:
                if reader.current_bit() > dsi_data_size - 1:
                    return EsdsDecoderSpecificInfo(object_type=object_type,
                                                   is_sbr_present=False,
                                                   is_ps_present=False)
                is_sbr_present = reader.get_bits(1) == 1
                if is_sbr_present:
                    sampling_frequency = AudioAacDecoderSpecificInfoParser.__parse_sampling_frequency(reader, dsi_data_size)
                    if sampling_frequency == 0:
                        return EsdsDecoderSpecificInfo(object_type=object_type,
                                                       is_sbr_present=is_sbr_present,
                                                       is_ps_present=False)
                    if reader.current_bit() < dsi_data_size - 12:
                        sync_extension_type = reader.get_bits(11)
                        if sync_extension_type == 0x548:
                            is_ps_present = reader.get_bits(1) == 1
            elif object_type == AudioObjectType.MPEG4_AUDIO_OBJECT_TYPE_ER_BSAC:
                if reader.current_bit() > dsi_data_size - (1 + 4):
                    return EsdsDecoderSpecificInfo(object_type=object_type,
                                                   is_sbr_present=False,
                                                   is_ps_present=False)
                is_sbr_present = reader.get_bits(1) == 1
                if is_sbr_present:
                    sampling_frequency = AudioAacDecoderSpecificInfoParser.__parse_sampling_frequency(reader, dsi_data_size)
                    if sampling_frequency == 0:
                        return EsdsDecoderSpecificInfo(object_type=object_type,
                                                       is_sbr_present=is_sbr_present,
                                                       is_ps_present=False)
                reader.get_bits(4)  # extension_channel_configuration

            return EsdsDecoderSpecificInfo(object_type=object_type,
                                           is_sbr_present=is_sbr_present,
                                           is_ps_present=is_ps_present)
