# Research Paper Discovery & Summarization Agent

A LangGraph-based research assistant that searches arXiv, pauses for human paper selection, downloads and indexes a selected PDF with FAISS, and generates a structured RAG summary using Groq.

## Main workflow

```text
Query → Planner → arXiv Search → Human Approval → PDF Processing
→ Chunking → Embeddings / FAISS → RAG Summary → Save Decision
```

## Technology
- **Orchestration:** LangGraph
- **LLM:** Groq via LangChain
- **Paper discovery:** arXiv
- **PDF processing:** PyMuPDF
- **Embeddings:** Hugging Face sentence-transformers
- **Vector store:** FAISS
- **API:** FastAPI

## Wiki

See the [project wiki](wiki/README.md) for architecture, agent responsibilities, data flow, RAG pipeline, API routes, configuration, deployment and implementation gaps.

## Important implementation note

The QA node is currently defined but not connected to the LangGraph workflow. The streaming summary helper also has a duplicate-definition/signature mismatch. These are documented in the wiki's [implementation gaps](wiki/12-implementation-gaps.md).

## Disclaimer

This repository is a research assistant demonstration. Always verify generated summaries and research claims against the original paper.
