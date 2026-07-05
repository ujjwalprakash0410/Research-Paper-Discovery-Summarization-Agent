from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from state import GraphState

from agents.planner import planner_node
from agents.search import search_node
from agents.approval import approval_node
from agents.document_processor import processor_node
from agents.summarizer import summarizer_node
from agents.qa import qa_node
from agents.save import save_node

# Create graph builder
builder = StateGraph(GraphState)

# -----------------------
# Add Nodes
# -----------------------

builder.add_node("planner", planner_node)
builder.add_node("search", search_node)
builder.add_node("approval", approval_node)
builder.add_node("document_processor", processor_node)
builder.add_node("summarizer", summarizer_node)
builder.add_node("save", save_node)

# -----------------------
# Add Edges
# -----------------------

builder.add_edge(START, "planner")
builder.add_edge("planner", "search")
builder.add_edge("search", "approval")
builder.add_edge("approval", "document_processor")
builder.add_edge("document_processor", "summarizer")
builder.add_edge("summarizer", "save")
builder.add_edge("save", END)
# -----------------------
# Compile
# -----------------------

memory = MemorySaver()

graph = builder.compile(
    checkpointer=memory
)