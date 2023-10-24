import os
import sqlite3
import streamlit as st
import time
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms import LlamaCPP
from llama_index.schema import BaseNode, Document
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt
from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
import hashlib
import pickle
from llama_index import StorageContext, load_index_from_storage

start_time = time.time()

DATA_DIR = "data"
MANUALS_DIR = "data/manuals"
GITHUB_DIR = "data/manuals/.github"
DECISION_DIR = "data/manuals/decisions"
CHANGELOG_DIR = "data/manuals/changelog"

st.title("Ask Aria")

st.markdown(
    """ 
    AI Disclaimer: Aria, the AI, generates responses based on data it has learned. These responses do not reflect any personal opinions or beliefs. All user interactions are collected and utilized to improve and educate the Aria system. By using this service, you're agreeing to license any contributions under the [MIT License](https://opensource.org/licenses/MIT). 
    
    For more details, visit our code repository on [GitHub](https://github.com/fire/fire.llama-index-streamlit). 
    
    Hello! I'm Aria, your guide and assistant in the world of V-Sekai.  
    As an assistant character, my role is to assist and inform newcomers  
    about our virtual universe. 
    
    --- 
    
    Remember, I'm always here to help you navigate through V-Sekai.  
    Let's explore this virtual world together!  
    """
)

from threading import Lock

lock = Lock()


@st.cache_data(ttl=3600)
def load_documents(paths):
    with lock:
        docs = []
        for path in paths:
            for name in os.listdir(path):
                full_path = os.path.join(path, name)
                if os.path.isfile(full_path):
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            text = f.read()
                            if len(text) == 0:
                                continue
                            docs.append(Document(text=text))
                    except UnicodeDecodeError:
                        print(f"Error decoding file: {full_path}")
        return docs


paths = [DATA_DIR, MANUALS_DIR, GITHUB_DIR, DECISION_DIR, CHANGELOG_DIR]
docs = load_documents(paths)

from InstructorEmbedding import INSTRUCTOR
model = INSTRUCTOR('hkunlp/instructor-xl')
sentence = "Virtual Reality Technology: Open-Source Software Development"
instruction = "Represent the journey and objectives of V-Sekai in the field of open-source VR technology document:"

embedModel = model.encode([[instruction, sentence]])
llmModel = LlamaCPP(
    model_url="https://huggingface.co/TheBloke/LlongOrca-13B-16K-GGUF/resolve/main/llongorca-13b-16k.Q5_K_S.gguf",
    temperature=0.1,
    max_new_tokens=1024,
    context_window=16000,
    generate_kwargs={},
    model_kwargs={"n_gpu_layers": 1000},
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    verbose=True,
)
serviceContext = ServiceContext.from_defaults(llm=llmModel, embed_model=embedModel)

storage_context = StorageContext.from_defaults(persist_dir="./storage")

def load_index_data(_storage_context, _docs, _service_context):
    try:
        indexData = load_index_from_storage(_storage_context)
    except Exception as e:
        print(f"Index data not found in storage. Generating new vectors: {e}")
        
        total_batches = len(_docs)
        for i, batch in enumerate(_docs, start=1):
            print(f"Processing batch {i} of {total_batches}")
            
            batch_index = VectorStoreIndex.from_documents(
                batch, service_context=_service_context
            )
            batch_index.storage_context.persist()
            
        indexData = load_index_from_storage(_storage_context)
    return indexData

paths = [DATA_DIR, MANUALS_DIR, GITHUB_DIR, DECISION_DIR, CHANGELOG_DIR]
docs = load_documents(paths)

batches = [docs[i:i + 5] for i in range(0, len(docs), 20)]

indexData = load_index_data(storage_context, batches, serviceContext)

queryEngine = indexData.as_query_engine()

indexData.storage_context.persist()

defaultQuery = ""

conn = sqlite3.connect("query_results.db")

c = conn.cursor()

c.execute(
    """ 
    CREATE TABLE IF NOT EXISTS results ( 
        timestamp TEXT, 
        query TEXT, 
        response TEXT, 
        time REAL, 
        PRIMARY KEY (timestamp, query) 
    ) 
"""
)

elapsed_time = time.time() - start_time

with st.form(key="my_form"):
    queryInput = st.text_input("Welcome to V-Sekai!", defaultQuery)
    submitButton = st.form_submit_button(label="Submit")

if submitButton:
    if not queryInput.strip():
        st.error(f"Please provide the search query.")
    else:
        try:
            startTime = time.time()

            responseOutput = queryEngine.query(queryInput)

            elapsedTime = time.time() - startTime

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

            responseString = str(responseOutput)

            c.execute(
                """ 
                INSERT INTO results (timestamp, query, response, time) 
                VALUES (?, ?, ?, ?) 
            """,
                (timestamp, queryInput, responseString, elapsedTime),
            )

            conn.commit()

            st.success(responseOutput)
        except Exception as e:
            import traceback

            st.error(f"An error occurred: {e}\n{traceback.format_exc()}")

if "page_number" not in st.session_state:
    st.session_state["page_number"] = 0

results_per_page = 10

start_index = st.session_state.page_number * results_per_page


def fetch_results(results_per_page, start_index):
    c.execute(
        """
        SELECT timestamp, query, response, time FROM results
        ORDER BY ROWID DESC
        LIMIT ? OFFSET ?
    """,
        (results_per_page, start_index),
    )
    return c.fetchall()


current_page_results = fetch_results(results_per_page, start_index)

current_page_results.insert(0, ("Timestamp", "Query", "Response", "System Overhead"))

# Displaying the results as a table
st.table(current_page_results)

if len(current_page_results) == results_per_page:
    if st.button("Next Page"):
        st.session_state.page_number += 1

if st.session_state.page_number > 0:
    if st.button("Previous Page"):
        st.session_state.page_number -= 1

conn.close()

st.markdown(f"Startup time: {elapsed_time} seconds")
