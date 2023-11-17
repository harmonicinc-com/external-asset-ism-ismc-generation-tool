from external_asset_ism_ismc_generation_tool.mp4_data_parser.model.descriptor.descriptor import Descriptor


class ESDescriptorDecoderConfig(Descriptor):
    tag: int
    object_type_indication: int
    stream_type: int
    up_stream: int
    buffer_size: int
    max_bitrate: int
    avg_bitrate: int

    def __init__(self, tag: int, object_type_indication: int, stream_type: int, up_stream: int, buffer_size: int, max_bitrate: int, avg_bitrate: int):
        self.object_type_indication = object_type_indication
        self.stream_type = stream_type
        self.up_stream = up_stream
        self.buffer_size = buffer_size
        self.max_bitrate = max_bitrate
        self.avg_bitrate = avg_bitrate
        super().__init__(tag)
