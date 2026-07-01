# 🤖 PDF RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that lets users upload PDF documents and ask questions grounded in their content — with source citations, auto-generated summaries, and suggested questions.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3-orange?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

---

## Overview

The system extracts text from uploaded PDFs, converts the content into embeddings, stores them in a FAISS vector database, retrieves the most relevant chunks for a user's query, and generates context-aware answers using an LLM.

## Features

- 📄 Upload PDF documents
- 🔍 Semantic search using embeddings
- 🧠 Retrieval-Augmented Generation (RAG)
- 🤖 LLM-powered question answering
- 📚 Source chunk visualization
- 📄 Automatic document summary generation
- 💡 Suggested questions generation
- 💬 Interactive chatbot interface
- 🗑 Clear chat / reset application

## Architecture

```
User → Streamlit Frontend → Flask Backend API → PDF Processing
     → Chunking → Sentence Transformer Embeddings → FAISS Vector DB
     → Top-K Retrieval → Groq LLM → Answer Generation
```

## Tech Stack

| Layer | Tech |
|---|---|
| Frontend | Streamlit |
| Backend | Flask |
| LLM | Groq API — LLaMA 3.3 70B Versatile |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Vector Database | FAISS |
| PDF Processing | PyMuPDF (fitz) |

## Project Structure

```
RAG_ON_PDF/
├── app.py              # Flask backend
├── frontend.py         # Streamlit frontend
├── requirements.txt
├── README.md
├── .gitignore
├── uploads/
├── index.faiss          # Vector index
└── chunks.pkl            # Stored text chunks
```

## Setup

```bash
git clone https://github.com/TanishqKakkar/RAG_ON_PDF.git
cd RAG_ON_PDF
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key
```

## Run

**Start backend:**
```bash
python app.py
# runs on http://127.0.0.1:5000
```

**Start frontend:**
```bash
streamlit run frontend.py
# runs on http://localhost:8501
```

## How It Works

1. **Upload PDF** — processed via PyMuPDF and converted to text
2. **Chunking** — text split into overlapping chunks
3. **Embedding** — each chunk converted to vector embeddings
4. **Vector Storage** — embeddings stored in a FAISS index
5. **Query Processing** — user question embedded with the same model
6. **Retrieval** — top-K relevant chunks retrieved from FAISS
7. **Answer Generation** — retrieved chunks passed to Groq LLM for a context-aware answer

## Future Improvements

- Multi-PDF support
- Hybrid search (FAISS + BM25)
- Re-ranking using cross-encoders
- OCR support for scanned PDFs
- User authentication
- Cloud deployment
- Conversation memory
- Citation-aware responses

## Author

**Tanishq Kakkar** — B.Tech CSE (AI & ML), Bennett University

## License

MIT License
