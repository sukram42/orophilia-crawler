
from enum import Enum
from typing import Dict, List, Mapping, Optional
from pydantic import BaseModel, RootModel


class Mountain(BaseModel):
    id: int
    name: Optional[str]
    height: Optional[int] = None
    lat: float
    lon: float
    wikidata: Optional[str] = None
    tags: Optional[dict] = None
    region: Optional[int] =None 
    wikiimage_url: Optional[str]= None

    @property
    def point(self):
        return (self.lat, self.lon)

MountainList = RootModel[List[Mountain]]

class Point(BaseModel):
    lat: float
    lon: float

class Route(BaseModel):
    id: Optional[int] = None
    mountain: int
    name: str
    hike_difficulty: Optional[int] = None
    uiaa_difficulty: Optional[int] = None

    is_via_ferrata: bool = False
    via_ferrata_difficulty: Optional[int]= None

    length: Optional[float] = None
    via: Optional[List[str]] = None
    starting_point: int

    # is this route generated?
    generated: bool


class PointOfInterestType(Enum):
    ALPINE_HUT =1 
    LAKE=2
    PARKING_LOT=3


class PointOfInterest(BaseModel):
    id: Optional[int] = None
    name: str
    lat: float
    lon: float
    type: PointOfInterestType
    tags: Optional[Mapping] = None

    @property
    def point(self):
        return (self.lat, self.lon)
    
class Waypoint(BaseModel):
    id: int
    lat: float
    lon: float

class Route2Waypoint(BaseModel):
    route: int
    waypoint: int
    index: int


class Region(BaseModel):
    id: int 
    name: str
    wikidata: Optional[str] = None

RegionList = RootModel[List[Region]]


T_SAC_HIKE_MAPPING= {
    "hiking": 1,
    "mountain_hiking": 2,
    "demandng_mountain_hiking": 3,
    "alpine_hiking": 4,
    "demanding_alpine_hiking":5,
    "difficult_alpine_hiking": 6,
    "unknown": -1
}



# Deprecated
point_of_interest_types ={
    "alpine-hut": 1,
    "lake": 2, 
    "parking_lot": 3
}