

import unittest
from crawler.models import Mountain, PointOfInterest, PointOfInterestType
from peaks_and_tracks_initializer.ingestion.points_of_interest.points_of_interest_utils import get_point_around_peak

from peaks_and_tracks_initializer.ingestion.routes.routes import get_route_from_point_of_interest_to_peak


class TestRoutes(unittest.TestCase):
    def test_get_route_from_point_of_interest(self):
        
        mountain = Mountain(
            name="Wildspitze",
            id=26865139,
            height=3768,
            lat=46.8852429,
            lon=10.867279
        )
        poi = PointOfInterest.model_validate_json('{"id":86299919,"name":"Breslauer Hütte","lat":46.8681837,"lon":10.8793002,"type":1,"tags":{"addr:city":"Sölden","addr:country":"AT","addr:housename":"Breslauer Hütte","addr:housenumber":"401","addr:place":"Hütten Vent","addr:postcode":"6458","at_bev:addr_date":"2022-10-01","building":"yes","cuisine":"jause;alpine_hut","ele":"2844","image":"http://www.flickr.com/photos/yumekosan/8157032164/","name":"Breslauer Hütte","operator":"DAV Sektion Breslau","phone":"+43 676 96 345 96","ref:refuges.info":"5470","smoking":"no","source":"geoimage.at","tourism":"alpine_hut","website":"http://www.dav-sektion-breslau.de/","wheelchair":"no","wikidata":"Q873992","wikipedia":"de:Breslauer Hütte"}}')

        
        route, waypoints = get_route_from_point_of_interest_to_peak(point=poi, peak=mountain)

        print(route, waypoints)