from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.descriptor.descriptor import Descriptor


class ESDescriptorDecoderSpecificInfo(Descriptor):
    tag: int
    decoder_specific_info: bytes

    def __init__(self, tag: int, decoder_specific_info: bytes):
        self.decoder_specific_info = decoder_specific_info
        super().__init__(tag)
