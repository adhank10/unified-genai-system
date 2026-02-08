from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import chromadb
import requests

# =========================
# App
# =========================
app = FastAPI(title="RAG Module API")

# =========================
# Base LLM (Ollama)
# =========================
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "phi3:mini"

# =========================
# Fine-tuned Model (Colab)
# =========================
FINETUNED_API_URL = "https://prolongedly-unrevelling-lorri.ngrok-free.dev/chat"

# =========================
# Embedding Model
# =========================
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# =========================
# Vector DB
# =========================
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="rag_chunks")

# =========================
# Request / Response Models
# =========================
class IngestResponse(BaseModel):
    document_id: str
    message: str


class QueryRequest(BaseModel):
    query: str


class RAGChatRequest(BaseModel):
    query: str


# =========================
# Health Check
# =========================
@app.get("/")
def root():
    return {"status": "ok", "message": "RAG backend running"}


# =========================
# Chunking
# =========================
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = max(0, end - overlap)

    return chunks


# =========================
# Prompt Builder (SHARED)
# =========================
def build_grounded_prompt(context: str, query: str) -> str:
    return f"""You are a medical assistant.
Use the context below to answer the question concisely and clearly.

Context:
{context}

Question:
{query}

Answer:
"""



# =========================
# Ingest + Embed
# =========================
@app.post("/ingest", response_model=IngestResponse)
async def ingest_document(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")

    document_id = file.filename
    chunks = chunk_text(text)
    embeddings = embedding_model.encode(chunks).tolist()

    ids = []
    metadatas = []

    for idx, chunk in enumerate(chunks):
        ids.append(f"{document_id}_chunk_{idx}")
        metadatas.append({
            "document_id": document_id,
            "chunk_index": idx,
            "text": chunk
        })

    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return IngestResponse(
        document_id=document_id,
        message=f"Document ingested with {len(chunks)} chunks"
    )


# =========================
# Retrieval Only
# =========================
@app.post("/query")
def query_documents(req: QueryRequest):
    query_embedding = embedding_model.encode([req.query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    return {
        "query": req.query,
        "results": results["metadatas"]
    }


# =========================
# Shared Retrieval Logic (DEDUPED)
# =========================
def retrieve_context(query: str, n_results: int = 3):
    query_embedding = embedding_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )

    seen = set()
    retrieved_chunks = []

    for item in results["metadatas"][0]:
        text = item["text"].strip()
        if text not in seen:
            retrieved_chunks.append(text)
            seen.add(text)

    context = "\n\n".join(retrieved_chunks)
    return context, results["metadatas"][0]


# =========================
# Base RAG (UNCHANGED BEHAVIOR)
# =========================
@app.post("/rag/chat")
def rag_chat(req: RAGChatRequest):
    context, sources = retrieve_context(req.query)

    prompt = build_grounded_prompt(context, req.query)

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": 200}
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        return {"error": response.text}

    return {
        "question": req.query,
        "answer": response.json().get("response", "").strip(),
        "sources": sources
    }


# =========================
# Fine-tuned RAG (FIXED)
# =========================
@app.post("/rag/chat/finetuned")
def rag_chat_finetuned(req: RAGChatRequest):
    context, sources = retrieve_context(req.query)

    prompt = build_grounded_prompt(context, req.query)

    response = requests.post(
        FINETUNED_API_URL,
        json={"prompt": prompt},
        timeout=180
    )

    if response.status_code != 200:
        return {"error": response.text}

    return {
        "answer": response.json()["response"],
        "sources": sources
    }


# =========================
# Compare Base RAG vs Fine-tuned RAG
# =========================
@app.post("/rag/compare")
def compare_rag(req: RAGChatRequest):
    # 1. Embed query
    query_embedding = embedding_model.encode([req.query]).tolist()

    # 2. Retrieve ONCE
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    retrieved_chunks = [
        item["text"] for item in results["metadatas"][0]
    ]

    context = "\n\n".join(retrieved_chunks)
    prompt = build_grounded_prompt(context, req.query)

    # 3. Base RAG (Ollama)
    base_payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": 200}
    }

    base_response = requests.post(
        OLLAMA_URL,
        json=base_payload,
        timeout=120
    )

    base_answer = base_response.json().get("response", "").strip()

    # 4. Fine-tuned RAG (Colab)
    ft_response = requests.post(
        FINETUNED_API_URL,
        json={"prompt": prompt},
        timeout=180
    )

    finetuned_raw = ft_response.json().get("response", "").strip()

    # 🔥 UX cleanup (same logic as frontend)
    if "Answer:" in finetuned_raw:
        finetuned_answer = finetuned_raw.split("Answer:")[-1].strip()
    else:
        finetuned_answer = finetuned_raw

    return {
        "query": req.query,
        "base_answer": base_answer,
        "finetuned_answer": finetuned_answer,
        "sources": results["metadatas"][0]
    }
