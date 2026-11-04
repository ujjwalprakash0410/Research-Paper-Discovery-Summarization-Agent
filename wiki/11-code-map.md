# 11. Complete Code Map

```text
Research-Paper-Discovery-Summarization-Agent/
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
├── app.py
├── config.py
├── docker-compose.yaml
├── graph.py
├── llm.py
├── main.py
├── models.py
├── prompts.py
├── state.py
├── requirements.txt
├── agents/
│   ├── ___init__.py
│   ├── approval.py
│   ├── document_processor.py
│   ├── planner.py
│   ├── qa.py
│   ├── save.py
│   ├── search.py
│   ├── streaming.py
│   └── summarizer.py
├── api/
│   ├── __init__.py
│   ├── routes.py
│   ├── schemas.py
│   └── streaming.py
├── memory/
│   ├── __init__.py
│   └── store.py
├── rag/
│   ├── __init__.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── faiss_db.py
│   └── parser.py
├── tests/
│   ├── __init__.py
│   └── test_graph.py
└── utils/
    ├── __init__.py
    ├── helpers.py
    └── pdf.py
```

## File responsibilities

| File | Responsibility |
|---|---|
| `main.py` | FastAPI entry point |
| `app.py` | Interactive terminal graph demo |
| `graph.py` | StateGraph nodes, edges and MemorySaver |
| `state.py` | GraphState TypedDict |
| `config.py` | Pydantic Settings |
| `models.py` | Paper and API request/response models |
| `prompts.py` | Summary and QA prompt templates |
| `llm.py` | Shared ChatGroq client |
| `agents/planner.py` | Query trimming and validation |
| `agents/search.py` | arXiv search and Paper mapping |
| `agents/approval.py` | Human paper-selection interrupt |
| `agents/document_processor.py` | PDF download, extraction, chunking and FAISS persistence |
| `agents/summarizer.py` | RAG summarization and streaming helpers |
| `agents/qa.py` | Retrieval-grounded QA function (not graph-wired) |
| `agents/save.py` | Save-decision interrupt and library write |
| `agents/streaming.py` | LLM token streaming generator |
| `api/routes.py` | HTTP routes and graph session resume |
| `api/streaming.py` | Generic StreamingResponse helper |
| `memory/store.py` | JSON paper library |
| `rag/parser.py` | PyMuPDF text extraction and page metadata |
| `rag/chunking.py` | RecursiveCharacterTextSplitter |
| `rag/embeddings.py` | Hugging Face embedding singleton |
| `rag/faiss_db.py` | FAISS vector store construction |
| `utils/pdf.py` | HTTP PDF download helper |
| `requirements.txt` | Python dependencies |
| Docker files | Container build and run settings |
| Tests | Empty test module at inspected revision |
| `README.md`, `api/schemas.py`, `utils/helpers.py` | Empty at inspected revision |
| Package markers | Empty except unusual `agents/___init__.py` filename |

The `agents/___init__.py` name is exactly as present in the repository.
