from langchain_community.vectorstores import FAISS

from rag.embeddings import embedding_model


def build_vector_store(chunks):

    return FAISS.from_documents(

        chunks,

        embedding_model

    )