from typing import Optional

from external_asset_ism_ismc_generation_tool.mp4_data_parser.mp4_extractor.box_type_relation import BoxTypeRelation


class BoxTypeRelationMap:
    __map: dict

    def __init__(self, relation_box_map: dict):
        self.__map = relation_box_map

    def __contains__(self, item: str) -> bool:
        return item in self.__map

    def __getitem__(self, item: str) -> Optional[BoxTypeRelation]:
        if item not in self.__map:
            return None

        return self.__map[item]
