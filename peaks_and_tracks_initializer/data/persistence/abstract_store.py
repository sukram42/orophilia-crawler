
from abc import ABC, abstractmethod
from typing import List

from crawler.models import MountainList, PointOfInterest, Region, RegionList, Route, Route2Waypoint, Waypoint


class Store(ABC):
    
    @abstractmethod
    def persist_regions(regions: RegionList):
        ...

    @abstractmethod
    def persist_peaks(peaks: MountainList):
        ...

    @abstractmethod
    def persist_point_of_interest(point_of_interest: PointOfInterest):
        ...

    @abstractmethod
    def persist_route(route: Route):
        ...

    @abstractmethod
    def persist_waypoints(waypoints: List[Waypoint]):
        ...

    @abstractmethod
    def persist_route_to_waypoints(route_to_waypoints: List[Route2Waypoint]):
        ...

    @abstractmethod    
    def get_ingested_regions()->RegionList:
        ...