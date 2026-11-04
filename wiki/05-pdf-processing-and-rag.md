# 5. PDF Processing and RAG

## Processing pipeline

```text
Selected Paper.pdf_url
       ↓
utils/pdf.py — requests.get()
       ↓
papers/selected.pdf
       ↓
rag/parser.py — PyMuPDF page extraction
       ↓
Document(page_content, metadata.page)
       ↓
rag/chunking.py — RecursiveCharacterTextSplitter
       ↓
rag/embeddings.py — HuggingFace embeddings
       ↓
rag/faiss_db.py — FAISS.from_documents()
       ↓
vectorstore/ — save_local()
```

## PDF download
`utils/pdf.py` calls `requests.get(url)`, checks the HTTP status with `raise_for_status()`, then writes the full response body to the requested path. The caller always uses `papers/selected.pdf`. No request timeout is specified, and the full body is held in memory before writing.

## Text extraction
`rag/parser.py` uses PyMuPDF:
- Opens the PDF with `fitz.open`.
- Iterates pages using zero-based indices but records one-based page numbers.
- Calls `page.get_text("text").strip()`.
- Skips pages with no extracted text.
- Creates one LangChain `Document` per non-empty page.
- Stores the source page in `Document.metadata["page"]`.
- Closes the PDF in a `finally` block.

No OCR fallback is implemented. Image-only/scanned pages with no text layer are skipped. Tables are not parsed separately; any text emitted by PyMuPDF is included in the page text.

## Chunking
`rag/chunking.py` configures `RecursiveCharacterTextSplitter` with:
- `chunk_size = 1000` by default.
- `chunk_overlap = 200` by default.

`chunk_text(documents)` calls `split_documents`, which retains the source Document metadata on split chunks.

## Embeddings
`rag/embeddings.py` creates a module-level `HuggingFaceEmbeddings` instance using `sentence-transformers/all-MiniLM-L6-v2` by default. This shared object is used when building and loading FAISS.

## FAISS vector store
`rag/faiss_db.py` wraps `FAISS.from_documents(chunks, embedding_model)`. The processor persists the store through `save_local("vectorstore")`. The summary and QA code load it with `FAISS.load_local(..., allow_dangerous_deserialization=True)`.

## Retrieval
Both summary and QA nodes configure `search_kwargs={"k": 4}`. The value is hard-coded, even though `top_k` is declared in configuration.

## Limitations
- Retrieval is dense vector search; there is no BM25/hybrid retrieval.
- Page metadata is retained and can be surfaced by the QA node.
- Summarization uses query-retrieved chunks rather than a full-paper hierarchical summary.
- There is no reranker, query expansion, metadata filtering or citation verification.
- There is no OCR or dedicated table extraction.
- The PDF name and vector-store path are fixed, creating potential collisions between concurrent workflows.
- Loading FAISS with dangerous deserialization enabled assumes the local index files are trusted.
