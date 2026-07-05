from llm import llm


def stream_llm(prompt):

    for chunk in llm.stream(prompt):

        if chunk.content:
            yield chunk.content