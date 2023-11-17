import enum


class DescriptorType(enum.Enum):
    ES_DESCRIPTOR = 0x03
    ES_DESCRIPTOR_DECODER_CONFIG = 0x04
    ES_DESCRIPTOR_DECODER_SPECIFIC_INFO = 0x05

    UNKNOWN = None

    @classmethod
    def _missing_(cls, value):
        return DescriptorType.UNKNOWN
