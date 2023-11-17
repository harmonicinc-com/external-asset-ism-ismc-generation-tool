from external_asset_ism_ismc_generation_tool.common.base_model import BaseModel


class Hvc1(BaseModel):
    width: int
    height: int
    horiz_resolution: int
    vert_resolution: int
    compressor_name: int
    data: bytes

    def __init__(self, width: int, height: int, horiz_resolution: int, vert_resolution: int, compressor_name: int, data: bytes):
        self.width = width
        self.height = height
        self.horiz_resolution = horiz_resolution
        self.vert_resolution = vert_resolution
        self.compressor_name = compressor_name
        self.data = data
