QUERIES = {
    'french_cities': """
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT DISTINCT ?city ?name ?population
        WHERE {
            ...
        }
    """,
    'french_writers': """
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT DISTINCT ?writer ?name ?birth
        WHERE {
            ...
        }
    """,
    'wikidata_french_painters': """
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX bd: <http://www.bigdata.com/rdf#>

    SELECT ?painter ?painterLabel ?birthDate
    WHERE {
        ?painter wdt:P31 wd:Q5 ;  # Instance de : Humain
                 wdt:P106 wd:Q1028181 ;  # Profession : Peintre
                 wdt:P27 wd:Q142 ;  # Nationalité : Française
                 wdt:P569 ?birthDate .  # Date de naissance
        SERVICE wikibase:label { bd:serviceParam wikibase:language "fr,en". }
    }
    ORDER BY ?birthDate
    LIMIT 10
"""

}
