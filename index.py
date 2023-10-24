import os
import sqlite3
import streamlit as st
import time
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
)
from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt
from llama_index.schema import Document
from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from threading import Lock

DATA_DIRS = [
    "data",
    "data/manuals",
    "data/manuals/.github",
    "data/manuals/decisions",
    "data/manuals/changelog",
]

st.title("Ask Aria")

st.markdown(
    """
AI Disclaimer: Aria, the AI, generates responses based on data it has learned. These responses do not reflect any personal opinions or beliefs. All user interactions are collected and utilized to improve and educate the Aria system. By using this service, you're agreeing to license any contributions under the [MIT License](https://opensource.org/licenses/MIT).

For more details, visit our code repository on [GitHub](https://github.com/fire/fire.llama-index-streamlit).

Hello! I'm Aria, your guide and assistant in the world of V-Sekai. 
As an assistant character, my role is to assist and inform newcomers 
about our virtual universe.

## What Can I Do?

- Guide you through the basics of V-Sekai
- Provide information about game mechanics and features
- Assist with any queries or issues you might encounter
- Keep you updated on new updates and events

---

Remember, I'm always here to help you navigate through V-Sekai. 
Let's explore this virtual world together! 
"""
)

from threading import Lock

lock = Lock()


@st.cache_resource(ttl=3600)
def load_documents_and_model(paths):
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

        embedModel = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-base-en-v1.5")
        llmModel = LlamaCPP(
            model_url="https://huggingface.co/TheBloke/LlongOrca-13B-16K-GGUF/resolve/main/llongorca-13b-16k.Q5_K_S.gguf",
            temperature=0.01,
            max_new_tokens=1024,
            context_window=14000,
            generate_kwargs={},
            model_kwargs={"n_gpu_layers": 1000},
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            verbose=False,
        )
        service_context = ServiceContext.from_defaults(llm=llmModel, embed_model=embedModel)

        return docs, service_context

docs, service_context = load_documents_and_model(DATA_DIRS)

@st.cache_resource(ttl=3600)
def load_index_data(_docs, _service_context):
    return VectorStoreIndex.from_documents(_docs, service_context=_service_context)


indexData = load_index_data(docs, service_context)

queryEngine = indexData.as_query_engine()

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

with st.form(key="my_form"):
    queryInput = st.text_input("Welcome to V-Sekai!", "")
    submitButton = st.form_submit_button(label="Submit")

if submitButton and queryInput.strip():
    startTime = time.time()
    responseOutput = queryEngine.query(queryInput)
    elapsedTime = time.time() - startTime
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    c.execute(
        """
        INSERT INTO results (timestamp, query, response, time)
        VALUES (?, ?, ?, ?)
    """,
        (timestamp, queryInput, str(responseOutput), elapsedTime),
    )
    conn.commit()
    st.success(responseOutput)

results_per_page = 10
start_index = st.session_state.get("page_number", 0) * results_per_page


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

if len(current_page_results) == results_per_page and st.button("Next Page"):
    st.session_state["page_number"] = st.session_state.get("page_number", 0) + 1

if st.session_state.get("page_number", 0) > 0 and st.button("Previous Page"):
    st.session_state["page_number"] -= 1

conn.close()
