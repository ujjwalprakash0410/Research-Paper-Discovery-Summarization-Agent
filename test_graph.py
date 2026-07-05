from graph import graph
from langgraph.types import Command

config = {
    "configurable": {
        "thread_id": "research-session-1"
    }
}

initial_state = {
    "query": "Large Language Models",

    "papers": [],
    "selected_index": None,
    "selected_paper": None,

    "summary": "",

    "vector_store_path": "",

    "messages": [],

    "qa_query": "What personality traits were evaluated?",

    "answer": ""
}

print("=" * 80)
print("STEP 1 : SEARCH")
print("=" * 80)

result = graph.invoke(
    initial_state,
    config=config
)

# Graph pauses at first interrupt
print(result)

print("\n")

paper_number = input("Select paper number: ")

print("\n")
print("=" * 80)
print("STEP 2 : PROCESS PAPER")
print("=" * 80)

result = graph.invoke(
    Command(resume=paper_number),
    config=config
)

print("\n")
print("=" * 80)
print("SUMMARY")
print("=" * 80)

print(result["summary"])

print("\n")
print("=" * 80)
print("QA ANSWER")
print("=" * 80)

print(result["answer"])

print("\n")
print("=" * 80)
print("SOURCES")
print("=" * 80)

for source in result["messages"]:
    print(f"Page {source['page']}")
    print(source["content"])
    print("-" * 80)

print("\n")

save_choice = input("Save this paper? (yes/no): ")

print("\n")
print("=" * 80)
print("STEP 3 : SAVE")
print("=" * 80)

result = graph.invoke(
    Command(resume=save_choice),
    config=config
)

print("\n")

if save_choice.lower() == "yes":
    print("✅ Paper saved successfully.")
else:
    print("❌ Paper not saved.")

print("\n")

print("=" * 80)
print("WORKFLOW COMPLETE")
print("=" * 80)