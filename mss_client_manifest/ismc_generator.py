import decimal
import xml.etree.ElementTree as ET
from itertools import chain

import pycountry
from external_asset_ism_ismc_generation_tool.common.logger.i_logger import ILogger
from external_asset_ism_ismc_generation_tool.common.logger.logger import Logger
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.four_cc import FourCC
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.mp4_track_info import Mp4TrackInfo
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.track_type import TrackType
from external_asset_ism_ismc_generation_tool.mss_client_manifest.models.chunk_data import ChunkData
from external_asset_ism_ismc_generation_tool.mss_client_manifest.models.quality_level import QualityLevel
from external_asset_ism_ismc_generation_tool.mss_client_manifest.models.smooth_streaming_media import SmoothStreamingMedia
from external_asset_ism_ismc_generation_tool.mss_client_manifest.models.stream_index import StreamIndex
from external_asset_ism_ismc_generation_tool.mss_client_manifest.models.stream_type import StreamType


class IsmcGenerator:
    __TIME_SCALE = 10000000
    __VIDEO_URL_PATTERN = 'QualityLevels({{bitrate}})/Fragments({track_name}={{start time}})'
    __AUDIO_URL_PATTERN = 'QualityLevels({{bitrate}})/Fragments({track_name}={{start time}})'
    __logger: ILogger = Logger("IsmcGenerator")

    @classmethod
    def redefine_logger(cls, logger: ILogger):
        cls.__logger = logger

    @staticmethod
    def generate(duration: int, mp4_track_infos: list) -> str:
        IsmcGenerator.__logger.info('Create client (.ismc) manifest')
        audio_stream_indexes = IsmcGenerator.__get_audio_stream_indexes(mp4_track_infos, IsmcGenerator.__TIME_SCALE)
        video_stream_indexes = IsmcGenerator.__get_video_stream_indexes(mp4_track_infos, IsmcGenerator.__TIME_SCALE)
        stream_indexes = audio_stream_indexes + video_stream_indexes
        minor_version = '0'
        if IsmcGenerator.__is_hevc_track_exists(video_stream_indexes):
            minor_version = '2'
        ismc_document = SmoothStreamingMedia(minor_version=minor_version,
                                             duration=str(round(duration * IsmcGenerator.__TIME_SCALE)),
                                             time_scale=str(IsmcGenerator.__TIME_SCALE))
        for stream_index in stream_indexes:
            ismc_document.add_stream_index(stream_index)
        xml_ismc = ismc_document.to_xml()
        ET.indent(xml_ismc)
        return ET.tostring(xml_ismc, encoding="utf-8", method="xml").decode("utf-8")

    @staticmethod
    def __get_audio_stream_indexes(mp4_track_infos: list, timescale: int) -> list:
        stream_indexes: list = []
        filtered_mp4_audio_tracks = list({track for track in mp4_track_infos if track.track_type == TrackType.AUDIO})
        for track in filtered_mp4_audio_tracks:
            stream_type = StreamType.AUDIO
            name = f"{StreamType.AUDIO.value}_{track.track_id}"
            url = IsmcGenerator.__AUDIO_URL_PATTERN.format(track_name=name)
            language_info = pycountry.languages.lookup(track.language)
            language = language_info.alpha_2 if language_info else track.language

            stream_index = StreamIndex(stream_type=stream_type,
                                       chunks=str(track.chunks),
                                       quality_levels='1',
                                       url=url,
                                       name=name,
                                       language=language)
            IsmcGenerator.__logger.info(f'Track info: {stream_index}')
            for chunk in IsmcGenerator.__get_chunks(track, timescale):
                stream_index.add_chunk_data(chunk)
            quality_level = IsmcGenerator.__get_quality_level(track, 0)
            IsmcGenerator.__logger.info(f'Audio track info - quality level: {quality_level}')
            stream_index.add_quality_level(quality_level)

            stream_indexes.append(stream_index)
        return stream_indexes

    @staticmethod
    def __get_video_stream_indexes(mp4_track_infos: list, timescale: int) -> list:
        stream_indexes: list = []
        video_tracks = list(track for track in mp4_track_infos if track.track_type == TrackType.VIDEO)
        different_stream_index_tracks = {}
        id = 0
        for track in video_tracks:
            if id not in different_stream_index_tracks:
                different_stream_index_tracks[id] = []
            if len(different_stream_index_tracks[id]) > 0 and not track.is_chunk_data_equal(different_stream_index_tracks[id][-1]):
                id += 1
                different_stream_index_tracks[id] = []
            different_stream_index_tracks[id].append(track)

        for id_tracks, video_tracks in different_stream_index_tracks.items():
            quality_level_list = IsmcGenerator.__get_video_quality_levels(video_tracks)
            first_video_track = next((track for track in video_tracks), None)
            name = StreamType.VIDEO.value + '_' + str(id_tracks)
            url = IsmcGenerator.__VIDEO_URL_PATTERN.format(track_name=name)
            stream_index = StreamIndex(stream_type=StreamType.VIDEO,
                                       chunks=str(first_video_track.chunks),
                                       quality_levels=str(len(quality_level_list)),
                                       url=url,
                                       name=name)

            IsmcGenerator.__logger.info(f'Track info: {stream_index}')
            for chunk in IsmcGenerator.__get_chunks(first_video_track, timescale):
                stream_index.add_chunk_data(chunk)
            for quality_level in quality_level_list:
                IsmcGenerator.__logger.info(f'Video track info - quality level: {quality_level}')
                stream_index.add_quality_level(quality_level)

            stream_indexes.append(stream_index)

        return stream_indexes

    @staticmethod
    def __get_video_quality_levels(mp4_track_infos: list) -> list:
        # TODO: Move configuration to the general settings
        # Do not generate a client manifest if key frames in video tracks do not match
        # if not IsmcGenerator._check_eq_video_key_frames:
        #     raise ValueError("Key frames in video tracks do not match. The manifest could not be generated")

        quality_levels: list = []
        index = 0
        for track in mp4_track_infos:
            if track.track_type == TrackType.VIDEO:

                quality_level = IsmcGenerator.__get_quality_level(track, index)
                if index > 0:
                    if quality_levels[index - 1] != quality_level:
                        quality_levels.append(quality_level)
                        index += 1
                else:
                    quality_levels.append(quality_level)
                    index += 1
        return quality_levels

    @staticmethod
    def __check_eq_video_key_frames(mp4_track_infos: list) -> bool:
        base_track = next((track for track in mp4_track_infos if track.track_type == TrackType.VIDEO), None)
        if not base_track:
            return False
        return all(base_track.is_chunk_data_equal(track) for track in mp4_track_infos if track.track_type == TrackType.VIDEO)

    @staticmethod
    def __get_quality_level(mp4_track_info: Mp4TrackInfo, index: int) -> QualityLevel:
        if mp4_track_info.track_type == TrackType.AUDIO:
            return QualityLevel(index=str(index),
                                bitrate=mp4_track_info.bit_rate,
                                audio_tag=mp4_track_info.audio_tag,
                                bits_per_sample=str(mp4_track_info.bits_per_sample),
                                four_cc=str(mp4_track_info.four_cc),
                                codec_private_data=str(mp4_track_info.codec_private_data),
                                channels=str(mp4_track_info.channels),
                                packet_size=str(mp4_track_info.packet_size),
                                sampling_rate=str(mp4_track_info.sampling_rate))
        elif mp4_track_info.track_type == TrackType.VIDEO:
            return QualityLevel(index=str(index),
                                bitrate=mp4_track_info.bit_rate,
                                four_cc=str(mp4_track_info.four_cc),
                                max_width=str(mp4_track_info.width),
                                max_height=str(mp4_track_info.height),
                                codec_private_data=str(mp4_track_info.codec_private_data))

    @staticmethod
    def __get_chunks(mp4_track_info, timescale):
        c: list = []
        is_first_c = True
        current_num = 0
        time_start = 0
        time_start_round = 0

        for chunk in mp4_track_info.chunk_datas:
            duration = decimal.Decimal(str(chunk * timescale))
            if is_first_c:
                c.append(ChunkData(time_start='0', duration=duration))
                is_first_c = False
            else:
                time_start += c[-1].duration
                time_start_round += round(c[-1].duration)
                diff = round(time_start) - time_start_round
                if diff != 0:
                    c[-1].duration = c[-1].duration + diff
                    time_start_round += diff

                c.append(ChunkData(duration=duration))
            current_num += 1
        return c
        # TODO: Move configuration to the general settings
        # merge chunks with the same duration into one chunk with r:

        # c_with_r = []
        # current_d = None
        # count = 0
        # for chunk in c:
        #     if chunk.duration == current_d:
        #         count += 1
        #         c_with_r[-1].r = str(count)
        #     else:
        #         count = 0
        #         current_d = chunk.duration
        #         c_with_r.append(ChunkData(time_start=chunk.time_start, duration=current_d))
        # return c_with_r

    @staticmethod
    def __is_hevc_track_exists(video_stream_indexes: list) -> bool:
        quality_level_list = list(chain.from_iterable(video_stream_index.quality_level_list for video_stream_index in video_stream_indexes))
        return any(four_cc.upper() == FourCC.HVC1.value for four_cc in [quality_level.four_cc for quality_level in quality_level_list])
