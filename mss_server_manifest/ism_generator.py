import xml.etree.ElementTree as ET
from typing import Optional

import pycountry

from external_asset_ism_ismc_generation_tool.common.logger.i_logger import ILogger
from external_asset_ism_ismc_generation_tool.common.logger.logger import Logger
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.track_type import TrackType
from external_asset_ism_ismc_generation_tool.mss_server_manifest.models.audio import Audio
from external_asset_ism_ismc_generation_tool.mss_server_manifest.models.body import Body
from external_asset_ism_ismc_generation_tool.mss_server_manifest.models.head import Head
from external_asset_ism_ismc_generation_tool.mss_server_manifest.models.smil import Smil
from external_asset_ism_ismc_generation_tool.mss_server_manifest.models.video import Video


class IsmGenerator:
    __logger: ILogger = Logger("IsmGenerator")

    @classmethod
    def redefine_logger(cls, logger: ILogger):
        cls.__logger = logger

    @staticmethod
    def generate(manifest_name: str, audios: Optional[list] = None, videos: Optional[list] = None, text_streams: Optional[list] = None) -> str:
        IsmGenerator.__logger.info(f'Create server manifest {manifest_name}.ism')
        ism_document = Smil()

        ism_document.head = IsmGenerator.__fill_head(manifest_name)
        ism_document.body = IsmGenerator.__fill_body(audios, videos, text_streams)
        xml_ism = ism_document.to_xml()
        ET.indent(xml_ism)
        ism_doc = ET.tostring(xml_ism, encoding="utf-8", method="xml")
        return ism_doc.decode("utf-8")

    @staticmethod
    def __fill_head(manifest_name: str) -> Head:
        head = Head()
        head.add_meta("formats", "mp4")
        head.add_meta("fragmentsPerHLSSegment", "1")
        head.add_meta("clientManifestRelativePath", f"{manifest_name}.ismc")
        return head

    @staticmethod
    def __fill_body(audios: Optional[list] = None, videos: Optional[list] = None, text_streams: Optional[list] = None) -> Body:
        body = Body()
        if audios:
            for audio in audios:
                IsmGenerator.__logger.info(f'Add audio data to the server manifest: {audio}')
                body.add_audio(audio)
        if videos:
            for video in videos:
                IsmGenerator.__logger.info(f'Add video data to the server manifest: {video}')
                body.add_video(video)
        if text_streams:
            for text_stream in text_streams:
                body.add_audio(text_stream)
        return body

    @staticmethod
    def get_audios(mp4_track_infos: list) -> list:
        mp4_audio_tracks = [track for track in mp4_track_infos if track.track_type == TrackType.AUDIO]
        audios = []
        for track in mp4_audio_tracks:
            language_info = pycountry.languages.lookup(track.language)
            language = language_info.alpha_2 if language_info else track.language
            audio = Audio(src=track.blob_name, system_bitrate=track.bit_rate, system_language=language)
            audio.add_param(name="trackID", value=str(track.track_id), value_type="data")
            if audio not in audios:
                audios.append(audio)
        return audios

    @staticmethod
    def get_videos(mp4_track_infos: list) -> list:
        mp4_video_tracks = list(track for track in mp4_track_infos if track.track_type == TrackType.VIDEO)
        videos = []
        for track in mp4_video_tracks:
            video = Video(src=track.blob_name, system_bitrate=track.bit_rate)
            video.add_param(name="trackID", value=str(track.track_id), value_type="data")
            videos.append(video)
        return videos
