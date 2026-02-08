import streamlit as st
import requests
import time

# -----------------------------
# CONFIG
# -----------------------------
PROMPT_BACKEND = "http://127.0.0.1:8000"
RAG_BACKEND = "http://127.0.0.1:8001"

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(page_title="Unified GenAI System", layout="wide")
st.title("🧠 Unified GenAI System")
st.caption("Prompt • RAG • Fine-tuned RAG • Evaluation")

# -----------------------------
# MODE SELECTION
# -----------------------------
mode = st.radio(
    "Choose what you want to do",
    [
        "Simple Chatbot",
        "RAG Chatbot",
        "Fine-tuned RAG Chatbot",
        "Compare RAG vs Fine-tuned",
    ],
    horizontal=True,
)

st.divider()

# -----------------------------
# DOCUMENT UPLOAD (RAG MODES)
# -----------------------------
if mode != "Simple Chatbot":
    st.subheader("📄 Upload Document (for RAG)")
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

    if uploaded_file:
        with st.spinner("Ingesting document..."):
            files = {"file": uploaded_file}
            r = requests.post(f"{RAG_BACKEND}/ingest", files=files)
            if r.status_code == 200:
                st.success("Document ingested successfully")
            else:
                st.error("Failed to ingest document")

st.divider()

# -----------------------------
# QUERY INPUT
# -----------------------------
query = st.text_area("Enter your question", height=120)
ask = st.button("Ask")

# -----------------------------
# EVALUATION HELPERS
# -----------------------------
def faithfulness_label(sources):
    return "✅ Grounded" if sources else "⚠️ Ungrounded"

def scope_label(answer, query):
    overreach_terms = ["side effect", "research", "gene", "dosage"]
    if any(t in answer.lower() for t in overreach_terms) and "side" not in query.lower():
        return "Low"
    return "High"

def refusal_label(answer):
    return "✅ Correct" if "i cannot" in answer.lower() or "i don't know" in answer.lower() else "❌ Incorrect"

def structure_label(answer):
    return "Concise" if len(answer.split()) < 60 else "Verbose"

# -----------------------------
# MODE LOGIC
# -----------------------------
if ask and query.strip():

    # -------- MODE 1: PROMPT --------
    if mode == "Simple Chatbot":
        with st.spinner("Thinking..."):
            r = requests.post(
                f"{PROMPT_BACKEND}/chat/prompt",
                json={"query": query},
                timeout=60,
            )
            answer = r.json().get("answer", "")

        st.subheader("🤖 Response")
        st.write(answer)

    # -------- MODE 2: RAG --------
    elif mode == "RAG Chatbot":
        with st.spinner("Retrieving & answering..."):
            r = requests.post(
                f"{RAG_BACKEND}/rag/chat",
                json={"query": query},
                timeout=120,
            )
            data = r.json()

        st.subheader("🤖 Answer")
        st.write(data.get("answer", ""))

        st.subheader("📚 Sources")
        for src in data.get("sources", []):
            st.markdown(f"- **{src['document_id']} | chunk {src['chunk_index']}**")

    # -------- MODE 3: FINE-TUNED RAG --------
    elif mode == "Fine-tuned RAG Chatbot":
        with st.spinner("Retrieving & answering (fine-tuned)..."):
            r = requests.post(
                f"{RAG_BACKEND}/rag/chat/finetuned",
                json={"query": query},
                timeout=180,
            )
            data = r.json()

        raw_answer = data.get("answer", "")

        # UX cleanup
        if "Answer:" in raw_answer:
            clean_answer = raw_answer.split("Answer:")[-1].strip()
        else:
            clean_answer = raw_answer.strip()

        st.subheader("🤖 Answer")
        st.write(clean_answer)

        st.subheader("📚 Sources")
        for src in data.get("sources", []):
            st.markdown(f"- **{src['document_id']} | chunk {src['chunk_index']}**")

    # -------- MODE 4: COMPARISON + EVALUATION --------
    elif mode == "Compare RAG vs Fine-tuned":
        with st.spinner("Running comparison..."):
            start = time.time()
            r = requests.post(
                f"{RAG_BACKEND}/rag/compare",
                json={"query": query},
                timeout=180,
            )
            latency = round(time.time() - start, 2)
            data = r.json()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🟡 Base RAG")
            st.write(data.get("base_answer", ""))

        with col2:
            st.subheader("🔵 Fine-tuned RAG")
            st.write(data.get("finetuned_answer", ""))

        st.subheader("📚 Sources")
        for src in data.get("sources", []):
            st.markdown(f"- **{src['document_id']} | chunk {src['chunk_index']}**")

        # -----------------------------
        # EVALUATION SUMMARY
        # -----------------------------
        st.subheader("🧪 Evaluation Summary")

        evaluation = {
            "Metric": [
                "Faithfulness",
                "Scope adherence",
                "Refusal behavior",
                "Answer structure",
                "Latency",
            ],
            "Base RAG": [
                faithfulness_label(data["sources"]),
                scope_label(data["base_answer"], query),
                refusal_label(data["base_answer"]),
                structure_label(data["base_answer"]),
                f"{latency}s",
            ],
            "Fine-tuned RAG": [
                faithfulness_label(data["sources"]),
                scope_label(data["finetuned_answer"], query),
                refusal_label(data["finetuned_answer"]),
                structure_label(data["finetuned_answer"]),
                f"{latency}s",
            ],
        }
        st.success("Evaluation block reached")
        st.table(evaluation)
