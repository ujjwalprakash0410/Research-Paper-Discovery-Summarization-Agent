from langchain_community.vectorstores import FAISS

from state import GraphState
from rag.embeddings import embedding_model
from llm import llm
from prompts import QA_PROMPT


def qa_node(state: GraphState):

    vector_store = FAISS.load_local(
        state["vector_store_path"],
        embedding_model,
        allow_dangerous_deserialization=True,
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 4}
    )

    docs = retriever.invoke(state["qa_query"])

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    prompt = QA_PROMPT.invoke(
        {
            "context": context,
            "question": state["qa_query"],
        }
    )

    response = llm.invoke(prompt)

    sources = []

    for doc in docs:
        page = doc.metadata.get("page", "Unknown")
        sources.append(
            {
                "page": page,
                "content": doc.page_content[:250],
            }
        )

    return {
        "answer": response.content,
        "messages": sources,
    }