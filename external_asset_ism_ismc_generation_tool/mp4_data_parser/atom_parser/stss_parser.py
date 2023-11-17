from typing import Optional

from pymp4.parser import Box

from external_asset_ism_ismc_generation_tool.common.logger.i_logger import ILogger
from external_asset_ism_ismc_generation_tool.common.logger.logger import Logger


class STSSParser:
    __logger: ILogger = Logger("STSSParser")

    @classmethod
    def redefine_logger(cls, logger: ILogger):
        cls.__logger = logger

    def __init__(self, stss_atom: Box):
        self.stss_atom = stss_atom

    def get_key_frames_numbers_from_stss(self) -> Optional[list]:
        if self.stss_atom:
            return [str(entry.sample_number) for entry in self.stss_atom['entries']]
