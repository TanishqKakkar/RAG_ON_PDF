import streamlit as st
import requests

# ==========================
# Page Config
# ==========================
st.set_page_config(
    page_title="PDF RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)
# ==========================
# Session State
# ==========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "questions" not in st.session_state:
    st.session_state.questions = ""

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = ""

st.title("🤖 PDF RAG Chatbot")

if st.session_state.pdf_name:

    st.success(
        f"Loaded PDF: {st.session_state.pdf_name}"
    )

if st.session_state.summary:

    st.subheader(
        "📄 Document Summary"
    )

    st.write(
        st.session_state.summary
    )

if st.session_state.questions:

    st.subheader(
        "💡 Suggested Questions"
    )

    st.write(
        st.session_state.questions
    )



# ==========================
# Sidebar
# ==========================
with st.sidebar:

    st.header("⚙ Controls")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    if st.button("🔄 Reset Application"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.divider()

    st.header("📄 Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )

    if uploaded_file:

        if st.button("Process PDF"):

            with st.spinner(
                "Indexing PDF..."
            ):

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf"
                    )
                }

                response = requests.post(
                    "http://127.0.0.1:5000/upload",
                    files=files
                )

                result = response.json()

                st.success(
                    result["message"]
                )

                st.session_state.pdf_uploaded = True

                st.session_state.pdf_name = (
                    uploaded_file.name
                )

                st.session_state.summary = (
                    result["summary"]
                )

                st.session_state.questions = (
                    result["suggested_questions"]
                )

# ==========================
# Chat History
# ==========================
for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# ==========================
# Chat Input
# ==========================
if prompt := st.chat_input(
    "Ask a question from the PDF..."
):

    if not st.session_state.pdf_uploaded:

        st.warning(
            "Upload and process a PDF first."
        )

    else:

        # User message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # API call
        with st.spinner(
            "Thinking..."
        ):

            response = requests.post(
                "http://127.0.0.1:5000/ask",
                json={
                    "question": prompt
                }
            )

            result = response.json()

            answer = result["answer"]
            sources = result["sources"]

        # Assistant message
        with st.chat_message(
            "assistant"
        ):

            st.markdown(answer)

            with st.expander(
                 "📚 View Sources"
            ):

                for i, source in enumerate(
                    sources
                ):

                    st.markdown(
                        f"### Source {i+1}"
                    )

                    st.write(source)

                    st.divider()

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )