from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import settings


splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.chunk_size,
    chunk_overlap=settings.chunk_overlap,
)


def chunk_text(documents):
    """
    Split documents while preserving metadata.
    """

    return splitter.split_documents(documents)