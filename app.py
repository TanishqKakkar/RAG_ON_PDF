from flask import Flask, request, jsonify
import fitz
import faiss
import pickle
import numpy as np
import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from groq import Groq

# =====================================
# Flask App
# =====================================
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# =====================================
# Load Environment Variables
# =====================================
load_dotenv()

# =====================================
# Groq Client
# =====================================
client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)

# =====================================
# Embedding Model
# =====================================
embed_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# =====================================
# Home Route
# =====================================
@app.route("/")
def home():

    return jsonify(
        {
            "message": "PDF RAG API Running"
        }
    )

# =====================================
# Upload PDF Route
# =====================================
@app.route(
    "/upload",
    methods=["POST"]
)
def upload_pdf():

    try:

        if "file" not in request.files:

            return jsonify(
                {
                    "error":
                    "No file uploaded"
                }
            ), 400

        file = request.files["file"]

        if file.filename == "":

            return jsonify(
                {
                    "error":
                    "No file selected"
                }
            ), 400

        # Save uploaded file
        filepath = os.path.join(
            UPLOAD_FOLDER,
            "current.pdf"
        )

        file.save(filepath)

        print("\nPDF uploaded")

        # =============================
        # Read PDF
        # =============================
        doc = fitz.open(filepath)

        text = ""

        for page in doc:

            text += page.get_text()

        doc.close()

        print(
            f"Characters extracted: {len(text)}"
        )

        # =============================
        # Generate Summary
        # =============================
        summary_prompt = f"""
Summarize this document in 5 bullet points.

Document:

{text[:10000]}
"""

        summary_response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": summary_prompt
                }
            ],

            temperature=0
        )

        summary = (
            summary_response
            .choices[0]
            .message.content
        )

        # =============================
        # Suggested Questions
        # =============================
        question_prompt = f"""
Generate 5 useful questions
that a user may ask
about this document.

Return only the questions.

Document:

{text[:10000]}
"""

        question_response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": question_prompt
                }
            ],

            temperature=0
        )

        suggested_questions = (
            question_response
            .choices[0]
            .message.content
        )

        # =============================
        # Chunking
        # =============================
        chunk_size = 1000
        overlap = 200

        chunks = []

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunks.append(
                text[start:end]
            )

            start += (
                chunk_size - overlap
            )

        print(
            f"Chunks created: {len(chunks)}"
        )

        # =============================
        # Embeddings
        # =============================
        embeddings = embed_model.encode(
            chunks
        )

        embeddings = np.array(
            embeddings
        ).astype(
            "float32"
        )

        # =============================
        # FAISS
        # =============================
        index = faiss.IndexFlatL2(
            embeddings.shape[1]
        )

        index.add(
            embeddings
        )

        # Save FAISS
        faiss.write_index(
            index,
            "index.faiss"
        )

        # Save Chunks
        with open(
            "chunks.pkl",
            "wb"
        ) as f:

            pickle.dump(
                chunks,
                f
            )

        print(
            "Index saved successfully"
        )

        return jsonify(
            {
                "message":
                "PDF indexed successfully",

                "chunks":
                len(chunks),

                "summary":
                summary,

                "suggested_questions":
                suggested_questions
            }
        )

    except Exception as e:

        return jsonify(
            {
                "error":
                str(e)
            }
        ), 500


# =====================================
# Ask Route
# =====================================
@app.route(
    "/ask",
    methods=["POST"]
)
def ask_question():

    try:

        if not os.path.exists(
            "index.faiss"
        ):

            return jsonify(
                {
                    "error":
                    "Upload a PDF first"
                }
            ), 400

        data = request.get_json()

        if not data:

            return jsonify(
                {
                    "error":
                    "No JSON received"
                }
            ), 400

        question = data.get(
            "question"
        )

        if not question:

            return jsonify(
                {
                    "error":
                    "Question required"
                }
            ), 400

        print("\n" + "=" * 80)
        print("QUESTION:")
        print(question)

        # =============================
        # Load Index
        # =============================
        index = faiss.read_index(
            "index.faiss"
        )

        with open(
            "chunks.pkl",
            "rb"
        ) as f:

            chunks = pickle.load(f)

        # =============================
        # Query Embedding
        # =============================
        query_embedding = embed_model.encode(
            [question]
        )

        query_embedding = np.array(
            query_embedding
        ).astype(
            "float32"
        )

        # =============================
        # Retrieval
        # =============================
        k = 5

        distances, indices = index.search(
            query_embedding,
            k
        )

        retrieved_chunks = []

        print("\nRetrieved Chunks:")

        for idx in indices[0]:

            retrieved_chunks.append(
                chunks[idx]
            )

            print("-" * 50)
            print(
                chunks[idx][:300]
            )

        context = "\n\n".join(
            retrieved_chunks
        )

        # =============================
        # Prompt
        # =============================
        prompt = f"""
You are a helpful assistant.

Answer ONLY from the context.

If the answer cannot be found
in the context, reply exactly:

I could not find this in the document.

Context:
{context}

Question:
{question}
"""

        # =============================
        # Groq Response
        # =============================
        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0
        )

        answer = (
            response
            .choices[0]
            .message.content
        )

        print("\nANSWER:")
        print(answer)

        return jsonify(
    {
        "question": question,
        "answer": answer,
        "sources": retrieved_chunks
    }
)

    except Exception as e:

        return jsonify(
            {
                "error":
                str(e)
            }
        ), 500


# =====================================
# Run Flask
# =====================================
if __name__ == "__main__":

    app.run(
    debug=True,
    use_reloader=False
)