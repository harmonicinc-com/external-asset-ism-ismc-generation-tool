import io

from azure.storage.blob import BlobServiceClient, BlobClient
from external_asset_ism_ismc_generation_tool.common.logger.i_logger import ILogger
from external_asset_ism_ismc_generation_tool.common.logger.logger import Logger


class AzureBlobServiceClient:
    __logger: ILogger = Logger("AzureBlobServiceClient")

    @classmethod
    def redefine_logger(cls, logger: ILogger):
        cls.__logger = logger

    def __init__(self, settings: dict):
        if 'container_name' in settings:
            self.container_name = settings['container_name']
        else:
            self.__logger.error(f'Azure Container name is not defined in settings: {settings}')
            raise ValueError("Azure container name is not defined")

        self.connection_string = self.__get_connection_string(settings)

        self.blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)

    def get_list_of_blobs(self):
        return self.container_client.list_blobs()

    def download_part_of_blob(self, blob_name: str, offset=None, length=None):
        blob_client = BlobClient.from_connection_string(conn_str=self.connection_string,
                                                        container_name=self.container_name,
                                                        blob_name=blob_name)
        return blob_client.download_blob(offset=offset, length=length).readall()

    def upload_blob_to_container(self, blob_name: str, content: str):
        stream = io.BytesIO(content.encode())
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.upload_blob(stream)

    def blob_exists(self, blob_name: str):
        blob_client = self.container_client.get_blob_client(blob_name)
        return blob_client.exists()

    def __get_connection_string(self, settings: dict):
        if 'connection_string' in settings:
            return settings['connection_string']
        elif 'account_name' in settings and 'account_key' in settings:
            return f"DefaultEndpointsProtocol=https;" \
                   f"AccountName={settings['account_name']};" \
                   f"AccountKey={settings['account_key']};" \
                   f"EndpointSuffix=core.windows.net"
        else:
            self.__logger.error(f'Azure Connection string is not defined in settings: {settings}')
            raise ValueError("Azure connection string is not defined")
