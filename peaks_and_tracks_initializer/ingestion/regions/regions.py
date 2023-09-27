import os
from typing import List
from crawler.models import Region, RegionList
from peaks_and_tracks_initializer.data.overpass import get_overpass_client

QUERY_FILE = "regions.query"


def convert_raw_to_regions(region: dict) -> Region:
    """
    Method to convert an dictionary to a Region
    """
    if region.get("tags", {}) == None:
        return

    return Region(
        id=region["id"],
        name=region.get("tags", {}).get("name", "No Name"),
        wikidata=region.get("tags", {}).get("wikidata"),
    )


def crawl_regions() -> RegionList:
    """Method to crawl different regions

    Returns
    -------
    List[Region]
        _description_
    """
    client = get_overpass_client()
    res = client.file_query(os.path.join(os.path.dirname(__file__), QUERY_FILE))

    regions = [
        *map(lambda i: {"id": i["id"], "tags": i.get("tags")}, res.json()["elements"])
    ]

    # Convert to Region type
    regions = map(convert_raw_to_regions, regions)
    regions = filter(lambda _region: _region is not None, regions)
    return RegionList([*regions])
