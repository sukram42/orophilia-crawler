
from abc import ABC, abstractmethod
from typing import List

import requests

from crawler.models import Point


class AbstractElevationFetcher(ABC):

    @abstractmethod
    def get_elevation(self, coords: List[Point]):
        ...




class OpenElevationElevationFetcher(AbstractElevationFetcher):

    base_url = "http://api.open-elevation.com/api/v1"
    def get_elevation(self, coords: List[Point]):
        endpoint = "/lookup"
        data = requests.post(
            f"{self.base_url}{endpoint}", 
            headers={"Accept": "application/json",
                     "Content-Type": "application/json"},
            data={
            "locations": [{
                "latitude": c.lat,
                "longitude": c.lon
            } for c in coords]
        })
        print(data)

fe  = OpenElevationElevationFetcher()
fe.get_elevation([Point(lat=57.728905, lon=11.949309)])#