"""Module for all the helper methods in the peaks domain.
"""

import hashlib
from typing import Callable, Optional

import requests

from crawler.models import Mountain, Region


def is_mountain(item: dict)->bool:
    """Method to check if an dict describes a mountain"""

    if "tags" not in item:
        return False

    if "natural" not in item["tags"]:
        return False

    return item["tags"]["natural"] == "peak"


WIKI_DATA_URL = "https://www.wikidata.org/w/api.php?action=wbgetclaims&property=P18&entity={wikitag}&format=json"
WIKI_IMAGE_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/{hash_1}/{hash_2}/{filename_spaced}"
)
def get_image_url(item)->Optional[str]:
    """Method to get the Wikipedia image of an item.

    Parameters
    ----------
    item : OpenStreetMap Object.
        The object returned from open street map

    Returns
    -------
    image_url: Optional[str]
        returns the image url or just nothing.
    """
    # Get the Wikitag of the Mountain
    wikitag = item.get("tags", {}).get("wikidata")
    if wikitag is None:
        return

    # call wikidata api
    response = requests.get(WIKI_DATA_URL.format(wikitag=wikitag))
    data = response.json()

    # Get all the pictures
    filename = data.get("claims", {}).get("P18", [])

    if len(filename) == 0:
        return

    # Get the file name
    filename = filename[0].get("mainsnak", {}).get("datavalue", {}).get("value")
    if filename is None:
        return

    # Refactor the filename
    filename_spaced = filename.replace(" ", "_")
    # hash the filename (needed for image URL)
    hash = hashlib.md5(filename_spaced.encode("utf-8")).hexdigest()

    # Get the image url
    return WIKI_IMAGE_URL.format(
        hash_1=hash[:1], hash_2=hash[:2], filename_spaced=filename_spaced
    )

def conversion_method(region: Region)->Callable:
    """Returns a method to convert a dict to an Mountain Object

    Parameters
    ----------
    region : Region
        The region for which this function should hold.
    """
    def convert_to_mountain(item: dict) -> Mountain:
        """Method to convert a dictionary to a Mountain object

        Returns
        -------
        Mountain
            The mountain which the dict is describing
        """
        height = item["tags"].get("ele")
        return Mountain(
            id=item["id"],
            name=item["tags"].get("name", "No Name Gipfel"),
            height=int(float(height)) if height else None,
            lat=item["lat"],
            lon=item["lon"],
            wikidata=item["tags"].get("wikidata"),
            tags=item["tags"],
            region=region.id,
            wikiimage_url=get_image_url(item),
        )

    return convert_to_mountain