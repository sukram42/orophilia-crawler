# MOUNTAIN_ID = 26865139 #  WIldspitze
# MOUNTAIN_ID = 256041740 # Großvenediger
# MOUNTAIN_ID = 256042810 # Ehrwalder Sonnenspitze
# MOUNTAIN_ID = 48783387 # Hochries
# mountain_id = 1772512527 # Kampenhauptgipfel
# MOUNTAIN_ID=364134323 # Watzmann
# MOUNTAIN_ID=415842730 #Grammersberg n
# MOUNTAIN_ID=26863176 # Hochkalter
# MOUNTAIN_ID=310287862 # Drachenkopf
# MOUNTAIN_ID=3116985621 # Watzmann kind

mountain_ids = [
    # 364134323,  # Watzmann,
    1617915343 #  Mittlere Ödkarspitze
    # 256042810,  # Ehrwalder Sonnenspitze
    # 26865139,  #  WIldspitze
    # 256041740,  # Großvenediger
    # 256042810,  # Ehrwalder Sonnenspitze
    # 48783387,  # Hochries
    # 1772512527,  # Kampenhauptgipfel
    # 415842730,  # Grammersberg n
    # 26863176,  # Hochkalter
    # 310287862,  # Drachenkopf
    # 3116985621,  # Watzmann kind
]


## Upload
import os
from typing import Optional, Union
from supabase import create_client, Client
from overpass import OverpassClient
from tqdm import tqdm
from models import (
    T_SAC_HIKE_MAPPING,
    Route,
    Mountain,
    PointOfInterest,
    point_of_interest_types,
    Waypoint,
    Route2Waypoint,
)

import osmnx as ox

utw = ox.settings.useful_tags_way + [
    "sac_scale",
    "climbing:grade:uiaa",
    "name",
    "trail_visibility",
    "note",
]
ox.config(use_cache=True, log_console=True, useful_tags_way=utw)

url: str = "https://ntcmlxdemillsrdjybpc.supabase.co"
key: str = ""

supabase: Client = create_client(url, key)

def convert_uiaa(uiaa: Optional[Union[str, int]])-> int:
    if uiaa is None: 
        return -1
    
    if isinstance(uiaa, int):
        return uiaa
    
    try: 
        return int(uiaa)
    except ValueError as e:
        pass

    uiaa ={
        "I": 1,
        "II": 2, 
        "III": 3,
        "IV": 4,
        "V": 5, 
        "VI": 6,
        "VII": 7, 
        "VIII": 8, 
    }.get(uiaa.upper())

    if uiaa is None:
         return -1
    return uiaa



for mountain_id in tqdm(mountain_ids):
    # Get Mountain
    data = supabase.table("mountains").select("*").eq("id", mountain_id).execute()
    mountain = Mountain.model_validate(data.data[0])
    print(f"+++EXTRACT MOUNTAIN {mountain.name} ({mountain.id})")
    mountain_folder = f"figs/{mountain.id}_{mountain.name}"
    os.makedirs(mountain_folder, exist_ok=True)

    # Get all mountain huts near the peak
    with open("query/get_alpine_huts_near_mountain.query", "r", encoding="utf-8") as f:
        query = f.read()
    
    client = OverpassClient()
    res = client.query(query.format(lat=mountain.lat, lon=mountain.lon))
    mountain_huts = [
        *filter(lambda item: item["type"] == "way", res.json()["elements"])
    ]

    # Get a graph of all ways :
    G = ox.graph_from_point(
        mountain.point,
        dist=6000,
        network_type="all",
        custom_filter='["highway"~"path|track"]',
        simplify=False,
    )

    # Plot the streets
    # fig, ax = ox.plot_graph(G)
    # fig.show()

    def upsertRoute(r: Route):
        result = (
            supabase.table("routes")
            .upsert(r.model_dump(exclude_none=True, exclude_unset=True))
            .execute()
        )
        return Route.model_validate(result.data[0])

    def calc_for_hut(mountain_hut):
        mountain_hut_0 = (mountain_hut["center"]["lat"], mountain_hut["center"]["lon"])
        # print(mountain_hut_0)

        # Add mountain hut
        hut = PointOfInterest(
            id=mountain_hut["id"],
            name=mountain_hut["tags"].get("name", "no name"),
            lat=mountain_hut["center"]["lat"],
            lon=mountain_hut["center"]["lon"],
            type=point_of_interest_types["alpine-hut"],
            tags=mountain_hut["tags"],
        )
        # Save it
        supabase.table("points-of-interest").upsert(hut.model_dump()).execute()

        mountain_node = ox.distance.nearest_nodes(
            G, mountain.point[1], mountain.point[0]
        )
        # Get nearest node
        hut_node = ox.distance.nearest_nodes(G, mountain_hut_0[1], mountain_hut_0[0])
        # print(hut_node, mountain_node)

        # PLOT
        # c = ['r' if a==mountain_node or a==hut_node else 'g' for a in G.nodes()]
        # s = [10 if a==mountain_node or a==hut_node else 1 for a in G.nodes()]

        # fig, ax = ox.plot_graph(G, node_color=c, node_size=s)
        # import matplotlib.pyplot as plt
        # fig.savefig(f"{mountain_folder}/start_end.jpg")

        import networkx as nx

        route = nx.shortest_path(
            G, hut_node, mountain_node, weight="length"
        )  # route drawing
        length = nx.shortest_path_length(G, hut_node, mountain_node, weight="length")

        # Add new Route
        new_route = Route(
            id=f"{str(mountain_id)[:5]}{str(mountain_hut['id'])[:5]}",
            name=f"from {mountain_hut['tags']['name']}",
            mountain=mountain.id,
            length=length,
            starting_point=hut.id,
        )
        new_route = upsertRoute(new_route)

        # Path tags
        hike_difficulties = []
        uiaa_difficulties = []
        hike_names = []
        route_coordinates = []

        way_points = []
        way_point_relations = []
        for part in range(len(route) - 1):
            _edge = G.get_edge_data(route[part], route[part + 1])[0]
            hike_difficulties.append(
                T_SAC_HIKE_MAPPING.get(_edge.get("sac_scale", "unknown"), -1)
            )
            uiaa_difficulties.append(convert_uiaa(_edge.get("climbing:grade:uiaa")))

            hike_names.append(_edge.get("name"))
            # print(G.get_edge_data(route[part], route[part + 1])[0])

            _point = G.nodes[route[part]]
            route_coordinates.append([_point["y"], _point["x"]])

            # Add waypoints to route
            way_points.append(
                Waypoint(id=route[part], lat=_point["y"], lon=_point["x"]).model_dump()
            )

            # Add it to route

            way_point_relations.append(
                Route2Waypoint(
                    route=new_route.id, waypoint=route[part], index=part
                ).model_dump()
            )

        # Adding the waypoints
        supabase.table("waypoints").upsert(way_points).execute()
        supabase.table("route2waypoint").upsert(way_point_relations).execute()

        # Adding Route information from waypoints
        new_route.hike_difficulty = max(hike_difficulties)
        new_route.uiaa_difficulty = max(uiaa_difficulties)
        way_names = set(filter(lambda n: n is not None, hike_names))
        new_route.via = [*way_names]
        new_route = upsertRoute(new_route)

        # print("COORDS: \n")
        # print(route_coordinates)

        # fig, ax = ox.plot_graph_route(G, route)
        # ax.set_title(f"{mountain.name} from {mountain_hut['tags']['name']} | len: {length} | T{max(hike_difficulties)}")
        # print("Difficulties: ", hike_difficulties)
        # fig.savefig(f"{mountain_folder}/routing_{mountain_hut['tags']['name']}.jpg")

    for hut in mountain_huts:
        calc_for_hut(hut)
