#%%
from typing import Dict, List
import json
import os

from pydantic import parse_obj_as

from models import Mountain

print(os.getcwd())
#%%
with open("../geo/karwendel.json") as f: 
    data = json.load(f)

#%%
print(data)
# %%

def convert_type_node(item:Dict): 
    print(item)
    if "tags" not in item: 
        return

    if item['tags'].get("natural") == "peak":
        return Mountain(name=item['tags'].get('name', "No Name Gipfel"),
                        height=item['tags'].get("ele"),
                        lat=item["lat"],
                        lon=item["lon"],
                        wikidata=item['tags'].get("wikidata"),
                        tags=item['tags']
                        )
    raise Exception("hm")

def convert_to_model(item: Dict):
    print(item)
    if "tags" not in item: 
        return

    if item['type'] == "node":
        return convert_type_node(item)
    
    print(item)
    return

# %%
m = [*filter(lambda m: m is not None, map(convert_to_model, data))]

# %%
m[:50]
# %%
# # Upload
from supabase import create_client, Client

url: str = 'https://ntcmlxdemillsrdjybpc.supabase.co'
key: str = ''

supabase: Client = create_client(url, key)
#%%
# %%
m
from pydantic import BaseModel
class MountainList(BaseModel):
    mountains: List[Mountain]

m_list=MountainList(mountains=m)
# %%
data = supabase.table("Mountains").insert(m_list.model_dump()['mountains'][:50]).execute()
print(data)
# %%

# %%
