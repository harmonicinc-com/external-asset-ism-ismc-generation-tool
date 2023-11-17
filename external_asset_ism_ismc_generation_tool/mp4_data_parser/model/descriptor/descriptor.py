from external_asset_ism_ismc_generation_tool.common.base_model import BaseModel


class Descriptor(BaseModel):
    tag: int

    def __init__(self, tag: int):
        self.tag = tag
