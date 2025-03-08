
from supabase import create_client, Client

from crawler.models import Mountain

url: str = 'https://ntcmlxdemillsrdjybpc.supabase.co'
key: str = ''

supabase: Client = create_client(url, key)


data = supabase.table("Mountains").select("*").execute()
# Assert we pulled real data.
assert len(data.data) > 0
print(data)

a = Mountain(name="Testmountain", height=10)
print(a)
data = supabase.table("Mountains").insert(a.model_dump()).execute()
print(data)

