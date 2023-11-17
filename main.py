from external_asset_ism_ismc_generation_tool.azure_client.azure_blob_service_client import AzureBlobServiceClient
from external_asset_ism_ismc_generation_tool.common.logger.logger import Logger
from external_asset_ism_ismc_generation_tool.common.common import Common
from external_asset_ism_ismc_generation_tool.mp4_data_parser.mp4_data_parser import Mp4DataParser
from external_asset_ism_ismc_generation_tool.mss_client_manifest.ismc_generator import IsmcGenerator
from external_asset_ism_ismc_generation_tool.mss_server_manifest.ism_generator import IsmGenerator
from external_asset_ism_ismc_generation_tool.mss_server_manifest.models.text_stream import TextStream
from external_asset_ism_ismc_generation_tool.settings_parser.cli_arguments_parser import CliArgumentsParser
from external_asset_ism_ismc_generation_tool.settings_parser.config_file_parser import ConfigFileParser


def generate_manifests():
    settings_from_cli_arguments = CliArgumentsParser.parse()
    settings_from_config_file = ConfigFileParser.parse()
    settings_list = [settings_from_config_file, settings_from_cli_arguments]
    settings = Common.merge_dicts(settings_list)

    az_blob_service_client: AzureBlobServiceClient = AzureBlobServiceClient(settings)
    text_streams = []
    logger.info(msg="Get blobs list from Azure container")
    blobs = az_blob_service_client.get_list_of_blobs()

    if blobs is None:
        logger.error(msg=f"Cannot find blobs inside the container {az_blob_service_client.container_client.container_name}")
        raise ValueError(f"Cannot find blobs inside the container {az_blob_service_client.container_client.container_name}")

    manifest_name = None

    mp4_datas: dict = {}

    for blob in blobs:
        logger.info(msg=f"Handle blob {blob.name}")
        if blob.name.endswith(".mp4"):
            if manifest_name is None:
                manifest_name = blob.name.split(".")[0]

            mp4_datas[blob.name] = __get_moov_data(az_blob_service_client, blob.name)

        if blob.name.endswith(".ttml") or blob.name.endswith(".vtt"):
            text_streams.append(TextStream(src=blob.name))

    duration, mp4_track_info_list = Mp4DataParser.get_tracks_data(mp4_datas)

    server_manifest_name = f'{manifest_name}.ism'
    if not az_blob_service_client.blob_exists(server_manifest_name):
        audios = IsmGenerator.get_audios(mp4_track_infos=mp4_track_info_list)
        videos = IsmGenerator.get_videos(mp4_track_infos=mp4_track_info_list)
        ism_xml_string = IsmGenerator.generate(manifest_name, audios=audios, videos=videos, text_streams=text_streams)
        az_blob_service_client.upload_blob_to_container(server_manifest_name, ism_xml_string)
        logger.info(f"{server_manifest_name} is created and stored to the {az_blob_service_client.container_client.container_name} container")
    else:
        logger.warning(f"{server_manifest_name} already exists")

    client_manifest_name = f'{manifest_name}.ismc'
    if not az_blob_service_client.blob_exists(client_manifest_name):
        ismc_xml_string = IsmcGenerator.generate(duration=duration, mp4_track_infos=mp4_track_info_list)
        az_blob_service_client.upload_blob_to_container(client_manifest_name, ismc_xml_string)
        logger.info(f"{client_manifest_name} is created and stored to the {az_blob_service_client.container_client.container_name} container")
    else:
        logger.warning(f"{client_manifest_name} already exists")


def __get_moov_data(az_blob_service_client: AzureBlobServiceClient, blob_name: str) -> bytes:
    _MP4_HEADER_LENGTH = 8  # 8 byte
    _MOOV_ATOM_TYPE = 'moov'
    _MDAT_ATOM_TYPE = 'mdat'

    start_byte = 0
    atom_type = ''
    atom_size = -1
    atom_header_data = ''
    mp4_data = ''

    while atom_type != _MOOV_ATOM_TYPE:
        if atom_size == _MP4_HEADER_LENGTH or atom_size == -1:
            atom_header_data = az_blob_service_client.download_part_of_blob(blob_name=blob_name,
                                                                            offset=start_byte,
                                                                            length=_MP4_HEADER_LENGTH)
            start_byte = start_byte + _MP4_HEADER_LENGTH
            atom_size, atom_type = Mp4DataParser.parse_atom_header(atom_header_data)

        if atom_type == _MOOV_ATOM_TYPE:
            mp4_data = atom_header_data + az_blob_service_client.download_part_of_blob(blob_name=blob_name,
                                                                                       offset=start_byte,
                                                                                       length=atom_size)

        start_byte = start_byte + atom_size - _MP4_HEADER_LENGTH
        atom_size = _MP4_HEADER_LENGTH

    return mp4_data


if __name__ == '__main__':
    logger: Logger = Logger("Mp4ManifestsCreator")
    generate_manifests()
