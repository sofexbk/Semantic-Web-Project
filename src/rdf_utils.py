"""Utility functions for RDF data handling"""

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, FOAF

def create_graph():
    """Create and return a new RDF graph"""
    return Graph()

def add_triple(graph, subject, predicate, object_):
    """Add a triple to the graph"""
    graph.add((URIRef(subject), URIRef(predicate), URIRef(object_)))

def add_literal(graph, subject, predicate, literal):
    """Add a literal value to the graph"""
    graph.add((URIRef(subject), URIRef(predicate), Literal(literal)))

def save_graph(graph, file_path, format='turtle'):
    """Save the graph to a file"""
    try:
        graph.serialize(destination=file_path, format=format)
        return True
    except Exception as e:
        print(f"Error saving graph: {e}")
        return False

def load_graph(file_path, format='turtle'):
    """Load a graph from a file"""
    graph = Graph()
    try:
        graph.parse(file_path, format=format)
        return graph
    except Exception as e:
        print(f"Error loading graph: {e}")
        return None