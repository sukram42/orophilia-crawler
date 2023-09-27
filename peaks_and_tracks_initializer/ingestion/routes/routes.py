from typing import List, Optional, Tuple
from crawler.models import (
    T_SAC_HIKE_MAPPING,
    Mountain,
    PointOfInterest,
    Route,
    Route2Waypoint,
    Waypoint,
)

import osmnx as ox
import networkx as nx

from peaks_and_tracks_initializer.ingestion.routes.routes_utils import convert_uiaa

TRACK_CONDITION = '["highway"~"path|track|via_ferrata"]'

utw = ox.settings.useful_tags_way + [
    "sac_scale",
    "climbing:grade:uiaa",
    "name",
    "trail_visibility",
    "note",
    "surface",
    "via_ferrata"
]
ox.config(use_cache=True, log_console=False, useful_tags_way=utw)



def get_route_from_point_of_interest_to_peak(
    point: PointOfInterest, peak: Mountain, route_radius=10000
) -> Tuple[Optional[Route], List[Waypoint], List[Route2Waypoint]]:
    """Get a route and its waypoints from a peak to a point of interest.

    Parameters
    ----------
    point : PointOfInterest
        _description_
    peak : Mountain
        _description_
    route_radius : int, optional
        radius of the graph in meter, by default 10000

    Returns
    -------
    Tuple[Route, List[Waypoint]]
        Returns the waypoints and the route
    """
    # Get graph
    G = ox.graph_from_point(
        peak.point,
        dist=route_radius,
        network_type="all",
        custom_filter=TRACK_CONDITION,
        # simplification drops islands.
        simplify=False,
    )

    # Add Elevation
    elevation_set = "C:/Users/Markus/Documents/open-topo-data/opentopodata/data/etopo1/ETOPO1_Ice_g_geotiff.tif"
    G = ox.add_node_elevations_raster(G, elevation_set)


    # Get nearest node to peak
    mountain_node = ox.distance.nearest_nodes(G, peak.lon, peak.lat)
    # Get nearest node to point of interest
    poi_node = ox.distance.nearest_nodes(G, point.lon, point.lat)

    # calculate shortest path
    # TODO refine this method
    try:
        route = nx.shortest_path(G, mountain_node, poi_node, weight="length")
        length = nx.shortest_path_length(G, mountain_node, poi_node, weight="length")
    except nx.exception.NetworkXNoPath:
        return None, [], []


    # get route
    new_route = Route(
        id=get_route_id(peak, point),
        name=f"from {point.name}",
        mountain=peak.id,
        starting_point=point.id,
        generated=True,
        length=length
    )

    way_point_relations=[]

    # add tags
    hike_difficulties = []
    uiaa_difficulties = []
    via_ferrata_scale = []
    is_via_ferrata = False
    hike_names = []
    route_coordinates = []

    way_points = []

    for part in range(len(route) - 1):
        # Get the edge
        _edge = G.get_edge_data(route[part], route[part + 1])[0]

        # Get the T-Scale difficulty
        hike_difficulties.append(
            T_SAC_HIKE_MAPPING.get(_edge.get("sac_scale", "unknown"), -1)
        )

        # Get the UIAA grades
        uiaa_difficulties.append(convert_uiaa(_edge.get("climbing:grade:uiaa")))
        if _edge.get("highway")=="via_ferrata": 
            is_via_ferrata = True
            via_ferrata_scale.append(_edge.get("via_ferrata_scale", -1))

        # Get the names of tracks
        hike_names.append(_edge.get("name"))

        # Get coordinates of waypoint
        _point = G.nodes[route[part]]
        route_coordinates.append([_point["y"], _point["x"]])

        # Add Waypoints to route
        way_points.append(
            Waypoint(id=route[part], lat=_point["y"], lon=_point["x"]).model_dump()
        )
        # Save the relations. We do it already here, so we can be sure about the index
        way_point_relations.append(
                Route2Waypoint(
                    route=new_route.id, waypoint=route[part], index=part
                ).model_dump()
        )

 
    new_route.hike_difficulty = max(hike_difficulties)
    new_route.is_via_ferrata = is_via_ferrata
    # TODO Adding via ferrata scale
    new_route.uiaa_difficulty = max(uiaa_difficulties)
    new_route.via = [*set(filter(lambda _name: _name is not None, hike_names))]
    

    
    return (new_route, way_points, way_point_relations)


def get_route_id(peak: Mountain, point: PointOfInterest)->str:
    """Gets a deterministic path"""
    return f"{str(peak.id)[:5]}{str(point.id)[:5]}"
