from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Endpoint DBpedia
DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"

def execute_sparql(query):
    headers = {"Accept": "application/sparql-results+json"}
    response = requests.get(DBPEDIA_ENDPOINT, params={"query": query}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        sparql_query = request.form['sparql_query']
        results = execute_sparql(sparql_query)
        return render_template('results.html', results=results)
    return render_template('query.html')

@app.route('/graph', methods=['GET'])
def graph():
    query = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    SELECT DISTINCT ?city ?name ?population
    WHERE {
        ?city a dbo:City ;
              dbo:country <http://dbpedia.org/resource/France> ;
              rdfs:label ?name ;
              dbo:populationTotal ?population .
        FILTER(LANG(?name) = "fr")
    }
    LIMIT 50
    """
    results = execute_sparql(query)
    return render_template('graph.html', results=results)

@app.route('/api/graph-data', methods=['GET'])
def graph_data():
    query = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    SELECT DISTINCT ?city ?name ?population
    WHERE {
        ?city a dbo:City ;
              dbo:country <http://dbpedia.org/resource/France> ;
              rdfs:label ?name ;
              dbo:populationTotal ?population .
        FILTER(LANG(?name) = "fr")
    }
    LIMIT 10
    """
    results = execute_sparql(query)
    if "error" in results:
        return jsonify({"error": results["error"]}), 500
    nodes = []
    links = []
    for result in results["results"]["bindings"]:
        city = result["city"]["value"]
        name = result["name"]["value"]
        population = int(result["population"]["value"])
        nodes.append({"id": city, "name": name, "population": population})
    return jsonify({"nodes": nodes, "links": links})

if __name__ == "__main__":
    app.run(debug=True)
