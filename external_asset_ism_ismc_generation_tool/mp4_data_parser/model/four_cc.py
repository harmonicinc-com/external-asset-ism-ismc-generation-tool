from enum import Enum


class FourCC(Enum):
    AVC1 = 'AVC1'
    HVC1 = 'HVC1'
    HEVC1 = 'HEV1'
    AAC = 'AAC'
    AAC_CL = 'AACL'
    AAC_HE = 'AACH'
    AACP = 'AACP'

    UNKNOWN = None

    @classmethod
    def _missing_(cls, value):
        return FourCC.UNKNOWN

