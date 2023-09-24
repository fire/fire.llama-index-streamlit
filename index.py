import os
import sqlite3
import streamlit as st
import time
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt
from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings

st.title("Ask Aria")

embedModel = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-base-en")
llmModel = LlamaCPP(
    model_url="https://huggingface.co/s3nh/teknium-OpenHermes-13B-GGUF/resolve/main/teknium-OpenHermes-13B.Q5_K_S.gguf",
    temperature=0.1,
    max_new_tokens=256,
    context_window=3900,
    generate_kwargs={},
    model_kwargs={"n_gpu_layers": 1000},
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    verbose=True,
)

documentsData = SimpleDirectoryReader("data").load_data()
serviceContext = ServiceContext.from_defaults(llm=llmModel, embed_model=embedModel)
indexData = VectorStoreIndex.from_documents(documentsData, service_context=serviceContext)

queryEngine = indexData.as_query_engine()

defaultQuery = ""

conn = sqlite3.connect('query_results.db')

c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS results (
        timestamp TEXT,
        query TEXT,
        response TEXT,
        time REAL,
        PRIMARY KEY (timestamp, query)
    )
''')

with st.form(key='my_form'):
    queryInput = st.text_input("What would you like to ask? (source: data/avatar-presentation-preflight-check.md)", defaultQuery)
    submitButton = st.form_submit_button(label='Submit')

if submitButton:
    if not queryInput.strip():
        st.error(f"Please provide the search query.")
    else:
        try:
            startTime = time.time()

            responseOutput = queryEngine.query(queryInput) 

            elapsedTime = time.time() - startTime
            
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
            
            responseString = str(responseOutput)
            
            c.execute('''
                INSERT INTO results (timestamp, query, response, time)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, queryInput, responseString, elapsedTime))

            conn.commit()
            
            st.success(responseOutput)
        except Exception as e:
            import traceback
            st.error(f"An error occurred: {e}\n{traceback.format_exc()}")

c.execute('''
    SELECT * FROM results
    ORDER BY ROWID DESC
    LIMIT 10
''')
last10QueriesResults = c.fetchall()

st.table(last10QueriesResults)

conn.close()
