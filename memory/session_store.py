session_store = {}


def save_session(thread_id: str, vector_store_path: str):
    session_store[thread_id] = vector_store_path


def get_vector_store(thread_id: str):
    return session_store.get(thread_id)