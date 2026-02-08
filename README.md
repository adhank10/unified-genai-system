# Unified GenAI System

A modular GenAI system demonstrating prompt-based interaction, Retrieval-Augmented Generation (RAG), and behavioral fine-tuning using LoRA, with clear evaluation of model behavior.

This project focuses on **system design, safety, and evaluation**, not just model performance.

---

## Key Capabilities

- Prompt-only chatbot (baseline)
- RAG chatbot with document grounding and source attribution
- Fine-tuned RAG chatbot with improved safety and scope control
- Side-by-side comparison with evaluation metrics

---

## Architecture Overview

- **Prompt Module**: Baseline LLM interaction (FastAPI + Ollama)
- **RAG Module**: Document-grounded QA using embeddings and vector search
- **Fine-tuning**: Behavioral LoRA fine-tuning (trained on Google Colab)
- **Frontend**: Streamlit UI to interact with all modes

---

## Evaluation Philosophy

This system evaluates LLMs using **behavioral and system-level diagnostics**:

- Faithfulness (grounding via sources)
- Scope adherence
- Refusal behavior
- Answer structure
- Latency

Classical NLP metrics such as BLEU or ROUGE are intentionally avoided, as they are not suitable for open-ended LLM systems.

---

## Notes

- Model weights, adapters, and vector databases are **not included** in this repository.
- Fine-tuning is performed externally (Google Colab) and accessed via API during inference.

---

## System Workflow

```mermaid
flowchart TD
    User --> Frontend

    Frontend -->|Prompt Mode| PromptAPI
    PromptAPI --> Ollama

    Frontend -->|RAG Mode| RAG
    RAG --> Embed
    Embed --> VectorDB
    VectorDB --> Retrieve
    Retrieve --> PromptBuild
    PromptBuild --> Phi 3

    Frontend -->|Fine-tuned RAG| RAG
    PromptBuild --> FineTunedAPI

    Frontend -->|Comparison| Compare
    Compare --> Phi 3
    Compare --> FineTunedAPI

This repository is intended to demonstrate **production-style GenAI system design**.
