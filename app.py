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
</style>
""", unsafe_allow_html=True)

# UI
st.title("🛡️ Defense SOP Intelligence Assistant")
st.caption("RAG-based SOP retrieval system")
st.info("Uses public SOP documents for decision support.")

# Load pipeline
@st.cache_resource
def load_pipeline():
    return build_rag_pipeline()

qa = load_pipeline()

# Input
query = st.text_input("Ask a question:")

# Output
if query:
    with st.spinner("Searching..."):
        result = qa(query)

        # Answer
        st.subheader("Answer")
        st.markdown(
            f'<div class="answer-box">{result["result"]}</div>',
            unsafe_allow_html=True
        )

        # Sources (FIXED - NO DUPLICATES)
        st.subheader("Sources")

        if result["source_documents"]:
            shown = set()   # ✅ removes duplicates

            for doc in result["source_documents"]:
                source = doc.metadata.get("source", "Unknown")

                if source not in shown:
                    st.markdown(f"• **{source}**")
                    shown.add(source)

        else:
            st.write("No sources found.")