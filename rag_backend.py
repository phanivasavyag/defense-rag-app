import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document

def build_rag_pipeline():
    documents = []

    # Load PDFs
    for file in os.listdir("data"):
        if file.endswith(".pdf"):
            reader = PdfReader(f"data/{file}")
            text = ""

            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text()

            # ✅ Attach metadata (file name)
            documents.append(
                Document(
                    page_content=text,
                    metadata={"source": file}
                )
            )

    # Split manually (IMPORTANT: keep metadata)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = []
    for doc in documents:
        split_texts = splitter.split_text(doc.page_content)

        for chunk in split_texts:
            chunks.append(
                Document(
                    page_content=chunk,
                    metadata=doc.metadata  # ✅ keep source
                )
            )

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