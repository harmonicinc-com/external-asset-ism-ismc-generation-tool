import struct

from external_asset_ism_ismc_generation_tool.common.logger.i_logger import ILogger
from external_asset_ism_ismc_generation_tool.common.logger.logger import Logger


class BitReader:
    __logger: ILogger = Logger("BitReader")

    @classmethod
    def redefine_logger(cls, logger: ILogger):
        cls.__logger = logger

    # Detail: http://multimedia.cx/eggs/python-bit-classes
    __INITIAL_BIT_POSITION: int = 7
    __INITIAL_BYTE_POSITION: int = 1

    __buffer: bytes
    __bit_position: int
    __byte_position: int

    def __init__(self, buffer: bytes):
        self.__buffer = buffer
        self.__bit_position = self.__INITIAL_BIT_POSITION
        self.__byte_position = self.__INITIAL_BYTE_POSITION
        self.__byte = struct.unpack("B", self.__buffer[0].to_bytes(1, 'big'))[0]

    def get_bits(self, num_bits):
        num = 0
        mask = 1 << self.__bit_position
        while num_bits:
            num_bits -= 1
            num <<= 1
            if self.__byte & mask:
                num |= 1
            mask >>= 1
            self.__bit_position -= 1
            if self.__bit_position < 0:
                self.__bit_position = 7
                mask = 1 << self.__bit_position
                self.__byte = self.read_byte()
                self.__byte_position += 1
        return num

    def read_byte(self) -> int:
        if self.__byte_position < len(self.__buffer):
            return struct.unpack("B", self.__buffer[self.__byte_position].to_bytes(1, 'big'))[0]

        return 0

    def read_bytes(self, count):
        data = self.__buffer[self.__byte_position - 1: self.__byte_position - 1 + count]
        self.step(count)
        return data

    def trim(self):
        bits_to_trim = 7 - self.__bit_position
        self.get_bits(bits_to_trim)

    def tell(self):
        return self.__byte_position

    def step(self, idx):
        self.__byte_position += idx

    def ue(self):
        leading_zero_bits = -1
        b = 0
        while not b:
            leading_zero_bits += 1
            b = self.get_bits(1)
        return 2 ** leading_zero_bits - 1 + self.get_bits(leading_zero_bits)

    def current_bit(self):
        return (self.__byte_position - 1) * 8 + (7 - self.__bit_position)
