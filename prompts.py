from langchain_core.prompts import ChatPromptTemplate

SUMMARY_PROMPT = ChatPromptTemplate.from_template(
"""
You are an expert research paper analyst.

Use ONLY the retrieved context.

Summarize the paper in the following format.

Problem

Method

Results

Limitations

Future Work

Context

{context}
"""
)

QA_PROMPT = ChatPromptTemplate.from_template("""
You are an expert research assistant.

Answer ONLY from the provided context.

If the answer is not present, say:
"I could not find the answer in the paper."

Context:
{context}

Question:
{question}
""")