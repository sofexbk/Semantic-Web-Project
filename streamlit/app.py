import streamlit as st
from rdflib import Graph, RDF, OWL, RDFS, Namespace
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config
import io

st.set_page_config(
    page_title="Ontology Explorer",
    layout="wide"
)

st.title("Ontology Explorer")

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
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Instances View", "SPARQL Query", "Example Queries"])
    
    with tab1:
        # Original instances visualization code
        instances = []
        instance_relations = []
        
        for s in g.subjects(RDF.type, OWL.NamedIndividual):
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
        st.subheader("Statistics")
        col1, col2 = st.columns(2)
        col1.metric("Total Instances", len(instances))
        col2.metric("Total Relations", len(instance_relations))
        
        # Display Instances Table
        st.subheader("Instances")
        st.dataframe(pd.DataFrame(instances), hide_index=True, use_container_width=True)
        
        # Graph Visualization
        st.subheader("Instances Graph")
        
        nodes = []
        edges = []
        unique_nodes = set()
        
        class_colors = {
            "Ville": "#FF9999",
            "Stade": "#99FF99",
            "AttractionTouristique": "#9999FF",
            "Hébergement": "#FFFF99",
            "Transport": "#FF99FF",
            "Événement": "#99FFFF"
        }
        
        for instance in instances:
            node_id = instance['Label']
            if node_id not in unique_nodes:
                color = class_colors.get(instance['Class'], "#CCCCCC")
                nodes.append(Node(id=node_id,
                                label=f"{node_id}\n({instance['Class']})",
                                size=20,
                                color=color))
                unique_nodes.add(node_id)
        
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
    
    with tab2:
        st.subheader("SPARQL Query")
        
        # Query input
        query = st.text_area(
            "Enter your SPARQL query:",
            height=200,
            help="Write your SPARQL query here. Use the example queries tab for inspiration."
        )
        
        # Execute query button
        if st.button("Execute Query"):
            if query:
                try:
                    # Execute the query
                    results = g.query(query)
                    
                    # Convert results to dataframe
                    results_list = []
                    for row in results:
                        row_dict = {}
                        for i, var in enumerate(results.vars):
                            # Get the value, try to get label if it's a URI
                            value = row[i]
                            if value:
                                label = g.value(value, RDFS.label)
                                row_dict[var] = str(label) if label else str(value)
                        results_list.append(row_dict)
                    
                    if results_list:
                        st.success("Query executed successfully!")
                        st.dataframe(
                            pd.DataFrame(results_list),
                            hide_index=True,
                            use_container_width=True
                        )
                    else:
                        st.info("Query executed successfully, but no results were found.")
                except Exception as e:
                    st.error(f"Error executing query: {str(e)}")
            else:
                st.warning("Please enter a query before executing.")
    
    with tab3:
        st.subheader("Example SPARQL Queries")
        st.markdown("""
        Here are some example queries you can try:
        
        **1. List all cities and their populations:**
        ```sparql
        SELECT ?ville ?population
        WHERE {
            ?v a <http://webprotege.stanford.edu/R9h67ZnQqOxO6u446tnEMDh> ;
               rdfs:label ?ville ;
               <http://webprotege.stanford.edu/RCIMFNeR0YUWwMyKiObI6VW> ?population .
        }
        ```
        
        **2. Find all stades and their capacities:**
        ```sparql
        SELECT ?stade ?capacite
        WHERE {
            ?s a <http://webprotege.stanford.edu/RCbA0jAo4MLJXgvYVF95Akb> ;
               rdfs:label ?stade ;
               <http://webprotege.stanford.edu/RBnT186BtLqpqphpwD3Qs3> ?capacite .
        }
        ```
        
        **3. List all hébergements and their prices:**
        ```sparql
        SELECT ?hebergement ?prix ?type
        WHERE {
            ?h a <http://webprotege.stanford.edu/R7UJIN6NT7Tapc9in4gdw6E> ;
               rdfs:label ?hebergement ;
               <http://webprotege.stanford.edu/RBLvwa7K7mgwopazKTT7uOT> ?prix ;
               <http://webprotege.stanford.edu/RBTLZWixsW632PLJIC1aVqJ> ?type .
        }
        ```
        
        **4. Find attractions touristiques in a specific city:**
        ```sparql
        SELECT ?attraction ?ville
        WHERE {
            ?a a <http://webprotege.stanford.edu/RBjhUA7K8VEm6GyfKJVmLIO> ;
               rdfs:label ?attraction ;
               <http://webprotege.stanford.edu/R84NeQba9tLBd852QSrWlye> ?v .
            ?v rdfs:label ?ville .
        }
        ```
        
        **5. List all events and their locations:**
        ```sparql
        SELECT ?evenement ?lieu
        WHERE {
            ?e a <http://webprotege.stanford.edu/RDq7poxU1HSynXoSByFBzrV> ;
               rdfs:label ?evenement ;
               <http://webprotege.stanford.edu/RCP83CjVkvaeqYSg7vFhxec> ?l .
            ?l rdfs:label ?lieu .
        }
        ```
        """)
