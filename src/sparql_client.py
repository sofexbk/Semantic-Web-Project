"""SPARQL client for querying DBPedia"""

from SPARQLWrapper import SPARQLWrapper, JSON
from config import DBPEDIA_ENDPOINT, DEFAULT_FORMAT, TIMEOUT

class DBPediaClient:
    def __init__(self):
        self.sparql = SPARQLWrapper(DBPEDIA_ENDPOINT)
        self.sparql.setReturnFormat(JSON)
        self.sparql.setTimeout(TIMEOUT)
    
    def query(self, query_string):
        """Execute a SPARQL query and return results"""
        self.sparql.setQuery(query_string)
        try:
            results = self.sparql.query().convert()
            return results['results']['bindings']
        except Exception as e:
            print(f"Error executing query: {e}")
            return None