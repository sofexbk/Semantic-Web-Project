from sparql_client import DBPediaClient
from wikidata_client import WikidataClient
from rdf_utils import create_graph, add_triple, save_graph
from query_examples2 import QUERIES

def main():
    # Initialize clients
    dbpedia_client = DBPediaClient()
    wikidata_client = WikidataClient()

    # Example 1: Query French cities from DBpedia
    print("Querying French cities from DBpedia...")
    results = dbpedia_client.query(QUERIES['french_cities'])
    if results:
        print("\nTop 10 French cities by population:")
        for result in results:
            name = result['name']['value']
            population = result['population']['value']
            print(f"{name}: {population} habitants")
    
    # Example 2: Query French writers from DBpedia
    print("\nQuerying French writers from DBpedia...")
    results = dbpedia_client.query(QUERIES['french_writers'])
    if results:
        print("\nFrench writers:")
        for result in results:
            name = result['name']['value']
            birth = result['birth']['value']
            print(f"{name} (né(e) le {birth})")
    
    # Example 3: Query French painters from Wikidata
    print("\nQuerying French painters from Wikidata...")
    results = wikidata_client.query(QUERIES['wikidata_french_painters'])
    if results:
        print("\nFrench painters:")
        for result in results:
            name = result['painterLabel']['value']
            birth = result['birthDate']['value']
            print(f"{name} (né(e) le {birth})")
    
    # Example 4: Creating and saving a local RDF graph
    print("\nCreating local RDF graph...")
    graph = create_graph()
    
    # Adding some example data
    writer_uri = "http://example.org/writer/"
    book_uri = "http://example.org/book/"
    
    add_triple(graph, 
              f"{writer_uri}victor_hugo",
              "http://example.org/wrote",
              f"{book_uri}les_miserables")
    
    # Save the graph
    if save_graph(graph, "output.ttl"):
        print("Graph saved successfully to output.ttl")

if __name__ == "__main__":
    main()
