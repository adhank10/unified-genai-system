# Frontend (Streamlit)

This module provides a unified user interface for interacting with all GenAI modes.

---

## Features

- Prompt-only chatbot
- RAG chatbot with sources
- Fine-tuned RAG chatbot
- Side-by-side comparison with evaluation summary

---

## Tech Stack

- Streamlit
- Requests

---

## Usage

```bash
streamlit run app.py
Notes
The frontend acts purely as a client and does not run any models.
All inference happens via backend APIs.