# llama-index

A simple Streamlit web app for using [LlamaIndex](https://github.com/jerryjliu/llama_index), an interface to connect LLM’s with external data.

## Quick start Windows

```
scoop install micromamba
(& $env:MAMBA_EXE 'shell' 'hook' -s 'powershell' -p $env:MAMBA_ROOT_PREFIX) | Out-String | Invoke-Expression
micromamba create -n llama-index
micromamba activate -n llama-index
micromamba install -c conda-forge clblast
$env:CMAKE_ARGS="-DLLAMA_CLBLAST=on" 
pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
pip install -r requirements.txt
pip install streamlit
streamlit run index.py --server.port 8502 --server.address 127.0.0.1
```

## Quick start Macos

```
# install micromamba
micromamba create -n llama-index
micromamba activate -n llama-index
pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
pip install -r requirements.txt
pip install streamlit
streamlit run index.py --server.port 8502 --server.address 127.0.0.1
```

## Quick start, second run

```powershell
micromamba activate -n llama-index
streamlit run index.py --server.port 8502 --server.address 127.0.0.1
```

## Quick start, second run proxying

```
cp com.fire.llama.index.streamlit.plist ~/Library/LaunchAgents/
launchctl unload  ~/Library/LaunchAgents/com.fire.llama.index.streamlit.plist
launchctl load  ~/Library/LaunchAgents/com.fire.llama.index.streamlit.plist
```

```zsh
curl https://get.telebit.io/ | bash
telebit http 8502
```
