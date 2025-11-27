## Set up venv and use venv for this shell
```
python -m venv .venv
source .venv/bin/activate
```

## Install requirements

install requirements
```
pip install -r requirements.txt
```

## Ollama

_if running ollama is too much for you, replace it with openai llm in the code and requirements.txt_

Install ollama and start ollama locally with llama3 model loaded
this is a bit os dependent. This casually pulls a 4.7GB model into your machine.


Run this is in some other shell pretty please :)
```
ollama pull llama3
ollama serve
```

## Start the app

start the thing with
```
fastapi dev app.py
```
