import decimal
from typing import Optional

from pymp4.parser import Box

from external_asset_ism_ismc_generation_tool.common.logger.i_logger import ILogger
from external_asset_ism_ismc_generation_tool.common.logger.logger import Logger
from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.track_type import TrackType


class STTSParser:
    __logger: ILogger = Logger("STTSParser")

    @classmethod
    def redefine_logger(cls, logger: ILogger):
        cls.__logger = logger

    def __init__(self, stts_atom: Box):
        self.stts_atom = stts_atom
        self.stts_atom_entries = stts_atom['entries']

    def get_sample_count(self) -> int:
        return sum(entry.sample_count for entry in self.stts_atom_entries)

    def get_duration_for_sample(self, sample_number: int) -> int:
        sample_count = 0
        for entry in self.stts_atom_entries:
            sample_count += entry.sample_count
            if sample_number <= sample_count:
                return entry.sample_delta
        return 0

    def get_chunk_durations_from_stts(self, track_type: TrackType, timescale: int, key_frames_numbers: Optional[list] = None) -> list:
        _SEGMENT_DURATION = 2  # 2 sec TODO: move to general settings
        chunk_durations: list = []

        sample_number = 1
        sample_count = self.get_sample_count()
        chunk_duration = 0

        while sample_number <= sample_count:
            if chunk_duration >= _SEGMENT_DURATION * timescale and track_type == TrackType.VIDEO:
                if str(sample_number) in key_frames_numbers:
                    chunk_durations.append(chunk_duration / timescale)
                    chunk_duration = 0
            elif chunk_duration > _SEGMENT_DURATION * timescale:
                chunk_durations.append(chunk_duration / timescale)
                chunk_duration = 0
            chunk_duration += self.get_duration_for_sample(sample_number)
            sample_number += 1

        chunk_durations.append(decimal.Decimal(str(chunk_duration / timescale)))

        return chunk_durations
