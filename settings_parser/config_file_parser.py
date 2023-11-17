from typing import Optional

from external_asset_ism_ismc_generation_tool.common.common import Common
from external_asset_ism_ismc_generation_tool.common.logger.i_logger import ILogger
from external_asset_ism_ismc_generation_tool.common.logger.logger import Logger


class ConfigFileParser:
    config_file_path: str = "azure_config.json"
    __logger: ILogger = Logger("Common")

    @classmethod
    def redefine_logger(cls, logger: ILogger):
        cls.__logger = logger

    @classmethod
    def redefine_config_file_path(cls, config_file_path: str):
        cls.config_file_path = config_file_path

    @staticmethod
    def parse() -> Optional[dict]:
        if Common.is_file_exists(ConfigFileParser.config_file_path):
            settings = Common.read_json(ConfigFileParser.config_file_path)
            ConfigFileParser.__logger.info(f'Get settings from the config file {ConfigFileParser.config_file_path}: {settings}')
            return {key: value for key, value in settings.items() if value is not None}


