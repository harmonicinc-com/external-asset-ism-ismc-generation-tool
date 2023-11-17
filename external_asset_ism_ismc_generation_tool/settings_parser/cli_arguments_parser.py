import argparse

from external_asset_ism_ismc_generation_tool.common.logger.i_logger import ILogger
from external_asset_ism_ismc_generation_tool.common.logger.logger import Logger


class CliArgumentsParser:
    __logger: ILogger = Logger("CliArgumentsParser")

    @classmethod
    def redefine_logger(cls, logger: ILogger):
        cls.__logger = logger

    @staticmethod
    def parse() -> dict:
        argument_parser = argparse.ArgumentParser(description="Argument parser for mp4_manifests_creator cli")
        argument_parser.add_argument('-connection_string', metavar='connection_string', type=str, help="Connection string for the Azure Storage account.")
        argument_parser.add_argument('-container_name', metavar="container_name", type=str, help="Azure container name")
        settings = vars(argument_parser.parse_args())
        CliArgumentsParser.__logger.info(f'Get settings from the command line args: {settings}')
        return {key: value for key, value in settings.items() if value is not None}
