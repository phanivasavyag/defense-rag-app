import streamlit as st
from rag_backend import build_rag_pipeline

# MUST BE FIRST
st.set_page_config(page_title="Defense SOP Intelligence Assistant")

# Background + overlay
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        rgba(0,0,0,0.6),
        rgba(0,0,0,0.6)
    ),
    url("https://static.vecteezy.com/system/resources/previews/060/002/644/non_2x/soldier-using-futuristic-hud-in-a-military-operation-at-sunset-free-photo.jpg");

    background-size: cover;
    background-position: center;
}

/* Center container */
.block-container {
    max-width: 800px;
    margin: auto;
    background-color: rgba(0,0,0,0.5);
    padding: 2rem;
    border-radius: 15px;
}

/* Answer box */
.answer-box {
    background-color: rgba(0,0,0,0.7);
    padding: 15px;
    border-radius: 10px;
    border-left: 4px solid #00ffcc;
    color: white;
}

/* FULL chat input container */
section[data-testid="stChatInput"] > div {
    border: 1px solid #00ffcc !important;
    border-radius: 12px !important;
    background: rgba(0, 0, 0, 0.6) !important;
}

/* Text area */
section[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: white !important;
    border: none !important;
    outline: none !important;
}

/* Remove red focus */
section[data-testid="stChatInput"] > div:focus-within {
    border: 1px solid #00ffcc !important;
    box-shadow: none !important;
}

/* Placeholder */
section[data-testid="stChatInput"] textarea::placeholder {
    color: #bbbbbb !important;
}

/* Send button */
section[data-testid="stChatInput"] button {
    background-color: #00ffcc !important;
    color: black !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# UI
st.title("Defense SOP Intelligence Assistant")
st.caption("RAG-based SOP retrieval system")
st.info("Uses public SOP documents for decision support.")

# Load pipeline
@st.cache_resource
def load_pipeline():
    return build_rag_pipeline()

qa = load_pipeline()

# Chat memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
query = st.chat_input("Ask your question...")

# Handle query
if query:
    questions = [q.strip() for q in query.split("\n") if q.strip()]

    for q in questions:
        with st.spinner(f"Searching for: {q}"):
            result = qa(q)

            st.session_state.chat_history.append({
                "question": q,
                "answer": result["result"],
                "sources": result["source_documents"]
            })

# Display chat history
for chat in st.session_state.chat_history:
    st.markdown(f"### You: {chat['question']}")

    st.markdown(
        f'<div class="answer-box">{chat["answer"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown("Sources:")

    if chat["sources"]:
        shown = set()

        for doc in chat["sources"]:
            source = doc.metadata.get("source", "Unknown")

            if source not in shown:
                st.markdown(f"- {source}")
                shown.add(source)
    else:
        st.write("No sources found.")

    st.markdown("---")