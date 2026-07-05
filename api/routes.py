import uuid

from fastapi import APIRouter
from langgraph.types import Command
from fastapi.responses import StreamingResponse
from agents.summarizer import stream_summary

from graph import graph
from memory.store import MemoryStore
from models import (
    SearchRequest,
    ApproveRequest,
    SaveRequest,
)

router = APIRouter()

store = MemoryStore()


@router.get("/")
def home():
    return {
        "message": "Research Agent API Running"
    }


@router.post("/search")
def search(request: SearchRequest):

    thread_id = str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    state = {
        "query": request.query,
        "papers": [],
        "selected_index": None,
        "selected_paper": None,
        "summary": "",
        "vector_store_path": "",
        "messages": [],
        "qa_query": "",
        "answer": ""
    }

    result = graph.invoke(
        state,
        config=config
    )

    interrupt = result["__interrupt__"][0].value

    return {
        "thread_id": thread_id,
        "message": interrupt["message"],
        "papers": interrupt["papers"]
    }


@router.post("/approve")
def approve(request: ApproveRequest):

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    result = graph.invoke(
        Command(
            resume=str(request.paper_number)
        ),
        config=config
    )

    return {
        "summary": result["summary"],
        "answer": result["answer"],
        "sources": result["messages"]
    }

@router.post("/save")
def save(request: SaveRequest):

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    graph.invoke(
        Command(
            resume=request.decision
        ),
        config=config
    )

    return {
        "status": "success"
    }


@router.get("/library")
def library():

    return store.get_library()

@router.get("/stream-summary")
def stream_summary_api():

    generator = stream_summary(
        "vectorstore",
        "Large Language Models"
    )

    return StreamingResponse(
        generator,
        media_type="text/plain"
    )

@router.get("/health")
def health():
    return {
        "status": "healthy"
    }