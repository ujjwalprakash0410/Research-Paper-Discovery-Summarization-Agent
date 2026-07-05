from collections import defaultdict

chat_history = defaultdict(list)


def add_message(thread_id: str, role: str, content: str):
    chat_history[thread_id].append(
        {
            "role": role,
            "content": content,
        }
    )


def get_history(thread_id: str):
    return chat_history[thread_id]