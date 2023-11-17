from pymp4.parser import Box

from external_asset_ism_ismc_generation_tool.common.logger.i_logger import ILogger
from external_asset_ism_ismc_generation_tool.common.logger.logger import Logger
from external_asset_ism_ismc_generation_tool.mp4_data_parser.atom_parser.esds_parser import ESDSParser
from external_asset_ism_ismc_generation_tool.mp4_data_parser.atom_parser.stsd_parser import STSDParser
from external_asset_ism_ismc_generation_tool.mp4_data_parser.atom_parser.stss_parser import STSSParser
from external_asset_ism_ismc_generation_tool.mp4_data_parser.atom_parser.stsz_parser import STSZParser
from external_asset_ism_ismc_generation_tool.mp4_data_parser.atom_parser.stts_parser import STTSParser
from external_asset_ism_ismc_generation_tool.mp4_data_parser.atom_parser.trak_parser import TRAKParser
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.mp4_track_info import Mp4TrackInfo
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.track_type import TrackType
from external_asset_ism_ismc_generation_tool.mp4_data_parser.mp4_extractor.mp4_extractor import MP4Extractor


class Mp4TrackInfoExtractor:
    __logger: ILogger = Logger("Mp4TrackInfoExtractor")

    @classmethod
    def redefine_logger(cls, logger: ILogger):
        cls.__logger = logger

    def __init__(self, trak_atom: Box, mvhd_duration: int, mvhd_timescale: int, blob_name: str):
        self.trak_parser = TRAKParser(trak_atom)
        mdia_atom = MP4Extractor.get_mp4_sub_box(trak_atom, 'mdia')
        minf_atom = MP4Extractor.get_mp4_sub_box(mdia_atom, 'minf')
        stbl_atom = MP4Extractor.get_mp4_sub_box(minf_atom, 'stbl')
        self.stss_parser = STSSParser(MP4Extractor.get_mp4_sub_box(stbl_atom, 'stss'))
        self.stts_parser = STTSParser(MP4Extractor.get_mp4_sub_box(stbl_atom, 'stts'))
        self.stsz_parser = STSZParser(MP4Extractor.get_mp4_sub_box(stbl_atom, 'stsz'))
        self.stsd_parser = STSDParser(MP4Extractor.get_mp4_sub_box(stbl_atom, 'stsd'))
        self.esds_parser = ESDSParser(MP4Extractor.get_mp4_sub_box(stbl_atom, 'esds'))
        self.track_type = self.trak_parser.get_track_type()
        self.track_id = self.trak_parser.get_track_id()
        self.track_size = self.stsz_parser.get_track_size()
        self.timescale = self.trak_parser.get_timescale()
        self.calculated_bit_rate = self.__calculated_bit_rate(mvhd_duration, mvhd_timescale)
        self.blob_name = blob_name

    def get_track_info(self) -> Mp4TrackInfo:
        Mp4TrackInfoExtractor.__logger.info(f'Get {self.track_type.value} track info from {self.blob_name}')
        if self.track_type == TrackType.VIDEO:
            return self.__extract_video_track_info()
        elif self.track_type == TrackType.AUDIO:
            return self.__extract_audio_track_info()

    def __extract_video_track_info(self) -> Mp4TrackInfo:
        key_frames_numbers = self.stss_parser.get_key_frames_numbers_from_stss()
        if not key_frames_numbers:
            Mp4TrackInfoExtractor.__logger.error('stss atom is not defined. Cannot get key frames numbers from stss atom')
            raise ValueError('Cannot extract video track info: stss atom is not defined')
        chunks = self.stts_parser.get_chunk_durations_from_stts(TrackType.VIDEO, self.timescale, key_frames_numbers)
        return Mp4TrackInfo(track_type=TrackType.VIDEO,
                            bit_rate=str(self.calculated_bit_rate),
                            track_id=self.track_id,
                            chunks=len(chunks),
                            four_cc=self.stsd_parser.get_track_format(),
                            chunk_datas=chunks,
                            blob_name=self.blob_name,
                            codec_private_data=self.stsd_parser.get_video_codec_private_data(),
                            width=self.stsd_parser.get_width(),
                            height=self.stsd_parser.get_height())

    def __extract_audio_track_info(self) -> Mp4TrackInfo:
        channels = self.stsd_parser.get_channels()
        packet_size = self.stsd_parser.get_packet_size()
        if packet_size == 0:
            packet_size = channels * 2
        chunks = self.stts_parser.get_chunk_durations_from_stts(TrackType.AUDIO, self.timescale)
        audio_tag = '255'  # 0xFF - undefined
        codec_private_data, bit_rate, four_cc = self.esds_parser.get_audio_track_data(self.calculated_bit_rate)
        return Mp4TrackInfo(track_type=TrackType.AUDIO,
                            bit_rate=str(bit_rate),
                            track_id=self.track_id,
                            chunks=len(chunks),
                            four_cc=four_cc,
                            chunk_datas=chunks,
                            blob_name=self.blob_name,
                            codec_private_data=codec_private_data,
                            bits_per_sample=self.stsd_parser.get_bits_per_sample(),
                            audio_tag=audio_tag,
                            channels=str(channels),
                            packet_size=str(packet_size),
                            sampling_rate=str(self.stsd_parser.get_sampling_rate()),
                            language=self.trak_parser.get_track_language())

    def __calculated_bit_rate(self, mvhd_duration, mvhd_timescale) -> int:
        track_size_in_bits = self.track_size * 8
        return int(track_size_in_bits / (mvhd_duration / mvhd_timescale))
