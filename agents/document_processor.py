from pathlib import Path

from state import GraphState

from utils.pdf import download_pdf

from rag.parser import extract_text

from rag.chunking import chunk_text

from rag.faiss_db import build_vector_store


PDF_DIR = Path("papers")

PDF_DIR.mkdir(exist_ok=True)


def processor_node(state: GraphState):

    paper = state["selected_paper"]

    pdf_path = PDF_DIR / "selected.pdf"

    download_pdf(

        paper.pdf_url,

        pdf_path

    )

    documents = extract_text(str(pdf_path))

    chunks = chunk_text(documents)

    vector_store = build_vector_store(chunks)

    vector_store.save_local("vectorstore")

    return {
        "vector_store_path": "vectorstore"
    }