from typing import Optional


class BoxTypeRelation:
    parents: Optional[list]
    children: Optional[list]

    def __init__(self, parents: Optional[list], children: Optional[list]):
        self.parents = parents
        self.children = children
