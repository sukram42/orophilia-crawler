

import unittest
from crawler.models import Mountain, Region

from peaks_and_tracks_initializer.ingestion.ingestion_controller import get_ingestion_controller


class TestIngestionController(unittest.TestCase):

    def setUp(self):
        self.client = get_ingestion_controller()

    def test_ingest_regions(self):
        res = self.client.ingest_regions()

    def test_ingest_peaks(self):
        test_region = Region(id=2121875, name="Chiemgauer Alpen")
        self.client.ingest_peaks_per_region(region=test_region)

    def test_get_ingested_regions(self):
        reg = self.client.get_ingested_regions()
        print(reg)

    def test_ingest_routes_from_interesting_points_around_mountain(self):
        mountain = Mountain(
            name="Wildspitze",
            id=26865139,
            height=3768,
            lat=46.8852429,
            lon=10.867279
        )
        self.client.ingest_routes_from_interesting_points_around_mountain(peak=mountain)
        print("hallo")
    
    def test_ingest_region(self):
        # Miminger Kette: 2131102
        region_id = 2131102
        self.client.ingest_routes_in_region(region_id=region_id)
        print("Done!")