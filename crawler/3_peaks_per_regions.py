import hashlib
import requests
from tqdm import tqdm
from models import Region


list_of_areas = [
    # Region(id=2110290, name='Watzmannstock'),
    # Region(id=2111133, name="Hochkalterstock"),
    # Region(id=2114147, name="Karwendel"),
    # Region(id=2131102, name="Mieminger Kette"),
    # Region(id=2129656, name="Hohe Tauern"),
    # Region(id=2127947, name="Ötztaler Alpen"),
    Region(id=2121875, name="Chiemgauer Alpen")

]

with open("query/peak_in_region.query", "r", encoding="utf-8") as f:
    template = f.read()


from overpass import OverpassClient
from models import Mountain, MountainList

client = OverpassClient()


def extract_mountains(region: Region):
    # res = client.query(template.format(region=list_of_areas[0]))
    res = client.query(template.format(region=region.name))

    def is_mountain(item: dict) -> bool:
        if "tags" not in item:
            return False

        if "natural" not in item["tags"]:
            return False

        return item["tags"]["natural"] == "peak"

    def get_image_url(item):
        wikitag = item.get("tags", {}).get("wikidata")
        if wikitag is None:
            return

        # call wikidata api
        url = f"https://www.wikidata.org/w/api.php?action=wbgetclaims&property=P18&entity={wikitag}&format=json"
        response = requests.get(url)
        data = response.json()

        print(response)

        filename = data.get("claims", {}).get("P18", [])

        if len(filename) == 0:
            return

        filename = filename[0].get("mainsnak", {}).get("datavalue", {}).get("value")

        if filename is None:
            return

        filename_spaced = filename.replace(" ", "_")

        hash = hashlib.md5(filename_spaced.encode("utf-8")).hexdigest()

        image_url = f"https://upload.wikimedia.org/wikipedia/commons/{hash[:1]}/{hash[:2]}/{filename_spaced}"
        return image_url

    def conversion_method(region: Region):
        def convert_to_mountain(item: dict) -> dict:
            height = item["tags"].get("ele")
            return Mountain(
                id=item["id"],
                name=item["tags"].get("name", "No Name Gipfel"),
                height=int(float(height)) if height else None,
                lat=item["lat"],
                lon=item["lon"],
                wikidata=item["tags"].get("wikidata"),
                tags=item["tags"],
                region=region.id,
                wikiimage_url=get_image_url(item),
            )

        return convert_to_mountain

    mountains = MountainList(
        [
            *map(
                conversion_method(region=region),
                filter(is_mountain, res.json()["elements"]),
            )
        ]
    )

    # Update to table mountains

    ## Upload
    from supabase import create_client, Client

    url: str = "https://ntcmlxdemillsrdjybpc.supabase.co"
    key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im50Y21seGRlbWlsbHNyZGp5YnBjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5MjA0MDgzMCwiZXhwIjoyMDA3NjE2ODMwfQ.yTQhbzzibLoXORx8sbdb35nl_lWRp0wxHgA3o8IoIPQ"

    print(f"Adding {len(mountains.model_dump())} mountains")
    supabase: Client = create_client(url, key)
    data = (
        supabase.table("mountains")
        .insert(mountains.model_dump(), upsert=True)
        .execute()
    )


for reg in tqdm(list_of_areas):
    print("Extract region ", reg)
    extract_mountains(reg)
