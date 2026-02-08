## Fine-tuning (Google Colab)

Fine-tuning was performed on Google Colab due to local hardware constraints.

### Training
- Method: LoRA (behavioral fine-tuning)
- Base model: phi-3-mini
- Objective:
  - Improve answer structure
  - Enforce scope adherence
  - Improve refusal behavior in medical queries

Training code is provided in `colab_finetune.ipynb`.

### Inference
Inference is handled via a lightweight FastAPI service running in Colab,
which exposes the fine-tuned model through an HTTP endpoint.

The local RAG backend calls this endpoint for fine-tuned generation.

### Dataset
Only a small dataset sample is included for illustration.
Full training data is excluded intentionally.
