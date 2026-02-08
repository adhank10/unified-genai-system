
# Fine-tuning Module (Google Colab)

This module documents the **behavioral fine-tuning process** using LoRA.

---

## Why Google Colab?

Fine-tuning was performed on Google Colab due to local hardware constraints.
Training and inference are intentionally decoupled from the local system.

---

## Training

- Base model: phi-3-mini
- Method: LoRA (PEFT)
- Objective:
  - Improve answer structure
  - Enforce scope adherence
  - Improve refusal behavior for medical queries

Training code is provided in `colab_finetune.ipynb`.

---

## Inference

The fine-tuned model is served via a lightweight FastAPI app running in Colab.
The local RAG backend calls this service over HTTP for fine-tuned generation.

---