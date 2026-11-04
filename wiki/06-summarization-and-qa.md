# 6. Summarization and Question Answering

## LLM client
`llm.py` constructs one shared `ChatGroq` instance:
- Model: `settings.llm_model` (default `llama-3.1-8b-instant`).
- API key: `settings.groq_api_key`.
- Temperature: 0.
- Streaming: enabled.

## Summary prompt
`prompts.py` defines `SUMMARY_PROMPT`. It instructs the model to act as an expert research-paper analyst, use only retrieved context, and summarize using:
1. Problem
2. Method
3. Results
4. Limitations
5. Future Work

The summarizer node retrieves four chunks using the original discovery query, joins page content into a context string, invokes the prompt and calls the Groq LLM. The response content becomes GraphState `summary`.

### Interpretation
This is a query-focused RAG summary, not a guarantee of complete-paper coverage. If the discovery query retrieves only a narrow section, methods, evaluation results or limitations elsewhere in the paper can be omitted.

## QA prompt and node
`QA_PROMPT` instructs the assistant to answer only from supplied context and to return “I could not find the answer in the paper.” if the evidence is absent.

`agents/qa.py`:
1. Loads FAISS from `state["vector_store_path"]`.
2. Retrieves four chunks using `state["qa_query"]`.
3. Joins the retrieved content.
4. Invokes QA_PROMPT with context and question.
5. Calls the LLM.
6. Builds source items containing page metadata and the first 250 characters of each retrieved chunk.
7. Returns `answer` and `messages`.

### Current execution status
The QA node is not registered in `graph.py`. Its function exists but the current graph never invokes it. There is no implemented follow-up question route despite an `AskRequest` model. The API's `/approve` response includes answer/source fields but they remain at their initial empty values in the current graph path.

## Streaming helpers
- `agents/streaming.py` yields non-empty content chunks from `llm.stream(prompt)`.
- `agents/summarizer.py` defines `stream_summary` twice with different signatures.
- The later definition accepts an already-built retriever and a query, and shadows the earlier path-based implementation.
- The API calls the function with a string path, so the surviving function attempts `.invoke()` on a string and fails when iterated.

See [API and Streaming](08-api-and-streaming.md) and [Implementation Gaps](12-implementation-gaps.md).
