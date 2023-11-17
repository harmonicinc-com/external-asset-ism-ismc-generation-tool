from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.descriptor.descriptor import Descriptor


class ESDescriptor(Descriptor):
    tag: int
    es_id: int
    flags: int
    stream_priority: int

    def __init__(self, tag: int, es_id: int, flags:int, stream_priority: int):
        self.es_id = es_id
        self.flags = flags
        self.stream_priority = stream_priority
        super().__init__(tag)
