from typing import TypedDict, Any, Optional
from models import Paper


class GraphState(TypedDict):
    # User input
    query: str

    # Search Agent output
    papers: list[Paper]

    # Human selection
    selected_index: Optional[int]
    selected_paper: Optional[Paper]

    # Summarizer Agent output
    summary: str

    # Shared RAG retriever
    vector_store_path: str

    # QA conversation
    messages: list

    # Latest user question
    qa_query: str

    # Latest grounded answer
    answer: str