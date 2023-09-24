# llama-index

A simple Streamlit web app for using [LlamaIndex](https://github.com/jerryjliu/llama_index), an interface to connect LLM’s with external data.

## Quick start

```
scoop install micromamba
(& $env:MAMBA_EXE 'shell' 'hook' -s 'powershell' -p $env:MAMBA_ROOT_PREFIX) | Out-String | Invoke-Expression
micromamba create -n llama-index
micromamba activate -n llama-index
$env:CMAKE_ARGS="-DLLAMA_CUBLAS=on"
pip install llama-cpp-python --force-reinstall --upgrade --user
pip install -r requirements.txt
pip install streamlit
streamlit run index.py
```

## Quick start, second run

```powershell
micromamba activate -n llama-index
streamlit run index.py
```
