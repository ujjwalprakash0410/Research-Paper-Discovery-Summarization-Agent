from pydantic import BaseModel
from typing import List, Optional


class Paper(BaseModel):
    title: str
    authors: List[str]
    abstract: str
    published: str
    pdf_url: str
    source: str
    score: Optional[float] = None

from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str


class SearchResponse(BaseModel):
    papers: list

class ApproveRequest(BaseModel):
    thread_id: str
    paper_number: int


class SaveRequest(BaseModel):
    thread_id: str
    decision: str


class AskRequest(BaseModel):
    thread_id: str
    question: str