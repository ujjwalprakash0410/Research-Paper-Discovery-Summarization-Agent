# 12. Implementation Gaps and Roadmap

This page separates code that is present from functionality that is actually connected to the running workflow.

## Confirmed gaps

### 1. QA node is imported but not registered
`graph.py` imports `qa_node` but never calls `builder.add_node("qa", qa_node)` or adds an edge to it. Therefore `qa_query` is not processed, `answer` is not populated and `messages` sources are not produced. The API and CLI expose fields/output that remain empty in the current connected workflow.

**Suggested fix:** register and connect the QA node, or expose a separate graph/API path for follow-up questions.

### 2. Streaming helper definitions conflict
`agents/summarizer.py` defines `stream_summary` twice:
- Earlier: accepts vector-store path + query and loads FAISS.
- Later: accepts retriever object + query.

Python keeps the later definition. The API calls it with `"vectorstore"` as the first argument, so the function later tries `.invoke()` on a string and fails.

**Suggested fix:** keep one definition and make its expected input explicit; add a route-level streaming test.

### 3. Checkpoints are in-memory
`MemorySaver` is not durable across process restarts and does not share state across multiple worker processes.

**Suggested fix:** adopt a persistent LangGraph checkpointer for deployed sessions.

### 4. Fixed PDF/index paths are shared
Every workflow writes to `papers/selected.pdf` and `vectorstore`. Concurrent sessions can overwrite one another's PDF/index; later selections replace the previous vector store.

**Suggested fix:** use per-thread or per-document paths and store those unique paths in GraphState.

### 5. Save route reports success even for no
The save route returns `{"status": "success"}` after resuming regardless of whether the decision was yes or no.

**Suggested fix:** return an explicit saved/not-saved result from the node and propagate it into state/API output.

## Other gaps
- Tavily key/dependency exists but Tavily is not used.
- `top_k` config exists but summary/QA use literal 4.
- No OCR fallback; image-only pages are skipped.
- PDF download has no explicit timeout or streaming-to-disk behavior.
- Selection number has no bounds validation.
- JSON library has no deduplication, locking or atomic write strategy.
- Compose has no persistent data volume.
- Required environment settings instantiate at import time.
- LangChain tracing settings are declared, but explicit tracing setup is not present in the tracked application code.
- No automated tests are implemented in the tracked test file.
- No authentication, authorization, rate limiting or production-grade observability.
- Summary prompt sees only a few retrieved chunks, so it may not cover the entire paper.

## Suggested implementation order
1. Connect and test QA or remove misleading empty answer/source fields.
2. Fix duplicate streaming function and test stream endpoint.
3. Isolate downloaded PDF and FAISS index per session.
4. Validate approval index and add download timeout/error handling.
5. Persist graph checkpoints and library data in deployment.
6. Make settings optional where appropriate; wire Tavily/tracing or remove unused config.
7. Add OCR and better table/layout extraction if scanned PDFs are in scope.
8. Add tests for interrupts/resume, parsing, chunk metadata, FAISS reload, summary, QA, streaming and library writes.
9. Add authentication, authorization, auditability, monitoring and rate limiting before exposing beyond a trusted demo.

## Do not infer
- Having a QA function does not mean the current graph runs QA.
- Having Tavily in requirements/config does not mean Tavily search is active.
- FAISS here is dense retrieval, not hybrid retrieval.
- A structured prompt does not guarantee full-paper coverage when only top-k chunks are supplied.
- MemorySaver and local JSON do not provide durable multi-user memory.
