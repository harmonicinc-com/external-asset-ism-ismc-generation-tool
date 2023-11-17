from enum import Enum


class TrackFormat(Enum):
    MP4A = 'mp4a'
    AVC1 = 'avc1'
    HEVC1 = 'hvc1'

    UNKNOWN = None

    @classmethod
    def _missing_(cls, value):
        return TrackFormat.UNKNOWN
