import os
import streamlit as st
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, load_index_from_storage
from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt
from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from llama_index import StorageContext

st.title("Ask Aria")

query = st.text_input(
    "What would you like to ask? (source: data/godot-developer-fund.md)", ""
)

persist_dir = "./storage"

if st.button("Submit"):
    if not query.strip():
        st.error(f"Please provide the search query.")
    else:
        try:
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
            
            # Check if index is already persisted
            if os.path.exists(persist_dir):
                # rebuild storage context
                storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
                # load index
                index = load_index_from_storage(storage_context)
            else:
                index = VectorStoreIndex.from_documents(
                    documents, service_context=service_context
                )
                # Persist the index
                index.storage_context.persist(persist_dir=persist_dir)

            # Create a query engine from the index
            query_engine = index.as_query_engine()

            # Query the engine with the user's input
            response = query_engine.query(query)
            
            st.success(response)
        except Exception as e:
            import traceback
            st.error(f"An error occurred: {e}\n{traceback.format_exc()}")
