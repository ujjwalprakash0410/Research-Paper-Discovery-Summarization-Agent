from langgraph.types import interrupt

from state import GraphState


def approval_node(state: GraphState):

    papers = state["papers"]

    print("\nAvailable Papers\n")

    for idx, paper in enumerate(papers):

        print(f"{idx + 1}. {paper.title}")

    selection = interrupt(
        {
            "message": "Select a paper number",
            "papers": [paper.model_dump() for paper in papers],
        }
    )

    index = int(selection) - 1

    return {

        "selected_index": index,

        "selected_paper": papers[index]

    }