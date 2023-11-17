from typing import Tuple

from external_asset_ism_ismc_generation_tool.common.logger.i_logger import ILogger
from external_asset_ism_ismc_generation_tool.common.logger.logger import Logger
from external_asset_ism_ismc_generation_tool.mp4_data_parser.mp4_extractor.mp4_extractor import MP4Extractor
from external_asset_ism_ismc_generation_tool.mp4_data_parser.mp4_track_info_extractor import Mp4TrackInfoExtractor


class Mp4DataParser:
    __logger: ILogger = Logger("Mp4DataParser")

    @classmethod
    def redefine_logger(cls, logger: ILogger):
        cls.__logger = logger

    @staticmethod
    def parse_atom_header(data: bytes) -> Tuple[int, str]:
        if len(data) != 8:
            Mp4DataParser.__logger.error(f'Cannot parse mp4 file: Invalid atom header length: {data}')
            raise ValueError("Invalid atom header length")

        size = int.from_bytes(data[:4], byteorder='big')
        atom_type = data[4:8].decode('utf-8')

        return size, atom_type

    @staticmethod
    def get_tracks_data(mp4_datas: dict) -> Tuple[int, list]:
        mp4_track_info_list = []
        mvhd_duration = 0
        for blob_name, mp4_data in mp4_datas.items():
            mp4_atoms = MP4Extractor.extract_mp4_boxes(mp4_data)
            if not mp4_atoms:
                Mp4DataParser.__logger.error(f'Cannot get mp4 atoms from mp4 data: {mp4_data} for {blob_name}')
                raise ValueError("Cannot get mp4 atoms from mp4 data")
            moov_atom = MP4Extractor.get_mp4_box(mp4_atoms, 'moov')
            if moov_atom:
                mvhd_atom = MP4Extractor.get_mp4_sub_box(moov_atom, 'mvhd')
                mvhd_duration = mvhd_atom['duration'] / mvhd_atom['timescale']
                trak_atoms = MP4Extractor.get_all_mp4_sub_boxes(moov_atom, 'trak')

                for trak_atom in trak_atoms:
                    mp4_track_info_creator = Mp4TrackInfoExtractor(trak_atom, mvhd_atom['duration'], mvhd_atom['timescale'], blob_name)
                    mp4_track_info_list.append(mp4_track_info_creator.get_track_info())
            else:
                Mp4DataParser.__logger.error(f'Cannot get tracks info: There is no `moov` atom in mp4 data for {blob_name}: {mp4_data}')
                raise ValueError("There is no 'moov' atom in mp4 data")
        return mvhd_duration, mp4_track_info_list
