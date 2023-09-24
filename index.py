import os
import streamlit as st
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt
from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings

st.title("Ask Aria")

# Construct the model outside of the form submission check
embed_model = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-base-en")
llm = LlamaCPP(
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

# Load documents from the 'data' directory
documents = SimpleDirectoryReader("data").load_data()
service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
index = VectorStoreIndex.from_documents(
    documents, service_context=service_context
)

# Create a chat engine from the index
chat_engine = index.as_chat_engine()

with st.form(key='my_form'):
    query = st.text_input(
        "What would you like to ask? (source: data)", ""
    )
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    if not query.strip():
        st.error(f"Please provide the search query.")
    else:
        try:
            # Chat with the engine using the user's input
            response = chat_engine.chat(query)
            
            st.success(response)
        except Exception as e:
            import traceback
            st.error(f"An error occurred: {e}\n{traceback.format_exc()}")
