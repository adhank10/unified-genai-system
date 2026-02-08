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
This repository is intended to demonstrate **production-style GenAI system design**.


## System Workflow (Mermaid)

```mermaid
flowchart TD
    User --> Frontend[Streamlit Frontend]

    %% RAG Mode
    Frontend -->|RAG Mode| RAG[RAG Backend<br/>FastAPI]
    RAG --> Embed[Embed Query<br/>SentenceTransformers]
    Embed --> VectorDB[Vector Search<br/>ChromaDB]
    VectorDB --> Retrieve[Retrieve Top-K Chunks]
    Retrieve --> PromptBuild[Build Grounded Prompt]

    %% Base RAG
    PromptBuild --> Phi3Base[Phi-3 Base Model<br/>Ollama]

    %% Fine-tuned RAG
    PromptBuild --> Phi3LoRA[Phi-3 with LoRA Adapter<br/>Colab API]

    %% Comparison Mode
    Frontend -->|Comparison Mode| Compare[Comparison Logic]
    Compare --> Phi3Base
    Compare --> Phi3LoRA
    Compare --> Eval[Side-by-side Answers<br/>Evaluation Metrics]

