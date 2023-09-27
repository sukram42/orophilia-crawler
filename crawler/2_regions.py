
import json
from models import RegionList
from models import Region

with open("geo/regions.json", "r") as f: 
   raw_reg =  json.load(f)

regions = [*map(lambda i: {"id": i['id'], "tags": i.get('tags')}, raw_reg) ]

def convert_to_region(item):
   if item.get('tags', {}) == None: 
      return
   
   return Region(id=item['id'],
                 name=item.get('tags',{}).get("name","No Name"),
                 wikidata=item.get('tags', {}).get("wikidata"),
                 )
regions = conv_regions = [*map(convert_to_region, regions)]
regions = RegionList([*filter(lambda i: i, regions)])
print(regions)


## Upload
from supabase import create_client, Client

url: str = 'https://ntcmlxdemillsrdjybpc.supabase.co'
key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im50Y21seGRlbWlsbHNyZGp5YnBjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5MjA0MDgzMCwiZXhwIjoyMDA3NjE2ODMwfQ.yTQhbzzibLoXORx8sbdb35nl_lWRp0wxHgA3o8IoIPQ'

supabase: Client = create_client(url, key)
data = supabase.table("regions").insert(regions.model_dump()).execute()
print(data)