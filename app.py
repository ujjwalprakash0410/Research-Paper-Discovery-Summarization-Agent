import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Research Paper Discovery & Summarization Agent",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Research Paper Discovery & Summarization Agent")

# ------------------------
# Session State
# ------------------------

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

if "papers" not in st.session_state:
    st.session_state.papers = []

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ------------------------
# Sidebar
# ------------------------

with st.sidebar:

    st.title("Research Agent")

    st.markdown("---")

    if st.button("📚 Refresh Library"):

        response = requests.get(
            f"{API_URL}/library"
        )

        library = response.json()

        if not library:
            st.info("Library is empty.")

        else:

            st.success(f"{len(library)} saved papers")

            for paper in library:

                with st.expander(paper["title"]):

                    st.write("### Authors")
                    st.write(", ".join(paper["authors"]))

                    st.write("### Summary")
                    st.write(paper["summary"])

                    st.link_button(
                        "Open PDF",
                        paper["pdf_url"]
                    )

# ------------------------
# Search
# ------------------------

st.header("🔍 Search Papers")

query = st.text_input(
    "Research Topic",
    placeholder="Large Language Models"
)

if st.button("Search"):

    st.session_state.summary = ""
    st.session_state.chat_history = []

    with st.spinner("Searching papers..."):

        response = requests.post(
            f"{API_URL}/search",
            json={
                "query": query
            }
        )

        data = response.json()

        st.session_state.thread_id = data["thread_id"]
        st.session_state.papers = data["papers"]

        st.success(f"Found {len(data['papers'])} papers.")

# ------------------------
# Paper Selection
# ------------------------

if st.session_state.papers:

    titles = [
        paper["title"]
        for paper in st.session_state.papers
    ]

    selected = st.selectbox(
        "Choose a paper",
        titles
    )

    selected_paper = st.session_state.papers[
        titles.index(selected)
    ]

    with st.expander("Paper Details"):

        st.write("### Authors")
        st.write(", ".join(selected_paper["authors"]))

        st.write("### Published")
        st.write(selected_paper["published"])

        st.write("### Abstract")
        st.write(selected_paper["abstract"])

    if st.button("Generate Summary"):

        with st.spinner("Reading paper..."):

            response = requests.post(
                f"{API_URL}/approve",
                json={
                    "thread_id": st.session_state.thread_id,
                    "paper_number": titles.index(selected) + 1,
                },
            )

            result = response.json()

            st.session_state.summary = result["summary"]

# ------------------------
# Summary
# ------------------------

if st.session_state.summary:

    st.header("📝 Paper Summary")

    st.markdown(st.session_state.summary)

    col1, col2 = st.columns(2)

    with col1:

        if st.button("💾 Save Paper"):

            requests.post(
                f"{API_URL}/save",
                json={
                    "thread_id": st.session_state.thread_id,
                    "decision": "yes",
                },
            )

            st.success("Paper saved!")

    with col2:

        if st.button("❌ Don't Save"):

            requests.post(
                f"{API_URL}/save",
                json={
                    "thread_id": st.session_state.thread_id,
                    "decision": "no",
                },
            )

# ------------------------
# Chat
# ------------------------

if st.session_state.summary:

    st.header("💬 Chat with the Paper")

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    prompt = st.chat_input(
        "Ask anything about this paper..."
    )

    if prompt:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "thread_id": st.session_state.thread_id,
                        "question": prompt,
                    },
                )

                answer = response.json()["answer"]

                st.markdown(answer)

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )