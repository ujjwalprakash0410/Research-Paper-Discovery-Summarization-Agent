# 1. Project Overview

## What the application does
The Research Paper Discovery & Summarization Agent searches arXiv for papers matching a text query, lets a user select one result, downloads the selected PDF, creates a local vector index from its extracted text, and uses a language model to generate a structured summary.

The intended summary sections are:
- Problem
- Method
- Results
- Limitations
- Future Work

A retrieval-based question-answering node is also defined, intended to answer follow-up questions from the selected paper and return page-level source excerpts. However, that node is not connected to the current LangGraph workflow.

## Implemented capabilities
1. **Research discovery:** arXiv search sorted by relevance.
2. **Human selection:** graph pauses and waits for a paper number.
3. **PDF ingestion:** downloads the selected PDF and extracts text page by page.
4. **RAG preparation:** splits page documents into chunks, embeds them and stores them in FAISS.
5. **Summarization:** retrieves up to four chunks and asks the Groq chat model for a structured summary.
6. **Optional library save:** asks whether to save the paper and summary to local JSON.
7. **API access:** exposes search, approval, save, library, health and summary-stream routes.
8. **CLI demonstration:** `app.py` runs the graph interactively in a terminal.

## Technology stack

| Layer | Technology |
|---|---|
| Workflow | LangGraph StateGraph |
| Human-in-the-loop | LangGraph interrupt / Command resume |
| LLM | ChatGroq through LangChain |
| Research source | arXiv Python client |
| PDF extraction | PyMuPDF |
| Chunking | RecursiveCharacterTextSplitter |
| Embeddings | Hugging Face sentence-transformer embeddings |
| Vector store | LangChain FAISS |
| API | FastAPI + Uvicorn |
| Paper library | Local JSON file |
| PDF download | Requests |
| Configuration | Pydantic Settings |

## Not implemented
The current code does not implement general web discovery despite declaring Tavily configuration and a dependency; search uses arXiv only. It also lacks a connected QA stage, frontend web app, database-backed library, durable graph checkpointing and multi-paper synthesis.

## User journey
A user submits a topic such as “Large Language Models”. The planner validates it, the search agent retrieves arXiv results, and the approval node pauses for selection. After the user picks a paper, the processor downloads and indexes its PDF. The summarizer generates a structured review. The save node asks whether to add the paper and summary to the local library.
