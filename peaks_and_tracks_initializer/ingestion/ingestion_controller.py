
from functools import lru_cache

from tqdm import tqdm

from crawler.models import Mountain, MountainList, Point, Region, RegionList, Route2Waypoint
from peaks_and_tracks_initializer.config import get_configuration
from peaks_and_tracks_initializer.data.persistence.abstract_store import Store
from peaks_and_tracks_initializer.data.persistence.supabase import get_supabase_store as get_persistence_store
from peaks_and_tracks_initializer.ingestion.peaks.peak_ingestion import crawl_peaks_per_region
from peaks_and_tracks_initializer.ingestion.points_of_interest.alpine_huts import get_alpine_huts_around_peak
from peaks_and_tracks_initializer.ingestion.points_of_interest.parking_spots import get_parking_lot_around_peak

from peaks_and_tracks_initializer.ingestion.regions.regions import crawl_regions
from peaks_and_tracks_initializer.ingestion.routes.routes import get_route_from_point_of_interest_to_peak

class IngestionController():
    def __init__(self) -> None:
        self.config = get_configuration()
        self.persistence: Store = get_persistence_store()

    def ingest_regions(self)->RegionList:
        # Get Regions
        regions = crawl_regions()
        self.persistence.persist_regions(regions)
        return regions

    def ingest_peaks_per_region(self, region: Region)->MountainList:
        """Loads and ingests the peaks of a region"""
        peaks_per_region = crawl_peaks_per_region(region)
        self.persistence.persist_peaks(peaks_per_region)
        return peaks_per_region

    def get_ingested_regions(self)->RegionList:
        """Returns the ingested Regions"""
        return self.persistence.get_ingested_regions().root
    
    def ingest_routes_from_interesting_points_around_mountain(self, peak: Mountain):

        # Get points of interest
        points_of_interests = [
            *get_alpine_huts_around_peak(peak=peak, radius=6000),
            *get_parking_lot_around_peak(peak=peak, radius=10000)
            ]
        
        # TODO Add an early return:
        # -> 2km with out considerable anstieg
        # -> 2km+ with a considerable abstieg
        # -> end point distance to peak
        # Add them to the persistence
        for poi in tqdm(points_of_interests):
            self.persistence.persist_point_of_interest(poi) 
            # Calulate routes
            route, waypoints, relation = get_route_from_point_of_interest_to_peak(point=poi, peak=peak)
            # If there is no route continue
            if route is None:
                continue
            # persist route
            self.persistence.persist_route(route)
            self.persistence.persist_waypoints(waypoints)
            self.persistence.persist_route_to_waypoints(relation)

    def ingest_routes_in_region(self, region_id: str): 
        regions = self.get_ingested_regions()
        _pos_regions = [*filter(lambda r: r.id==region_id, regions)]
        if len(_pos_regions) == 0: 
            raise ValueError(f"Region with id {region_id} not found.")
        region = _pos_regions[0]

        # Ingest all the mountains
        mountains = self.ingest_peaks_per_region(region=region)

        # iterate over mountains and ingest interesting points
        progress = tqdm(mountains.root)
        for peak in progress: 
            progress.set_description(f"{peak.name}({peak.id})")
            self.ingest_routes_from_interesting_points_around_mountain(peak)
        
@lru_cache
def get_ingestion_controller():
    return IngestionController()