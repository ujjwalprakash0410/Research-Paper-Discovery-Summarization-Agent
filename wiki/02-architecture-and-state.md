# 2. Architecture and LangGraph State

## Entry points
- `main.py` creates the FastAPI app and registers `api.routes.router`.
- `app.py` is a terminal-driven demonstration that invokes the compiled graph and resumes it using interactive input.
- Both paths use the compiled `graph` from `graph.py`.

## Graph construction
`graph.py` creates a `StateGraph(GraphState)`, adds nodes and connects them in a straight line:

```text
START → planner → search → approval → document_processor
      → summarizer → save → END
```

The graph is compiled with LangGraph `MemorySaver` as its checkpointer, allowing graph pauses and resume calls for a given thread ID.

## GraphState

Defined in `state.py` as a TypedDict:

| Field | Purpose | Current writer |
|---|---|---|
| `query` | User discovery query | Caller; normalized by planner |
| `papers` | Search result list | Search node |
| `selected_index` | Zero-based selected result | Approval node |
| `selected_paper` | Chosen Paper object | Approval node |
| `summary` | Generated summary | Summarizer node |
| `vector_store_path` | Local FAISS directory | Processor node |
| `messages` | Intended source excerpts | QA node, currently unwired |
| `qa_query` | Intended follow-up question | Caller / future QA flow |
| `answer` | Intended grounded answer | QA node, currently unwired |

Nodes return partial dictionaries; LangGraph merges those updates into the working state.

## Node sequence
The planner validates the query, search writes papers, approval writes the selection, processor writes the vector directory, summarizer writes the summary, and save optionally writes to the library. The QA node is imported in `graph.py` but is not registered as a graph node and has no edge.

## Interrupt and resume
The approval and save agents call LangGraph `interrupt(payload)`. The caller resumes the paused graph with `Command(resume=value)` and the same configuration:
`{"configurable": {"thread_id": "..."}}`.

The API creates a UUID thread ID during `POST /search` and requires that ID for `/approve` and `/save`.

## MemorySaver scope
`MemorySaver` stores checkpoints in process memory. It is suitable for a local demonstration but is not durable across server restarts and is not shared across multiple API worker processes. Outstanding approval sessions may be lost when the process restarts.
