from enum import Enum


class StreamType(Enum):
    VIDEO = "video"
    AUDIO = "audio"
    TEXT = "text"

    UNKNOWN = None

    @classmethod
    def _missing_(cls, value):
        return StreamType.UNKNOWN
