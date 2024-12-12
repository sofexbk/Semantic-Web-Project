"""Example SPARQL queries for DBPedia"""

QUERIES = {
    'french_cities': """
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbp: <http://dbpedia.org/property/>
        
        SELECT DISTINCT ?city ?name ?population
        WHERE {
            ?city a dbo:City ;
                  dbo:country <http://dbpedia.org/resource/France> ;
                  rdfs:label ?name ;
                  dbo:populationTotal ?population .
            FILTER(LANG(?name) = "fr")
        }
        ORDER BY DESC(?population)
        LIMIT 10
    """,
    
    'french_writers': """
        PREFIX dbo: <http://dbpedia.org/ontology/>
        
        SELECT DISTINCT ?writer ?name ?birth
        WHERE {
            ?writer a dbo:Writer ;
                    dbo:birthPlace/dbo:country <http://dbpedia.org/resource/France> ;
                    rdfs:label ?name ;
                    dbo:birthDate ?birth .
            FILTER(LANG(?name) = "fr")
        }
        ORDER BY ?birth
        LIMIT 10
    """
}