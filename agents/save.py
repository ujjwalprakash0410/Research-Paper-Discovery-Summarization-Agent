from langgraph.types import interrupt

from state import GraphState

from memory.store import MemoryStore

store = MemoryStore()


def save_node(state: GraphState):

    decision = interrupt(
        {
            "message": "Save this paper to your library? (yes/no)"
        }
    )

    if decision.lower() != "yes":
        return {}

    store.add_paper(
        state["selected_paper"],
        state["summary"]
    )

    return {}