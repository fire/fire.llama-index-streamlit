# llama-index

A simple Streamlit web app for using [LlamaIndex](https://github.com/jerryjliu/llama_index), an interface to connect LLM’s with external data.

For a step-by-step guide, see [this](https://alphasec.io/query-your-own-documents-with-llamaindex-and-langchain/) post. To deploy on [Railway](https://railway.app/?referralCode=alphasec), click the button below.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/GpZ0J4?referralCode=alphasec)

## Quick start

1. Install the requirements: `pip install -r requirements.txt`
2. Install Streamlit: `pip install streamlit`
3. For Windows users, install cublas:

```powershell
$env:CMAKE_ARGS="-DLLAMA_CUBLAS=on"
pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
```

4. Run the application: `streamlit run index.py`
