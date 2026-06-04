# 🤖 PDF RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF documents and ask questions based on the document content.

The system extracts text from PDFs, converts the content into embeddings, stores them in a FAISS vector database, retrieves relevant chunks based on user queries, and generates context-aware answers using a Large Language Model (LLM).

---

# 🚀 Features

* 📄 Upload PDF documents
* 🔍 Semantic search using embeddings
* 🧠 Retrieval-Augmented Generation (RAG)
* 🤖 LLM-powered question answering
* 📚 Source chunk visualization
* 📄 Automatic document summary generation
* 💡 Suggested questions generation
* 💬 Interactive chatbot interface
* 🗑 Clear chat functionality
* 🔄 Reset application functionality

---

# 🏗 Architecture

User
↓
Streamlit Frontend
↓
Flask Backend API
↓
PDF Processing
↓
Chunking
↓
Sentence Transformers Embeddings
↓
FAISS Vector Database
↓
Top-K Retrieval
↓
Groq LLM
↓
Answer Generation

---

# 🛠 Tech Stack

## Frontend

* Streamlit

## Backend

* Flask

## LLM

* Groq API
* Llama 3.3 70B Versatile

## Embeddings

* Sentence Transformers
* all-MiniLM-L6-v2

## Vector Database

* FAISS

## PDF Processing

* PyMuPDF (fitz)

---

# 📂 Project Structure

```text
RAG_CHATBOT/

│
├── app.py
├── frontend.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── uploads/
│
├── index.faiss
├── chunks.pkl

```

---

# ⚙ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/pdf-rag-chatbot.git

cd pdf-rag-chatbot
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root directory.

```env
GROQ_API_KEY=your_groq_api_key
```

---

# ▶ Running the Application

## Start Backend

```bash
python app.py
```

Backend runs on:

```text
http://127.0.0.1:5000
```

---

## Start Frontend

```bash
streamlit run frontend.py
```

Frontend runs on:

```text
http://localhost:8501
```

---

# 📖 How It Works

### Step 1: Upload PDF

The uploaded PDF is processed using PyMuPDF and converted into text.

### Step 2: Chunking

The extracted text is divided into overlapping chunks.

### Step 3: Embedding Generation

Each chunk is converted into vector embeddings using Sentence Transformers.

### Step 4: Vector Storage

Embeddings are stored inside a FAISS index.

### Step 5: Query Processing

The user question is embedded using the same embedding model.

### Step 6: Retrieval

Top-K most relevant chunks are retrieved from FAISS.

### Step 7: Answer Generation

Retrieved chunks are passed to the Groq LLM, which generates a context-aware answer.

---

# 📸 Screenshots

Add screenshots here after deployment.

### Home Page

<img width="1911" height="882" alt="image" src="https://github.com/user-attachments/assets/961d3cf0-e72a-42d7-bf7d-f5f67d6c242d" />


### Upload PDF

<img width="409" height="362" alt="image" src="https://github.com/user-attachments/assets/21c434ad-7ef0-4e45-ba80-25e01e0bff53" />


### Chat Interface

<img width="1151" height="623" alt="image" src="https://github.com/user-attachments/assets/6e198591-a124-4cbb-a47a-61fda022056c" />


### Sources

<img width="1240" height="607" alt="image" src="https://github.com/user-attachments/assets/e298d612-e1f3-4de4-b5de-9212e8f0cb05" />


---

# 🎯 Future Improvements

* Multi-PDF support
* Hybrid Search (FAISS + BM25)
* Re-ranking using Cross Encoders
* OCR support for scanned PDFs
* User authentication
* Cloud deployment
* Conversation memory
* Citation-aware responses

---

# 📄 License

This project is open-source and available under the MIT License.

---

# 👨‍💻 Author

Tanishq Kakkar

B.Tech CSE (AI & ML)

Bennett University
