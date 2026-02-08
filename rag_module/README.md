# RAG Module

This module implements **Retrieval-Augmented Generation (RAG)** with document grounding and source attribution.

---

## Purpose

- Reduce hallucinations
- Ensure answers are grounded in provided documents
- Enable traceability via sources
- Compare base vs fine-tuned generation behavior

---

## RAG Pipeline

1. Document ingestion and chunking
2. Embedding using SentenceTransformers
3. Vector search using ChromaDB
4. Grounded prompt construction
5. LLM response generation

---

## Tech Stack

- FastAPI
- SentenceTransformers
- ChromaDB
- Ollama

---

## Endpoints

- `POST /ingest` — Upload and embed documents
- `POST /rag/chat` — Base RAG generation
- `POST /rag/chat/finetuned` — Fine-tuned RAG generation
- `POST /rag/compare` — Side-by-side comparison

---

## Usage

```bash
uvicorn app:app --reload --port 8001

Notes

Vector databases and embeddings are created at runtime and are not committed to the repository.