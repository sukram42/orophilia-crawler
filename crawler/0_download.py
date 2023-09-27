
from tqdm import tqdm
from overpass import OverpassClient
import json

client = OverpassClient()

def crawl(name: str):
    res = client.file_query(f"query/{name}.query")
    with open(f"geo/{name}.json", "w", encoding="utf-8") as out:    
        json.dump(res.json()['elements'], out)


queries = [
    # "karwendel",
    "regions"
]
for q in tqdm(queries):
    crawl(q)