import fitz
from langchain_core.documents import Document


def extract_text(pdf_path: str) -> list[Document]:
    """
    Extract text from a PDF while preserving page metadata.

    Returns:
        List[Document]: One Document per PDF page with page number metadata.
    """

    documents = []

    doc = fitz.open(pdf_path)

    try:
        for page_num, page in enumerate(doc):
            text = page.get_text("text").strip()

            # Skip empty pages
            if not text:
                continue

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "page": page_num + 1
                    }
                )
            )

    finally:
        doc.close()

    return documents