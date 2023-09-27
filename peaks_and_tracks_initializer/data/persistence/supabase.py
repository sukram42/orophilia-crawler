from functools import lru_cache
import json
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from crawler.models import (
    MountainList,
    PointOfInterest,
    RegionList,
    Route,
    Route2Waypoint,
    Waypoint,
)
from peaks_and_tracks_initializer.data.persistence.abstract_store import Store
from supabase import create_client


class SupabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    supabase_url: str
    supabase_key: str


class SupabaseStore(Store):
    def __init__(self) -> None:
        super().__init__()
        config = SupabaseConfig()
        self.client = create_client(config.supabase_url, config.supabase_key)

    def persist_regions(self, regions: RegionList):
        self.client.table("regions").upsert(regions.model_dump()).execute()

    def persist_peaks(self, peaks: MountainList):
        self.client.table("mountains").insert(peaks.model_dump(), upsert=True).execute()

    def persist_point_of_interest(self, point_of_interest: PointOfInterest):
        self.client.table("points-of-interest").upsert(
            # Pydantic does not serialize sub-enums. Hence this little workaround
            json.loads(point_of_interest.model_dump_json())
        ).execute()

    def persist_route(self, route: Route):
        (
            self.client.table("routes")
            .upsert(route.model_dump(exclude_none=True, exclude_unset=True))
            .execute()
        )

    def persist_waypoints(self, waypoints: List[Waypoint]):
        self.client.table("waypoints").upsert(waypoints).execute()

    def persist_route_to_waypoints(self, route_to_waypoints: List[Route2Waypoint]):
        self.client.table("route2waypoint").upsert(route_to_waypoints).execute()

    def get_ingested_regions(self) -> RegionList:
        data = self.client.table("regions").select("*").execute()
        # Convert to regionList
        return RegionList.model_validate(data.data)


@lru_cache()
def get_supabase_store():
    return SupabaseStore()
