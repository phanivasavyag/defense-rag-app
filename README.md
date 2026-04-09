# 🛡️ Defense SOP Intelligence Assistant

## 🚀 Live Demo
👉 https://defense-rag-app-6lbwuhceyf7tlbswy3bkjk.streamlit.app/

---

## 📌 Overview
This project is a **Retrieval-Augmented Generation (RAG) system** designed to assist in retrieving relevant Defense Standard Operating Procedures (SOPs) using natural language queries.

Users can ask questions, and the system returns:
- 📌 Relevant answers
- 📄 Source documents used for retrieval

---

## ⚙️ Features
- 🔍 Semantic search over SOP documents
- 📄 Source-aware responses
- ⚡ Fast retrieval using FAISS vector database
- 🧠 Embeddings using Sentence Transformers
- 🎨 Clean Streamlit UI with military theme
- 🌐 Live deployed application

---

## 🧠 Tech Stack
- Python
- Streamlit
- LangChain
- FAISS
- Sentence Transformers

---

## 📂 How It Works
1. PDFs are loaded from the `data/` folder
2. Text is split into smaller chunks
3. Embeddings are generated using transformer models
4. FAISS stores vectors for fast similarity search
5. User query retrieves top relevant chunks
6. System displays answer + source documents

---

## 🧪 Sample Questions
Try asking:
- What is the procedure for emergency evacuation?
- How should personnel respond to security threats?
- What are the standard communication protocols?
- What steps are taken during disaster management?
- What are safety guidelines for field operations?

---

## 🎯 Use Cases
- Defense SOP retrieval
- Emergency response guidance
- Knowledge management systems
- Document-based Q&A systems

---

## 👨‍💻 Author
Phani Vasavya Gajula  
🔗 https://github.com/phanivasavyag

---

## ⭐ Note
This project uses publicly available SOP-style documents for demonstration purposes.