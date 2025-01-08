import streamlit as st
from rdflib import Graph, RDF, OWL, RDFS
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config
import io

st.set_page_config(
    page_title="Ontology Instances Viewer",
    layout="wide"
)

st.title("Ontology Instances Viewer")

# Sidebar for data source input
st.sidebar.header("Data Source")
uploaded_file = st.sidebar.file_uploader("Upload OWL file", type=['owl', 'xml'])

if 'graph' not in st.session_state:
    st.session_state.graph = None

# Load OWL data
if uploaded_file is not None:
    with st.spinner("Loading ontology data..."):
        try:
            content = uploaded_file.read().decode()
            g = Graph()
            g.parse(data=content, format='xml')
            st.session_state.graph = g
            st.success("Successfully loaded ontology!")
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")

if st.session_state.graph is not None:
    g = st.session_state.graph
    
    # Extract Classes
    classes = []
    for s in g.subjects(RDF.type, OWL.Class):
        label = g.value(s, RDFS.label)
        if label:
            classes.append({
                'URI': str(s),
                'Label': str(label)
            })
    
    # Extract Instances and their relationships
    instances = []
    instance_relations = []
    
    # Find all named individuals
    for s in g.subjects(RDF.type, OWL.NamedIndividual):
        # Get the class type
        for class_type in g.objects(s, RDF.type):
            if class_type != OWL.NamedIndividual:
                label = g.value(s, RDFS.label)
                class_label = g.value(class_type, RDFS.label)
                if label and class_label:
                    instances.append({
                        'URI': str(s),
                        'Label': str(label),
                        'Class': str(class_label)
                    })
        
        # Get relationships between individuals
        for p, o in g.predicate_objects(s):
            if p != RDF.type and g.value(o, RDF.type) == OWL.NamedIndividual:
                pred_label = g.value(p, RDFS.label)
                obj_label = g.value(o, RDFS.label)
                subj_label = label
                if pred_label and obj_label and subj_label:
                    instance_relations.append({
                        'Subject': str(subj_label),
                        'Predicate': str(pred_label),
                        'Object': str(obj_label)
                    })
    
    # Display Statistics
    st.subheader("Ontology Statistics")
    col1, col2 = st.columns(2)
    col1.metric("Classes", len(classes))
    col2.metric("Instances", len(instances))
    
    # Display Instances Table
    st.subheader("Instances")
    st.dataframe(pd.DataFrame(instances), hide_index=True, use_container_width=True)
    
    # Display Relations Table
    if instance_relations:
        st.subheader("Instance Relations")
        st.dataframe(pd.DataFrame(instance_relations), hide_index=True, use_container_width=True)
    
    # Graph Visualization
    st.subheader("Instances Graph Visualization")
    
    nodes = []
    edges = []
    unique_nodes = set()
    
    # Create color map for different classes
    class_colors = {
        "Ville": "#FF9999",  # Rouge clair
        "Stade": "#99FF99",  # Vert clair
        "AttractionTouristique": "#9999FF",  # Bleu clair
        "Hébergement": "#FFFF99",  # Jaune clair
        "Transport": "#FF99FF",  # Rose
        "Événement": "#99FFFF"   # Cyan
    }
    
    # Add instance nodes
    for instance in instances:
        node_id = instance['Label']
        if node_id not in unique_nodes:
            color = class_colors.get(instance['Class'], "#CCCCCC")  # Gris par défaut
            nodes.append(Node(id=node_id,
                            label=f"{node_id}\n({instance['Class']})",
                            size=20,
                            color=color))
            unique_nodes.add(node_id)
    
    # Add relationship edges
    for relation in instance_relations:
        edges.append(Edge(source=relation['Subject'],
                         target=relation['Object'],
                         label=relation['Predicate'],
                         color="#666666"))
    
    config = Config(
        width=1200,
        height=800,
        directed=True,
        physics=True,
        hierarchical=False,
        nodeHighlightBehavior=True,
        highlightColor="#F7A7A6",
        node={'labelProperty': 'label'},
        link={'labelProperty': 'label', 'renderLabel': True}
    )
    
    agraph(nodes=nodes, edges=edges, config=config)
