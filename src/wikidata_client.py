import requests

class WikidataClient:
    def __init__(self, endpoint="https://query.wikidata.org/sparql"):
        self.endpoint = endpoint

    def query(self, sparql_query):
        headers = {"Accept": "application/sparql-results+json"}
        response = requests.get(self.endpoint, params={"query": sparql_query}, headers=headers)

        if response.status_code == 200:
            return response.json()["results"]["bindings"]
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
