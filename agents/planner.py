from state import GraphState


def planner_node(state: GraphState):

    query = state["query"].strip()

    if not query:
        raise ValueError("Query cannot be empty.")

    return {
        "query": query
    }