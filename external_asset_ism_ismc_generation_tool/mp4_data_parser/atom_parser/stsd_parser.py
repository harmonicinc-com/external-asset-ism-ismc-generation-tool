from pymp4.parser import Box

from external_asset_ism_ismc_generation_tool.common.logger.i_logger import ILogger
from external_asset_ism_ismc_generation_tool.common.logger.logger import Logger
from external_asset_ism_ismc_generation_tool.mp4_data_parser.atom_parser.atoms_data_parser import AtomsDataParser
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.track_format import TrackFormat
from external_asset_ism_ismc_generation_tool.mp4_data_parser.mp4_extractor.mp4_extractor import MP4Extractor


class STSDParser:
    __logger: ILogger = Logger("STSDParser")

    @classmethod
    def redefine_logger(cls, logger: ILogger):
        cls.__logger = logger

    def __init__(self, stsd_atom: Box):
        self.stsd_atom = stsd_atom
        self.stsd_atom_entries = stsd_atom['entries']

    def get_track_format(self):
        return self.stsd_atom.entries[0].format.decode("utf-8")

    def get_width(self) -> int:
        track_format = self.get_track_format()
        STSDParser.__logger.info(f'Get track width for {track_format} track format')
        if track_format == TrackFormat.AVC1.value:
            return self.stsd_atom.entries[0]['width']
        elif track_format == TrackFormat.HEVC1.value:
            hvc1_atom = MP4Extractor.get_mp4_sub_box(self.stsd_atom, 'hvc1')
            hvc1_data = AtomsDataParser.parse_hvc1_data(hvc1_atom['data'])
            if hvc1_data:
                return hvc1_data.width
        return 0

    def get_height(self) -> int:
        track_format = self.get_track_format()
        STSDParser.__logger.info(f'Get track height for {track_format} track format')
        if track_format == TrackFormat.AVC1.value:
            return self.stsd_atom.entries[0]['height']
        elif track_format == TrackFormat.HEVC1.value:
            hvc1_atom = MP4Extractor.get_mp4_sub_box(self.stsd_atom, 'hvc1')
            hvc1_data = AtomsDataParser.parse_hvc1_data(hvc1_atom['data'])
            if hvc1_data:
                return hvc1_data.height
        return 0

    def get_video_codec_private_data(self) -> str:
        track_format = self.get_track_format()
        STSDParser.__logger.info(f'Get video codec private data for {track_format} track format')
        start_code = b'\x00\x00\x00\x01'.hex()
        if track_format == TrackFormat.AVC1.value:
            sample_info = self.stsd_atom.entries[0]['sample_info']
            avcc_atom = AtomsDataParser.parse_avcc(sample_info)
            if not avcc_atom:
                STSDParser.__logger.warning(f'Cannot get avcc_atom from {sample_info}')
                return ''
            sps = start_code + avcc_atom.sequence_parameters.hex()
            pps = start_code + avcc_atom.picture_parameter.hex()
            return sps + pps
        elif track_format == TrackFormat.HEVC1.value:
            hvc1_atom = MP4Extractor.get_mp4_sub_box(self.stsd_atom, 'hvc1')
            hvc1_data = AtomsDataParser.parse_hvc1_data(hvc1_atom['data'])
            if not hvc1_data:
                STSDParser.__logger.warning(f'Cannot get hvc1_data from {hvc1_atom["data"]}')
                return ''
            hvcc_atom = AtomsDataParser.parce_hvcc_data(hvc1_data.data)
            if not hvcc_atom:
                STSDParser.__logger.warning(f'Cannot get hvcc_atom from {hvc1_data.data}')
                return ''
            sps = start_code + hvcc_atom.nalu_list[1].hex()
            pps = start_code + hvcc_atom.nalu_list[2].hex()
            return sps + pps

    def get_bits_per_sample(self) -> int:
        return self.stsd_atom_entries[0].bits_per_sample

    def get_channels(self) -> int:
        return self.stsd_atom_entries[0].channels

    def get_sampling_rate(self) -> int:
        return self.stsd_atom_entries[0].sampling_rate

    def get_packet_size(self) -> int:
        return self.stsd_atom_entries[0].packet_size
