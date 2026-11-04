# 9. Models, Prompts and Configuration

## Paper model
`models.py` defines a Pydantic `Paper`:
- `title: str`
- `authors: List[str]`
- `abstract: str`
- `published: str`
- `pdf_url: str`
- `source: str`
- `score: Optional[float]` defaulting to None.

The search agent maps arXiv metadata into this model. Approval serializes it with `model_dump()`.

## API models
Also in `models.py`:
- `SearchRequest(query)`
- `SearchResponse(papers)` — currently unused.
- `ApproveRequest(thread_id, paper_number)`
- `SaveRequest(thread_id, decision)`
- `AskRequest(thread_id, question)` — unused; no ask endpoint exists.

The separate `api/schemas.py` is empty.

## Prompt templates
`prompts.py` defines two LangChain ChatPromptTemplates:
- `SUMMARY_PROMPT`: paper analyst role, context-only instruction and five-section summary.
- `QA_PROMPT`: context-only answer, with an explicit not-found fallback and question/context fields.

## Configuration
`config.py` uses Pydantic Settings, loads `.env`, is case-insensitive and ignores extra fields.

| Setting | Default / requirement | Purpose |
|---|---|---|
| `groq_api_key` | Required | Groq credentials |
| `tavily_api_key` | Required | Declared but unused by current search |
| `langchain_api_key` | Required | Tracing-related credential field |
| `langchain_tracing_v2` | true | Tracing-related setting |
| `langchain_project` | `research-agent` | Project label |
| `llm_model` | `llama-3.1-8b-instant` | Groq model |
| `embedding_model` | `sentence-transformers/all-MiniLM-L6-v2` | Embedding model |
| `chunk_size` | 1000 | Chunk size |
| `chunk_overlap` | 200 | Chunk overlap |
| `top_k` | 4 | Declared retrieval setting; nodes use literal 4 |
| `max_search_results` | 5 | arXiv result limit |

A module-level `settings = Settings()` is created at import time. Missing required environment values can therefore stop application import/startup even if a requested code path would not use all of them.

## LLM client
`llm.py` creates ChatGroq with temperature 0 and streaming enabled. Summarization, QA and streaming helpers import this shared client.

## Security
Do not commit `.env` or keys. The Git ignore file excludes `.env`.
