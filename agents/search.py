import arxiv

from models import Paper
from state import GraphState

from config import settings


client = arxiv.Client()


def search_arxiv(query: str):

    search = arxiv.Search(
        query=query,
        max_results=settings.max_search_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    papers = []

    for result in client.results(search):

        papers.append(

            Paper(

                title=result.title,

                authors=[author.name for author in result.authors],

                abstract=result.summary,

                published=str(result.published.date()),

                pdf_url=result.pdf_url,

                source="arxiv",

            )

        )

    return papers


def search_node(state: GraphState):

    query = state["query"]

    papers = search_arxiv(query)

    return {

        "papers": papers

    }