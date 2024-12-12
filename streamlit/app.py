import streamlit as st
import rdflib
from rdflib import Graph
import pandas as pd

st.set_page_config(
    page_title="RDF Knowledge Base Explorer",
    layout="wide"
)

st.title("RDF Knowledge Base Explorer")

st.sidebar.header("Data Source")
url = st.sidebar.text_input(
    "Enter RDF Resource URL",
    value="http://dbpedia.org/resource/Car",
    help="Enter the URL of an RDF resource to explore"
)

if 'graph' not in st.session_state:
    st.session_state.graph = None

if st.sidebar.button("Load Data"):
    with st.spinner("Loading RDF data..."):
        try:
            g = Graph()
            g.parse(url)
            st.session_state.graph = g
            st.success(f"Successfully loaded {len(g)} triples!")
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")

if st.session_state.graph is not None:
    triples = []
    for s, p, o in st.session_state.graph:
        triples.append({
            'Subject': str(s),
            'Predicate': str(p),
            'Object': str(o)
        })
    
    df = pd.DataFrame(triples)
    
    st.subheader("Filter Data")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        subject_filter = st.text_input("Filter by Subject")
    with col2:
        predicate_filter = st.text_input("Filter by Predicate")
    with col3:
        object_filter = st.text_input("Filter by Object")
    
    filtered_df = df.copy()
    if subject_filter:
        filtered_df = filtered_df[filtered_df['Subject'].str.contains(subject_filter, case=False, na=False)]
    if predicate_filter:
        filtered_df = filtered_df[filtered_df['Predicate'].str.contains(predicate_filter, case=False, na=False)]
    if object_filter:
        filtered_df = filtered_df[filtered_df['Object'].str.contains(object_filter, case=False, na=False)]
    
    st.subheader("Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Triples", len(df))
    col2.metric("Unique Subjects", len(df['Subject'].unique()))
    col3.metric("Unique Predicates", len(df['Predicate'].unique()))
    
    st.subheader("RDF Triples")
    st.dataframe(
        filtered_df,
        hide_index=True,
        use_container_width=True
    )
    
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="rdf_data.csv",
        mime="text/csv"
    )
    
