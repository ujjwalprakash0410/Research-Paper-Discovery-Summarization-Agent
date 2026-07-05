from langchain_community.vectorstores import FAISS

from state import GraphState
from rag.embeddings import embedding_model
from llm import llm
from prompts import SUMMARY_PROMPT


def summarizer_node(state: GraphState):

    vector_store = FAISS.load_local(
        state["vector_store_path"],
        embedding_model,
        allow_dangerous_deserialization=True,
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 4}
    )

    docs = retriever.invoke(state["query"])

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    prompt = SUMMARY_PROMPT.invoke(
        {
            "context": context
        }
    )

    response = llm.invoke(prompt)

    return {
        "summary": response.content
    }

from langchain_community.vectorstores import FAISS

from rag.embeddings import embedding_model
from prompts import SUMMARY_PROMPT
from llm import llm


def stream_summary(vector_store_path: str, query: str):

    vector_store = FAISS.load_local(
        vector_store_path,
        embedding_model,
        allow_dangerous_deserialization=True,
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 4}
    )

    docs = retriever.invoke(query)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = SUMMARY_PROMPT.invoke(
        {
            "context": context
        }
    )

    for chunk in llm.stream(prompt):

        if chunk.content:

            yield chunk.content

from agents.streaming import stream_llm


def stream_summary(retriever, query):

    docs = retriever.invoke(query)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = SUMMARY_PROMPT.invoke(
        {
            "context": context
        }
    )

    yield from stream_llm(prompt)