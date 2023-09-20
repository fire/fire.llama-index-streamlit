# llama-index

A simple Streamlit web app for using [LlamaIndex](https://github.com/jerryjliu/llama_index), an interface to connect LLM’s with external data.

For a step-by-step guide, see [this](https://alphasec.io/query-your-own-documents-with-llamaindex-and-langchain/) post. To deploy on [Railway](https://railway.app/?referralCode=alphasec), click the button below.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/GpZ0J4?referralCode=alphasec)

## Quick start

```
scoop install micromamba
(& $env:MAMBA_EXE 'shell' 'hook' -s 'powershell' -p $env:MAMBA_ROOT_PREFIX) | Out-String | Invoke-Expression
micromamba create -n llama-index
micromamba activate -n llama-index
micromamba install -c conda-forge clblast
$env:CMAKE_ARGS="-DLLAMA_CLBLAST=on"
pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir --user
pip install -r requirements.txt
pip install streamlit
streamlit run index.py
```