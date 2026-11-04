# 8. API and Streaming

## FastAPI setup
`main.py` creates a FastAPI instance titled “Research Paper Discovery & Summarization Agent”, version `1.0.0`, and registers `api.routes.router`. Routes are at the root; there is no version prefix or authentication middleware in the current app.

## Endpoint reference

| Method | Path | Behavior |
|---|---|---|
| GET | `/` | API running message |
| POST | `/search` | Starts graph thread and pauses for paper selection |
| POST | `/approve` | Resumes graph with paper number |
| POST | `/save` | Resumes graph with save decision |
| GET | `/library` | Returns saved-paper JSON library |
| GET | `/stream-summary` | Attempts to stream summary from local vector store |
| GET | `/health` | Returns healthy status |

## POST /search
Accepts `SearchRequest(query)`. It:
1. Generates a UUID thread ID.
2. Creates LangGraph config with that ID.
3. Initializes GraphState fields.
4. Calls `graph.invoke()`.
5. Reads the first interrupt payload.
6. Returns the thread ID, prompt and serialized papers.

The expected graph behavior is to pause at approval, so this route returns the candidates rather than a completed workflow result.

## POST /approve
Accepts `ApproveRequest(thread_id, paper_number)`. It resumes the same graph thread using `Command(resume=str(paper_number))` and returns `summary`, `answer` and `sources`. In the currently wired graph, summary is populated; answer and sources are not because QA is not wired.

## POST /save
Accepts `SaveRequest(thread_id, decision)`, resumes the second interrupt and returns `{"status": "success"}`. This response is returned for a no decision as well; it means the resume request completed, not necessarily that a record was saved.

## Library and health
- `GET /library` returns `MemoryStore.get_library()`.
- `GET /health` returns `{"status": "healthy"}`; it does not probe external services.
- `GET /` returns `{"message": "Research Agent API Running"}`.

## Streaming route
`GET /stream-summary` calls `stream_summary("vectorstore", "Large Language Models")` and wraps it in `StreamingResponse(media_type="text/plain")`.

Because the later `stream_summary(retriever, query)` definition shadows the earlier path-based function, the string path is treated as a retriever. When iteration begins, the code attempts `.invoke()` on the string and fails. The route is hard-coded and not parameterized by request.

`api/streaming.py` provides a generic `stream_response(generator)` wrapper but the route constructs StreamingResponse directly and does not use it.

## Request models
`models.py` defines SearchRequest, SearchResponse (unused), ApproveRequest, SaveRequest and AskRequest (no matching API route). `api/schemas.py` is empty.
