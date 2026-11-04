# 3. Agent Workflow

This page describes each node registered in `graph.py`.

## Planner — `agents/planner.py`
- Reads `state["query"]`.
- Strips leading/trailing whitespace.
- Raises `ValueError("Query cannot be empty.")` for an empty query.
- Returns the normalized query.

It is deterministic validation, not an LLM planning agent. It does not decompose the research goal, generate a search plan or dynamically select tools.

## Search — `agents/search.py`
Calls `search_arxiv(query)`, maps arXiv results into `Paper` objects and stores them in `papers`. See [Paper Discovery](04-paper-discovery.md).

## Approval — `agents/approval.py`
- Reads the papers list.
- Prints paper titles to standard output.
- Calls LangGraph `interrupt` with a prompt and serialized paper objects.
- On resume, converts the response to an integer, subtracts one and selects that result.
- Returns `selected_index` and `selected_paper`.

There is no explicit check that the selection is numeric and within the valid list range.

## Document Processor — `agents/document_processor.py`
- Uses the `papers/` directory.
- Downloads the selected PDF to the fixed path `papers/selected.pdf`.
- Extracts page documents with `rag.parser.extract_text`.
- Chunks them with `rag.chunking.chunk_text`.
- Builds FAISS using `rag.faiss_db.build_vector_store`.
- Saves the index to the fixed path `vectorstore`.
- Returns `vector_store_path`.

See [PDF Processing and RAG](05-pdf-processing-and-rag.md).

## Summarizer — `agents/summarizer.py`
Loads the FAISS index, retrieves up to four chunks using the original discovery query, joins their text, invokes `SUMMARY_PROMPT`, calls the Groq model and returns `summary`. It summarizes retrieved context, not necessarily every page of the paper.

## Save — `agents/save.py`
Pauses for a yes/no decision. If the lowercased decision is exactly `yes`, stores the selected paper and summary using `MemoryStore.add_paper`. Other values skip the save.

## QA — defined, not registered
`agents/qa.py` implements retrieval-based answering, but `graph.py` does not add it with `builder.add_node` or connect it with an edge. Therefore, it never executes in the current graph. The `qa_query`, `answer` and `messages` state fields remain unpopulated by the wired workflow.
