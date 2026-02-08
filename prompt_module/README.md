# Prompt Module

This module provides a **baseline prompt-only chatbot** using a local LLM.

---

## Purpose

- Establish baseline LLM behavior
- Serve as a reference point for RAG and fine-tuned RAG
- No retrieval, no fine-tuning

---

## Tech Stack

- FastAPI
- Ollama (local LLM)

---

## Endpoint

- `POST /chat/prompt`
  - Input: user query
  - Output: raw model response

---

## Usage

```bash
uvicorn app:app --reload --port 8000
