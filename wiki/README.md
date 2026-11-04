# Research Paper Discovery & Summarization Agent — Wiki

This wiki documents the current code in the repository. It follows the runtime from a research query through arXiv discovery, paper selection, PDF processing, FAISS indexing, summarization and optional library storage.

## Start here
- [01 — Project Overview](01-project-overview.md)
- [02 — Architecture and LangGraph State](02-architecture-and-state.md)
- [03 — Agent Workflow](03-agent-workflow.md)
- [04 — Paper Discovery](04-paper-discovery.md)
- [05 — PDF Processing and RAG](05-pdf-processing-and-rag.md)
- [06 — Summarization and QA](06-summarization-and-qa.md)
- [07 — Human Approval and Paper Library](07-human-approval-and-library.md)
- [08 — API and Streaming](08-api-and-streaming.md)
- [09 — Models, Prompts and Configuration](09-models-prompts-and-config.md)
- [10 — Deployment and Runtime](10-deployment-and-runtime.md)
- [11 — Complete Code Map](11-code-map.md)
- [12 — Implementation Gaps and Roadmap](12-implementation-gaps.md)

## System flow
```text
Research query → Planner → arXiv search → Human paper selection
 → PDF download → PyMuPDF extraction → overlapping chunks
 → Hugging Face embeddings → FAISS index → top-4 retrieval
 → Groq LLM structured summary → Human save decision → library.json
```

## Important implementation note
A QA agent exists in `agents/qa.py`, but the current `graph.py` does not register or connect it. Consequently, the graph does not populate answer/source fields. The streaming summary helper is also defined twice with different signatures; the later definition shadows the earlier one, while the API calls it using the earlier signature. These issues are documented in [Implementation Gaps](12-implementation-gaps.md).

## Source scope
This wiki is based on the recursive `main` tree and the contents of every tracked file in it. Empty files—including `README.md`, `api/schemas.py`, `tests/test_graph.py` and package markers—are recorded as empty rather than assigned behavior they do not contain.
