import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader

def build_rag_pipeline():
    documents = []

    # Load PDFs
    for file in os.listdir("data"):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(f"data/{file}")
            docs = loader.load()

            # Add source metadata
            for d in docs:
                d.metadata["source"] = file

            documents.extend(docs)

    # Split documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    # Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Vector DB
    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Query function
    def simple_answer(query):
        docs = retriever.get_relevant_documents(query)
        return {
            "result": docs[0].page_content if docs else "No answer found.",
            "source_documents": docs
        }

    return simple_answer