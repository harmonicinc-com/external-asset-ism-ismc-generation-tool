import xml.etree.ElementTree as ET

from external_asset_ism_ismc_generation_tool.common.base_model import BaseModel


class Body(BaseModel):
    switch: list

    def __init__(self):
        self.switch = []

    def add_audio(self, audio):
        self.switch.append(audio)

    def add_video(self, video):
        self.switch.append(video)

    def add_textstream(self, text_stream):
        self.switch.append(text_stream)

    def to_xml(self) -> ET.Element:
        body_element = ET.Element("body")
        switch_element = ET.Element("switch")
        for item in self.switch:
            switch_element.append(item.to_xml())
        body_element.append(switch_element)

        return body_element
