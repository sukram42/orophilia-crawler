import unittest
from crawler.models import Mountain, Point, PointOfInterestType
from peaks_and_tracks_initializer.ingestion.points_of_interest.parking_spots import get_parking_lot_around_peak

from peaks_and_tracks_initializer.ingestion.points_of_interest.points_of_interest_utils import (
    get_point_around_peak
)


class TestPointsOfInterst(unittest.TestCase):
    def test_way_node_search(self):
        # Wildspitze
        mountain = Mountain(
            name="Wildspitze",
            id=26865139,
            height=3768,
            lat=46.8852429,
            lon=10.867279
        )
        res = get_point_around_peak(peak=mountain,
                                    way_radius=6000, way_condition="tourism=alpine_hut",
                                    point_of_interest_type=PointOfInterestType.ALPINE_HUT)

    def test_get_parking_spots_around_node(self):
        # Wildspitze
        mountain = Mountain(
            name="Wildspitze",
            id=26865139,
            height=3768,
            lat=46.8852429,
            lon=10.867279
        )
        res = get_parking_lot_around_peak(peak=mountain,
                                    radius=10000)