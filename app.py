import streamlit as st
from rag_backend import build_rag_pipeline

# MUST BE FIRST
st.set_page_config(page_title="Defense SOP Intelligence Assistant")

# Background + overlay
st.markdown("""
<style>

/* PREMIUM DEFENSE BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: 
        linear-gradient(
            rgba(0,0,0,0.75),
            rgba(0,0,0,0.9)
        ),
        url("https://images.unsplash.com/photo-1535223289827-42f1e9919769");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* CENTER PANEL */
.block-container {
    max-width: 850px;
    margin: auto;
    background: rgba(0,0,0,0.6);
    backdrop-filter: blur(10px);
    padding: 2rem;
    border-radius: 15px;
}

/* ANSWER BOX */
.answer-box {
    background: rgba(0,0,0,0.75);
    padding: 15px;
    border-radius: 10px;
    border-left: 4px solid #00ffcc;
    color: white;
    box-shadow: 0 0 12px rgba(0,255,204,0.2);
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