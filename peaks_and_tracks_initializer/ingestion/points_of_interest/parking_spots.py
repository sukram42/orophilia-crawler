

from typing import Dict, List

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.discriminant_analysis import StandardScaler
from crawler.models import Mountain, PointOfInterest, PointOfInterestType
from peaks_and_tracks_initializer.ingestion.points_of_interest.points_of_interest_utils import get_point_around_peak


def get_parking_lot_around_peak(peak: Mountain, radius: int)->List[PointOfInterest]:
    """Get a list of alpine huts near a point

    Parameters
    ----------
    point : Point
        the point to search from. E.g Peak
    radius : int
        The radius in *meters*
    """
    parking_lots=get_point_around_peak(peak=peak,
                                way_radius=radius,
                                way_condition="amenity=parking",
                                point_of_interest_type=PointOfInterestType.PARKING_LOT)
    
    coordinates = map(lambda p: (p.lat, p.lon), parking_lots)

    # Convert to radians
    parking_lot_radians = np.radians([*coordinates])

    # Scale the data 
    scaler = StandardScaler().fit(parking_lot_radians)
    X = scaler.transform(parking_lot_radians)

    # Cluster
    dbscan = DBSCAN(eps=0.1, min_samples=2, metric='euclidean')
    dbscan.fit(X)

    cluster_labels = dbscan.labels_
    clusters = {}
    for i, label in enumerate(cluster_labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(parking_lots[i])

    return calculate_new_points_of_interest_for_cluster(clusters)

def calculate_new_points_of_interest_for_cluster(clusters: Dict[int, PointOfInterest]):
    result = [] 
    for cluster, lot in clusters.items():
        # calculate mean of lots
        if cluster != -1: 
            result.append(PointOfInterest(
                id=sum(int(l.id)*10 for l in lot)//len(lot), # making deterministic ids
                lat=sum([l.lat for l in lot])/len(lot),
                lon = sum([l.lon for l in lot])/len(lot),
                type=PointOfInterestType.PARKING_LOT,
                name="Cumulative Parking Area",
                tags={
                    "parking_lots": [l.model_dump_json() for l in lot]
                }
            ))
            continue

        # If its -1 then add all
        result.extend(lot)        
    
    return result
