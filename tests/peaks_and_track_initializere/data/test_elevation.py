

import unittest
from crawler.models import Point

from peaks_and_tracks_initializer.data.elevation import OpenElevationElevationFetcher


class TestElevationFetcher(unittest.TestCase):
    def test_get_elevation_for_open_elevation(self):
        el = OpenElevationElevationFetcher()
        a = el.get_elevation([
            Point(lat=46.8852429, lon=10.867279)])
