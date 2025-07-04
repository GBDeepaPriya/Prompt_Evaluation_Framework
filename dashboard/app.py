import streamlit as st
import yaml
import os
import pandas as pd

# --- File paths ---
PROMPT_PATH = os.path.join("data", "prompts.yaml")
RESULTS_PATH = os.path.join("output", "results.csv")
REFINED_PROMPT_PATH = os.path.join("output", "refined_prompts.yaml")

# --- Streamlit Setup ---
st.set_page_config(page_title="PromptEval Dashboard", layout="wide")
st.title("📊 Prompt Evaluation  Dashboard")
st.markdown("---")

# --- Load Prompt Dataset ---
try:
    with open(PROMPT_PATH, "r") as f:
        prompts = yaml.safe_load(f) or []
except FileNotFoundError:
    st.error("❌ Prompt file not found at: `data/prompts.yaml`")
    prompts = []

# --- Load Evaluation Results ---
if os.path.exists(RESULTS_PATH):
    results_df = pd.read_csv(RESULTS_PATH)
    st.success("✅ Evaluation results loaded successfully!")
else:
    st.warning("⚠️ Evaluation results file not found.")
    results_df = pd.DataFrame()

# --- Load Refined Prompts ---
refined_prompts = []
if os.path.exists(REFINED_PROMPT_PATH):
    try:
        with open(REFINED_PROMPT_PATH, "r") as f:
            refined_prompts = yaml.safe_load(f) or []
        if not isinstance(refined_prompts, list):
            refined_prompts = []
    except Exception as e:
        st.warning(f"⚠️ Failed to load refined prompts: {e}")
        refined_prompts = []

# --- Display Each Prompt Block ---
for prompt in prompts:
    prompt_id = prompt.get("prompt_id", "Unknown")
    with st.expander(f"🧠 Prompt ID: {prompt_id}", expanded=False):
        st.markdown(f"**📝 Text:** `{prompt.get('text', '')}`")
        st.markdown(f"**🎯 Intent:** `{prompt.get('intent', 'N/A')}`")
        st.markdown(f"**🔄 Strategy:** `{prompt.get('strategy', 'N/A')}`")
        st.markdown(f"**🧩 Complexity:** `{prompt.get('complexity', 'N/A')}`")

        

        # --- Evaluation Results ---
        if not results_df.empty and prompt_id in results_df["Prompt ID"].values:
            row = results_df[results_df["Prompt ID"] == prompt_id].iloc[0]

            st.markdown("---")
            st.subheader("📤 Model Response")
            st.write(row.get("Response", "N/A"))

            st.subheader("✅ Reference Answer")
            st.write(row.get("Reference", "N/A"))

            st.markdown("---")
            st.subheader("📈 Quantitative Metrics")
            col1, col2 = st.columns(2)
            col1.metric("BLEU Score", f"{row.get('BLEU', 0.0):.3f}")
            col2.metric("F1 Score", f"{row.get('F1', 0.0):.3f}")

            st.markdown("---")
            st.subheader("💬 ChatGPT-Assisted Evaluation")

            structured_fields = ["relevance", "correctness", "completeness", "coherence", "creativity", "bias"]
            has_structured = any(pd.notnull(row.get(field)) for field in structured_fields)

            if has_structured:
                for field in structured_fields:
                    value = row.get(field)
                    if pd.notnull(value):
                        st.write(f"**{field.capitalize()}**: {value}")
                comment = row.get("comment", "")
                if pd.notnull(comment):
                    st.info(f"📝 Comment: {comment}")
                else:
                    st.info("📝 No comment available.")
            else:
                st.warning("⚠️ Could not parse ChatGPT evaluation.")
                raw_response = row.get("raw_response", "")
                if isinstance(raw_response, str) and raw_response.strip():
                    st.code(raw_response, language="json")
                else:
                    st.write(raw_response or "No raw response available.")
        else:
            st.warning("⚠️ Evaluation results not found for this prompt.")

        # --- Refined Prompt ---
        refined_entry = next(
            (
                r for r in refined_prompts
                if r.get("prompt_id") == prompt_id or r.get("original_prompt") == prompt.get("text")
            ),
            None
        )
        if refined_entry and refined_entry.get("refined_prompt"):
            st.markdown("🛠️ **Suggested Refined Prompt:**")
            st.code(refined_entry["refined_prompt"], language="markdown")