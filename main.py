# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 10:24:38 2024

@author: Hizbullah Jadoon
"""
!sudo apt install python3
import streamlit as st
import chromadb
import pandas as pd

# Initialize the ChromaDB Persistent Client
client = chromadb.PersistentClient(path="./chroma_persist")  # Path to your persistent storage
collection = client.get_collection("icd_codes_collection")  # Load the existing collection

# Streamlit App Title
st.title("ICD Code Lookup")

# Option to choose search type: by ICD code or by description
search_type = st.radio("Search by", ("ICD Code", "Description"))

# If the user chooses to search by ICD Code
if search_type == "ICD Code":
    # Input field for ICD Code
    icd_code = st.text_input("Enter ICD Code")

    # When the user submits the ICD code
    if st.button("Search by ICD Code"):
        if icd_code:
            # Query ChromaDB to get the description
            result = collection.get(ids=[icd_code])
            if result['documents']:
                st.success(f"ICD Code: {icd_code}\nDescription: {result['documents'][0]}")
            else:
                st.error("ICD Code not found.")

# If the user chooses to search by Description
if search_type == "Description":
    # Input field for Description
    description = st.text_area("Enter description (or part of it)")

    # When the user submits the description
    if st.button("Search by Description"):
        if description:
            # Query ChromaDB to get the most relevant ICD code
            results = collection.query(query_texts=[description], n_results=1)
            if results['documents']:
                st.success(f"Most relevant ICD Code: {results['ids'][0]}\nDescription: {results['documents'][0]}")
            else:
                st.error("No matching ICD code found.")
