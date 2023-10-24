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
from llama_index import StorageContext, load_index_from_storage
from llama_index.llms import ChatMessage, MessageRole
from llama_index.chat_engine.condense_question import CondenseQuestionChatEngine
from llama_index.prompts.base import PromptTemplate
import uuid

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
"""
)


@st.cache_data(ttl=3600)
def load_documents(paths):
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

embedModel = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-base-en")
llmModel = LlamaCPP(
    model_url="https://huggingface.co/TheBloke/LlongOrca-13B-16K-GGUF/resolve/main/llongorca-13b-16k.Q5_K_S.gguf",
    temperature=0.1,
    max_new_tokens=1024,
    context_window=8000,
    generate_kwargs={},
    model_kwargs={"n_gpu_layers": 1000},
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    verbose=True,
)
serviceContext = ServiceContext.from_defaults(llm=llmModel, embed_model=embedModel)

storage_context = StorageContext.from_defaults(persist_dir="./storage")

@st.cache_resource(ttl=3600)
def load_index_data(_storage_context, _docs, _service_context):
    try:
        indexData = load_index_from_storage(_storage_context)
    except Exception as e:
        print(f"Index data not found in storage. Generating new vectors: {e}")
        indexData = VectorStoreIndex.from_documents(
            _docs, service_context=_service_context
        )
    return indexData


indexData = load_index_data(storage_context, docs, serviceContext)


custom_prompt = PromptTemplate(
    """
Given a conversation (between user and assistant) and a follow up message from the person,
rewrite the message to be a standalone question that captures all relevant context
from the conversation.

<Chat History> {chat_history}

<Follow Up Message> {question}

<Standalone question>
"""
)

custom_chat_history = []

query_engine = indexData.as_query_engine()

chat_engine = CondenseQuestionChatEngine.from_defaults(
    query_engine=query_engine,
    condense_question_prompt=custom_prompt,
    chat_history=custom_chat_history,
    verbose=False,
)

indexData.storage_context.persist()

defaultQuery = ""

# Connect to SQLite database
conn = sqlite3.connect("query_results.db")
c = conn.cursor()

# Create new conversations table
c.execute(
    """
    CREATE TABLE IF NOT EXISTS conversations (
        id TEXT,
        conversation_id TEXT,
        timestamp TEXT,
        from_user TEXT,
        value TEXT,
        time REAL,
        PRIMARY KEY (id)
    )
"""
)

# Check if results table exists
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='results'")
if c.fetchone():
    # Copy data from results table to conversations table
    c.execute(
        """
        INSERT INTO conversations (id, conversation_id, timestamp, from_user, value, time)
        SELECT NULL, NULL, timestamp, 'user', query, time FROM results
    """
    )
    c.execute("DROP TABLE IF EXISTS results")

# Form for user input
with st.form(key="my_form"):
    queryInput = st.text_input(
        "What would you like to ask? (source: data)", defaultQuery
    )
    submitButton = st.form_submit_button(label="Submit")

# Process form submission
if submitButton:
    if not queryInput.strip():
        st.error(f"Please provide the search query.")
    else:
        try:
            startTime = time.time()
            responseOutput = chat_engine.query(queryInput)
            elapsedTime = time.time() - startTime
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            responseString = str(responseOutput)

            # Generate a new conversation UUID
            conversation_id = str(uuid.uuid4())

            # Insert user's message into conversations table
            c.execute(
                """
                INSERT INTO conversations (id, conversation_id, timestamp, from_user, value, time)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    str(uuid.uuid4()),
                    conversation_id,
                    timestamp,
                    "user",
                    queryInput,
                    elapsedTime,
                ),
            )

            # Insert assistant's response into conversations table
            c.execute(
                """
                INSERT INTO conversations (id, conversation_id, timestamp, from_user, value, time)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    str(uuid.uuid4()),
                    conversation_id,
                    timestamp,
                    "assistant",
                    responseString,
                    elapsedTime,
                ),
            )

            conn.commit()

            st.success(responseOutput)
        except Exception as e:
            import traceback

            st.error(f"An error occurred: {e}\n{traceback.format_exc()}")

# Pagination
if "page_number" not in st.session_state:
    st.session_state["page_number"] = 0

results_per_page = 10
start_index = st.session_state.page_number * results_per_page


@st.cache_data(ttl=3600)
def fetch_results(results_per_page, start_index):
    c.execute(
        """
        WITH duration AS (
            SELECT 
                conversation_id, 
                timestamp, 
                MAX(time) - MIN(time) AS duration_in_seconds 
            FROM conversations 
            GROUP BY conversation_id
        ), 
        overhead AS (
            SELECT 
                conversation_id, 
                timestamp, 
                SUM(time) OVER (ORDER BY timestamp DESC, conversation_id ASC) AS cumulative_system_overhead 
            FROM conversations
        )
        SELECT 
            c.conversation_id, 
            c.timestamp, 
            c.from_user, 
            c.value,
            d.duration_in_seconds,
            o.cumulative_system_overhead
        FROM conversations c
        JOIN duration d ON c.conversation_id = d.conversation_id AND c.timestamp = d.timestamp
        JOIN overhead o ON c.conversation_id = o.conversation_id AND c.timestamp = o.timestamp
        ORDER BY c.timestamp DESC, c.conversation_id ASC
        LIMIT ? OFFSET ?
        """,
        (results_per_page, start_index),
    )
    return c.fetchall()


current_page_results = fetch_results(results_per_page, start_index)

st.table(current_page_results)

if len(current_page_results) == results_per_page:
    if st.button("Next Page"):
        st.session_state.page_number += 1

if st.session_state.page_number > 0:
    if st.button("Previous Page"):
        st.session_state.page_number -= 1

conn.close()
