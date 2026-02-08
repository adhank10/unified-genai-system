# Evaluation

This project evaluates LLM systems using **heuristic, system-level diagnostics** rather than classical NLP benchmarks.

---

## Metrics Used

- **Faithfulness**: Whether answers are grounded in retrieved sources
- **Scope adherence**: Avoidance of overreach beyond the question
- **Refusal behavior**: Correct handling of out-of-context queries
- **Answer structure**: Conciseness and clarity
- **Latency**: End-to-end response time

---

## Why Not BLEU / ROUGE?

Traditional NLP metrics are not suitable for evaluating open-ended LLM behavior,
especially in RAG and instruction-following systems.

---

## Key Observation

Behavioral fine-tuning improves safety and scope control while preserving factual grounding via RAG.
