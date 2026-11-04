# 10. Deployment and Runtime

## Dependencies
`requirements.txt` declares FastAPI, Uvicorn, LangGraph, LangChain core/community/Groq/HuggingFace/text-splitters, FAISS CPU, sentence-transformers, PyMuPDF, Pydantic/Pydantic Settings, python-dotenv, requests, arxiv and Tavily Python. Docker uses Python 3.11.

## Required environment
The Settings model requires:
- `GROQ_API_KEY`
- `TAVILY_API_KEY`
- `LANGCHAIN_API_KEY`

It also defines model, embedding, chunk, search and tracing settings. Because Settings is instantiated at import time, missing required values can stop startup before routes are registered.

Tavily is required by Settings but is not called in the source reviewed; discovery currently uses arXiv.

## Local run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Terminal workflow:
```bash
python app.py
```

The CLI starts with a hard-coded research query and QA question and prompts for paper selection and save confirmation.

## Docker
The Dockerfile:
- Uses `python:3.11-slim`.
- Sets bytecode, output buffering, pip cache and `PYTHONPATH=/app`.
- Installs requirements and copies source into `/app`.
- Exposes 8000 and runs Uvicorn on `0.0.0.0:8000`.

Compose defines one `research-agent` service, maps host 8000 to container 8000, loads `.env` and restarts unless stopped. It does not configure a persistent volume; downloaded papers, vectorstore and library JSON are container-local unless mounted externally.

## Ignore rules
`.gitignore` excludes local environment, caches, `papers/`, `vectorstore/` and `library.json`. `.dockerignore` excludes runtime artifacts and local development files from the build context.

## Tests
`tests/test_graph.py` and `tests/__init__.py` are empty. There are no implemented automated test cases in the tracked tests directory at this revision.
