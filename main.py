# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 10:24:38 2024

@author: Hizbullah Jadoon
"""

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import chromadb
import pandas as pd
import os
import gc
'''
# Step 1: Initialize the PersistentClient and specify a directory for storing the data
client = chromadb.PersistentClient(path="./chroma_persist")  # Specify your directory
collection = client.create_collection("icd_codes_collection")

file_path = os.path.join(os.path.dirname(__file__), 'cleaned_icd_codes.csv')
df = pd.read_csv(file_path)

# Step 3: Load your CSV file containing ICD codes and descriptions
#df = pd.read_csv("cleaned_icd_codes.csv")

# Assuming last_index is known or retrieved from somewhere
last_index = 0  # Set this to the last processed index
stop_index = 200  # Define where to stop processing
batch_size = 50  # Process in batches of 100 rows

# Step 4: Add ICD codes and descriptions to the collection in batches
#for start_idx in range(last_index, min(stop_index, len(df)), batch_size):
for start_idx in range(last_index,len(df), batch_size):

    # Get the current batch of rows
    batch = df.iloc[start_idx:start_idx + batch_size]

    # Add the ICD codes and descriptions to ChromaDB
    collection.add(
        documents=batch['Description'].tolist(),  # Add descriptions as documents
        ids=batch['Code'].tolist()  # Use ICD codes as IDs
    )

    # Print progress
    print(f"Processed batch {start_idx} to {start_idx + len(batch) - 1}")

    # Memory management: clear the batch and force garbage collection
    del batch
    gc.collect()

# Final print statement once done
print(f"Processed up to index Exiting.")

print("ICD codes have been added to the persistent collection successfully!")
'''
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
