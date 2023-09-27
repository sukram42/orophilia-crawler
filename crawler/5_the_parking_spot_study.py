"""
Parking spots are pack animals. 
We only need one of them in a cluster. Hence, we are going to cluster them! :D 
"""
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.discriminant_analysis import StandardScaler
from supabase import create_client, Client

from overpass import OverpassClient
from models import Mountain

# mountain_id = 364134323  # Watzmann
mountain_id = 1617915343 # Mittlere ödkarspitze


url: str = "https://ntcmlxdemillsrdjybpc.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im50Y21seGRlbWlsbHNyZGp5YnBjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5MjA0MDgzMCwiZXhwIjoyMDA3NjE2ODMwfQ.yTQhbzzibLoXORx8sbdb35nl_lWRp0wxHgA3o8IoIPQ"

supabase: Client = create_client(url, key)
data = supabase.table("mountains").select("*").eq("id", mountain_id).execute()
mountain = Mountain.model_validate(data.data[0])


# Get all mountain huts near the peak
with open("query/get_parking_spots_near_mountain.query", "r", encoding="utf-8") as f:
    query = f.read()


client = OverpassClient()
res = client.query(query.format(lat=mountain.lat, lon=mountain.lon))
parking_spots = [
    *filter(lambda item: item["type"] == "way", res.json()["elements"])
]
print(parking_spots)

coords = [*map(lambda p: (p['center']['lat'], p['center']['lon']), parking_spots)]
ids = [*map(lambda p: p['id'], parking_spots)]

# Scale the data
parking_spots_radians = np.radians(coords)

# Scale the data for DBSCAN
scaler = StandardScaler().fit(parking_spots_radians)
X = scaler.transform(parking_spots_radians)

dbscan = DBSCAN(eps=0.1, min_samples=2, metric='euclidean')
dbscan.fit(X)

cluster_labels = dbscan.labels_

clusters = {}
for i, label in enumerate(cluster_labels):
    if label != -1:  # Exclude noise points (not part of any cluster)
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(parking_spots[i])


print(clusters)
for id, area in clusters.items(): 
    cluster_centers = pd.DataFrame(pd.json_normalize(area))[['center.lat', 'center.lon']]



# calculate parking_area centers:
