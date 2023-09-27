
import os

from crawler.models import MountainList, Region

from peaks_and_tracks_initializer.data.overpass import get_overpass_client
from peaks_and_tracks_initializer.ingestion.peaks.peak_utils import conversion_method, is_mountain


QUERY_FILE = "peak_in_region.query"

def crawl_peaks_per_region(region: Region)->MountainList:
    """Crawls all peaks from a specific region"""
    client = get_overpass_client()
    peaks = client.file_query(os.path.join(os.path.dirname(__file__), QUERY_FILE),
                              region_name=region.name)
    
    return MountainList(
        [*map(
            conversion_method(region=region),
            filter(is_mountain, peaks.json()["elements"])
        )]
    )

