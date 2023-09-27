

import requests


class OverpassClient():
    timeout = 25  # second
    endpoint: str
    headers = {"Accept-Charset": "utf-8;q=0.7,*;q=0.7"}
    debug = False
    proxies = None


    def __init__(self, endpoint: str = "https://overpass-api.de/api/interpreter"):
        self.endpoint = endpoint


    def query(self, query: str):
        try: 
            r = requests.post(
                url=self.endpoint,
                data={"data": query},
                timeout=self.timeout,
                proxies=self.proxies,
                headers=self.headers,   
            )

        except requests.exceptions.Timeout:
            raise TimeoutError(self._timeout)

        return r
    
    def file_query(self, file):
        with open(file, "r", encoding="utf-8") as q:
            query = q.read()
        return self.query(query=query)
