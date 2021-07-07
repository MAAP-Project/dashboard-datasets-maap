from pydantic import BaseModel
from pydantic import constr
from typing import List
from geojson_pydantic.geometries import Polygon
from geojson_pydantic.types import BBox, Position

class Site(BaseModel):

    id: constr(min_length=3)
    label: constr(min_length=3)
    center: Position
    polygon: Polygon
    bounding_box: BBox
    indicators: List[str]

    def to_dict(self, **kwargs):
        return self.dict(by_alias=True, exclude_unset=True, **kwargs)

    def to_json(self, **kwargs):
        return self.json(by_alias=True, exclude_unset=True, **kwargs)

