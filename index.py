import os
import sqlite3
import streamlit as st
import time
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt
from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings

st.title("Ask Aria")

st.markdown("""
AI Disclaimer: Aria, the AI, generates responses based on data it has learned. These responses do not reflect any personal opinions or beliefs. All user interactions are collected and utilized to improve and educate the Aria system. By using this service, you're agreeing to license any contributions under the [MIT License](https://opensource.org/licenses/MIT).

For more details, visit our code repository on [GitHub](https://github.com/fire/fire.llama-index-streamlit).
""")


@st.cache_resource
def load_data_and_models():
    embedModel = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-base-en")
    llmModel = LlamaCPP(
        model_url="https://huggingface.co/s3nh/teknium-OpenHermes-13B-GGUF/resolve/main/teknium-OpenHermes-13B.Q5_K_S.gguf",
        temperature=0.1,
        max_new_tokens=256,
        context_window=3900,
        generate_kwargs={},
        model_kwargs={"n_gpu_layers": 1},
        messages_to_prompt=messages_to_prompt,
        completion_to_prompt=completion_to_prompt,
        verbose=True,
    )

    documentsData1 = SimpleDirectoryReader("data").load_data()
    documentsData2 = SimpleDirectoryReader("data/manuals").load_data()
    documentsData4 = SimpleDirectoryReader("data/manuals/.github").load_data()

    documentsData = documentsData1 + documentsData2 + documentsData4

    serviceContext = ServiceContext.from_defaults(llm=llmModel, embed_model=embedModel)
    indexData = VectorStoreIndex.from_documents(documentsData, service_context=serviceContext)

    queryEngine = indexData.as_query_engine()

    return queryEngine

queryEngine = load_data_and_models()

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
    queryInput = st.text_input("What would you like to ask? (source: data)", defaultQuery)
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

if 'page_number' not in st.session_state:
    st.session_state['page_number'] = 0

results_per_page = 10

start_index = st.session_state.page_number * results_per_page

c.execute('''
    SELECT * FROM results
    ORDER BY ROWID DESC
    LIMIT ? OFFSET ?
''', (results_per_page, start_index))
current_page_results = c.fetchall()

st.table(current_page_results)

if len(current_page_results) == results_per_page:
    if st.button('Next Page'):
        st.session_state.page_number += 1

if st.session_state.page_number > 0:
    if st.button('Previous Page'):
        st.session_state.page_number -= 1

conn.close()