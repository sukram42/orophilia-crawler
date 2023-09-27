
from typing import Dict, List, Mapping, Optional
from pydantic import BaseModel, RootModel


class Mountain(BaseModel):
    id: int
    name: Optional[str]
    height: Optional[int] = None
    lat: float
    lon: float
    wikidata: Optional[str]
    tags: Optional[dict]
    region: int
    wikiimage_url: Optional[str]

    @property
    def point(self):
        return (self.lat, self.lon)

MountainList = RootModel[List[Mountain]]

class Route(BaseModel):
    id: Optional[int] = None
    mountain: int
    name: str
    hike_difficulty: Optional[int] = None
    uiaa_difficulty: Optional[int] = None

    length: Optional[float] = None
    via: Optional[List[str]] = None
    starting_point: int


class PointOfInterest(BaseModel):
    id: Optional[int] = None
    name: str
    lat: float
    lon: float
    type: int
    tags: Mapping

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

T_sac_hike_mapping= {
    "hiking": 1,
    "mountain_hiking": 2,
    "demandng_mountain_hiking": 3,
    "alpine_hiking": 4,
    "demanding_alpine_hiking":5,
    "difficult_alpine_hiking": 6,
    "unknown": -1
}

point_of_interest_types ={
    "alpine-hut": 1,
    "lake": 2
}