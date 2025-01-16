import streamlit as st
from rdflib import Graph, RDF, OWL, RDFS, Namespace, URIRef
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config
import io

st.set_page_config(
    page_title="E-commerce Ontology Explorer",
    layout="wide"
)

st.title("E-commerce Ontology Explorer")

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
    tab1, tab2, tab3, tab4 = st.tabs(["Entity View", "Classes & Properties", "SPARQL Query", "Example Queries"])
    
    with tab1:
        # Get class hierarchy and relationships
        classes = {}
        class_relations = []
        instances = {}
        instance_relations = []
        
        # Get all classes and their labels
        for s, p, o in g.triples((None, RDF.type, OWL.Class)):
            label = g.value(s, RDFS.label)
            if label:
                classes[str(s)] = str(label)
        
        # Get all instances and their classes
        for s, p, o in g.triples((None, RDF.type, None)):
            if isinstance(o, URIRef) and str(o) in classes:
                label = g.value(s, RDFS.label)
                if label:
                    instances[str(s)] = {
                        'uri': str(s),
                        'label': str(label),
                        'class': classes[str(o)]
                    }
        
        # Get object properties between classes
        for s, p, o in g.triples((None, RDFS.domain, None)):
            if str(o) in classes and g.value(s, RDF.type) == OWL.ObjectProperty:
                pred_label = g.value(s, RDFS.label)
                range_class = g.value(s, RDFS.range)
                if pred_label and range_class and str(range_class) in classes:
                    class_relations.append({
                        'source': classes[str(o)],
                        'predicate': str(pred_label),
                        'target': classes[str(range_class)]
                    })
        
        # Get relationships between instances
        for s, p, o in g.triples((None, None, None)):
            if (isinstance(s, URIRef) and isinstance(o, URIRef) and 
                str(s) in instances and str(o) in instances and 
                p not in [RDF.type, RDFS.label]):
                pred_label = g.value(p, RDFS.label)
                if pred_label:
                    instance_relations.append({
                        'source': instances[str(s)]['label'],
                        'predicate': str(pred_label),
                        'target': instances[str(o)]['label']
                    })
        
        # Display Statistics
        st.subheader("Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Classes", len(classes))
        with col2:
            st.metric("Total Instances", len(instances))
        with col3:
            st.metric("Total Relations", len(class_relations) + len(instance_relations))
        
        # Graph Visualization
        st.subheader("Class and Instance Graph")
        
        nodes = []
        edges = []
        unique_nodes = set()
        
        # Color scheme
        class_colors = {
            "Product": "#FF9999",
            "User": "#99FF99",
            "Order": "#9999FF",
            "OrderDetail": "#FFFF99",
            "Payment": "#FF99FF",
            "Review": "#99FFFF",
            "Category": "#CCCCCC"
        }
        
        # Add class nodes
        for class_uri, class_label in classes.items():
            if class_label not in unique_nodes:
                nodes.append(Node(
                    id=f"class_{class_label}",
                    label=class_label,
                    size=30,
                    color="#FFD700",
                    shape="diamond"
                ))
                unique_nodes.add(class_label)
        
        # Add instance nodes
        for instance in instances.values():
            if instance['label'] not in unique_nodes:
                color = class_colors.get(instance['class'], "#CCCCCC")
                nodes.append(Node(
                    id=instance['label'],
                    label=f"{instance['label']}\n({instance['class']})",
                    size=20,
                    color=color
                ))
                unique_nodes.add(instance['label'])
        
        # Add class relationships
        for relation in class_relations:
            edges.append(Edge(
                source=f"class_{relation['source']}",
                target=f"class_{relation['target']}",
                label=relation['predicate'],
                color="#FF4500",
                type="CURVE_SMOOTH"
            ))
        
        # Add instance relationships
        for relation in instance_relations:
            edges.append(Edge(
                source=relation['source'],
                target=relation['target'],
                label=relation['predicate'],
                color="#666666",
                type="CURVE_SMOOTH"
            ))
        
        # Add instance-of relationships
        for instance in instances.values():
            edges.append(Edge(
                source=instance['label'],
                target=f"class_{instance['class']}",
                label="instanceOf",
                color="#32CD32",
                type="CURVE_SMOOTH"
            ))
        
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
        st.subheader("Classes and Properties Overview")
        
        # Classes section
        st.markdown("### Classes")
        class_data = []
        for s, p, o in g.triples((None, RDF.type, OWL.Class)):
            label = g.value(s, RDFS.label)
            comment = g.value(s, RDFS.comment)
            if label:
                class_data.append({
                    'URI': str(s),
                    'Label': str(label),
                    'Comment': str(comment) if comment else ''
                })
        
        if class_data:
            st.dataframe(pd.DataFrame(class_data))
        else:
            st.info("No classes found in the ontology")
        
        # Properties section
        st.markdown("### Object Properties")
        obj_prop_data = []
        for s, p, o in g.triples((None, RDF.type, OWL.ObjectProperty)):
            label = g.value(s, RDFS.label)
            comment = g.value(s, RDFS.comment)
            domain = g.value(s, RDFS.domain)
            range_ = g.value(s, RDFS.range)
            
            domain_label = g.value(domain, RDFS.label) if domain else None
            range_label = g.value(range_, RDFS.range) if range_ else None
            
            if label:
                obj_prop_data.append({
                    'URI': str(s),
                    'Label': str(label),
                    'Domain': str(domain_label) if domain_label else str(domain),
                    'Range': str(range_label) if range_label else str(range_),
                    'Comment': str(comment) if comment else ''
                })
        
        if obj_prop_data:
            st.dataframe(pd.DataFrame(obj_prop_data))
        else:
            st.info("No object properties found in the ontology")
        
        st.markdown("### Data Properties")
        data_prop_data = []
        for s, p, o in g.triples((None, RDF.type, OWL.DatatypeProperty)):
            label = g.value(s, RDFS.label)
            comment = g.value(s, RDFS.comment)
            domain = g.value(s, RDFS.domain)
            range_ = g.value(s, RDFS.range)
            
            domain_label = g.value(domain, RDFS.label) if domain else None
            
            if label:
                data_prop_data.append({
                    'URI': str(s),
                    'Label': str(label),
                    'Domain': str(domain_label) if domain_label else str(domain),
                    'Range': str(range_),
                    'Comment': str(comment) if comment else ''
                })
        
        if data_prop_data:
            st.dataframe(pd.DataFrame(data_prop_data))
        else:
            st.info("No data properties found in the ontology")

    with tab3:
        st.subheader("SPARQL Query")
        query = st.text_area("Enter your SPARQL query:", height=200)
        if st.button("Execute Query"):
            if query:
                try:
                    results = g.query(query)
                    results_list = []
                    for row in results:
                        row_dict = {}
                        for i, var in enumerate(results.vars):
                            value = row[i]
                            if value:
                                label = g.value(value, RDFS.label)
                                row_dict[var] = str(label) if label else str(value)
                        results_list.append(row_dict)
                    
                    if results_list:
                        st.success("Query executed successfully!")
                        st.dataframe(pd.DataFrame(results_list))
                    else:
                        st.info("Query executed successfully, but no results were found.")
                except Exception as e:
                    st.error(f"Error executing query: {str(e)}")
            else:
                st.warning("Please enter a query before executing.")
    
    with tab4:
        st.subheader("Example SPARQL Queries")
        st.markdown("""
        Here are some example queries you can try:
        
        **1. List all products and their prices:**
        ```sparql
        SELECT ?product ?price
        WHERE {
            ?p a <http://webprotege.stanford.edu/R8JN9OAQRp5oI4RTqxxD5w8> ;
               rdfs:label ?product ;
               <http://webprotege.stanford.edu/RX1EIoIlDlnw04HOLQvOn5> ?price .
        }
        ```
        
        **2. Find all orders and their status:**
        ```sparql
        SELECT ?order ?status
        WHERE {
            ?o a <http://webprotege.stanford.edu/R7ov25FBIgKeXhWYXPEj1Ek> ;
               rdfs:label ?order ;
               <http://webprotege.stanford.edu/RK7sV7gFzu0dZNM607ho1y> ?status .
        }
        ```
        
        **3. List all users and their roles:**
        ```sparql
        SELECT ?user ?email ?role
        WHERE {
            ?u a <http://webprotege.stanford.edu/RCDV3qJJ1DAbDbX7qBz5jUi> ;
               rdfs:label ?user ;
               <http://webprotege.stanford.edu/RDWXxGjYsCGV4ZCWkZKCYlt> ?email ;
               <http://webprotege.stanford.edu/RDm6E5QkiPPy7MSp1lmUjkn> ?role .
        }
        ```
        
        **4. Find all product reviews and ratings:**
        ```sparql
        SELECT ?product ?rating ?comment
        WHERE {
            ?r a <http://webprotege.stanford.edu/R7f02opMCTF0ty77OqhVpMY> ;
               <http://webprotege.stanford.edu/RDYnxwoVn6L224Ck4eZvlI2> ?p ;
               <http://webprotege.stanford.edu/RMn347iR5qdPSx9qM5WxEf> ?rating ;
               <http://webprotege.stanford.edu/RBwIrRJM9TFRo7rB20yeiYH> ?comment .
            ?p rdfs:label ?product .
        }
        ```
        
        **5. List all payments and their methods:**
        ```sparql
        SELECT ?payment ?method ?amount ?date
        WHERE {
            ?p a <http://webprotege.stanford.edu/RDonsgcbIVN6ZlHAMZjsYzQ> ;
               rdfs:label ?payment ;
               <http://webprotege.stanford.edu/R7w5EqCThkGttfTtndrTgRl> ?method ;
               <http://webprotege.stanford.edu/RDM3I85VLUM29EMGRlmypWI> ?amount ;
               <http://webprotege.stanford.edu/RDNfrR7G7Dx04C2I8EJlXAc> ?date .
        }
        ```
        """)
