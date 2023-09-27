from functools import partial
import os
from typing import Dict
from crawler.models import Mountain, PointOfInterest, PointOfInterestType
from peaks_and_tracks_initializer.data.overpass import get_overpass_client


def get_point_around_peak(peak: Mountain,
                          way_radius: int,
                          way_condition: str,
                          point_of_interest_type: PointOfInterestType):
    """Get specific `ways` (e.g parking spot, alpine_hut) around a certain node (e.g peak)

    Parameters
    ----------
    point : Point
        The point which is the start point
    way_radius : int
        The radius around the point to search, in meters
    way_condition : str
        The Overpass condition for the way. Will be inserted in the query e.g way[<way_condition>]. e.g amenity=parking
    node_condition : str, optional
        The condition of the node. By default we search for peaks., by default "natural=peak"
    node_radius : int, optional
        the radius around the location to look for a peak, by default 100
    """
    QUERY_FILE = "way_around_node_search.query"
    client = get_overpass_client()
    res = client.file_query(
        os.path.join(os.path.dirname(__file__), QUERY_FILE),
        way_condition=way_condition,
        way_radius=way_radius,
        node_radius=100,
        node_condition="natural=peak",

        lat=peak.lat, 
        lon=peak.lon
    )

    mountain_huts = filter(lambda item: item["type"] == "way", res.json()["elements"])
    mountain_huts = map(partial(convert_to_point_of_interest, type=point_of_interest_type), mountain_huts)

    return [*mountain_huts] 

def convert_to_point_of_interest(item: Dict, type: PointOfInterestType):
    """Method

    Parameters
    ----------
    item : Dict
        _description_
    point_of_interest_type : _type_
        _description_
    """
    return PointOfInterest(
        id=item["id"],
        name=item["tags"].get("name", "no name"),
        lat=item["center"]["lat"],
        lon=item["center"]["lon"],
        type=type,
        tags=item["tags"],
    )