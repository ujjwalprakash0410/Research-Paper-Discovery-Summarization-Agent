from langchain_community.vectorstores import FAISS

from rag.embeddings import embedding_model
from prompts import QA_PROMPT
from llm import llm

from memory.chat_store import (
    add_message,
    get_history,
)


def answer_question(
    thread_id: str,
    vector_store_path: str,
    question: str,
):

    vector_store = FAISS.load_local(
        vector_store_path,
        embedding_model,
        allow_dangerous_deserialization=True,
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 4}
    )

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    history = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in get_history(thread_id)
    )

    prompt = QA_PROMPT.invoke(
        {
            "history": history,
            "context": context,
            "question": question,
        }
    )

    response = llm.invoke(prompt)

    add_message(
        thread_id,
        "User",
        question,
    )

    add_message(
        thread_id,
        "Assistant",
        response.content,
    )

    return {
        "answer": response.content,
        "sources": [
            {
                "page": d.metadata.get("page", "Unknown"),
                "content": d.page_content[:250],
            }
            for d in docs
        ],
    }