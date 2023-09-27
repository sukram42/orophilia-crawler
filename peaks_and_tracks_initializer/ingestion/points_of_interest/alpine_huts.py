
from typing import List
from crawler.models import Mountain, Point, PointOfInterest, PointOfInterestType
from peaks_and_tracks_initializer.ingestion.points_of_interest.points_of_interest_utils import get_point_around_peak


def get_alpine_huts_around_peak(peak: Mountain, radius: int)->List[PointOfInterest]:
    """Get a list of alpine huts near a point

    Parameters
    ----------
    point : Point
        the point to search from. E.g Peak
    radius : int
        The radius in *meters*
    """
    return get_point_around_peak(peak=peak,
                                way_radius=radius, way_condition="tourism=alpine_hut",
                                point_of_interest_type=PointOfInterestType.ALPINE_HUT)