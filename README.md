# llama-index

A simple Streamlit web app for using [LlamaIndex](https://github.com/jerryjliu/llama_index), an interface to connect LLM’s with external data.

## Quick start

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
streamlit run index.py --server.port 8502 --server.address 0.0.0.0
```

## Quick start, second run

```powershell
micromamba activate -n llama-index
streamlit run index.py --server.port 8502 --server.address 0.0.0.0
```

## Quick start, second run proxying

```
cp com.fire.llama.index.streamlit.plist ~/Library/LaunchAgents/
launchctl load  ~/Library/LaunchAgents/com.fire.llama.index.streamlit.plist
```

```zsh
wg-quick down ./tunnel.conf
curl https://tunnel.pyjam.as/8502 > tunnel.conf && wg-quick up ./tunnel.conf
```
