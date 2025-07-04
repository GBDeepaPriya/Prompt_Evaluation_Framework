import yaml
import os
import pandas as pd
from models.llm_interface import generate_response
from evaluation.metrics import evaluate_bleu, evaluate_f1
from evaluation.chatgpt_assisted import chatgpt_judge
from utils.schema import Prompt
from tuner.prompt_tuner import refine_prompt

# --- File paths ---
PROMPT_PATH = os.path.join("data", "prompts.yaml")
RESULTS_PATH = os.path.join("output", "results.csv")
REFINED_PATH = os.path.join("output", "refined_prompts.yaml")
os.makedirs("output", exist_ok=True)

# --- Load prompts ---
with open(PROMPT_PATH, "r") as f:
    prompts = yaml.safe_load(f)

print("\n📌 PromptEval — Running Evaluation\n")

results = []

# --- Loop through prompts ---
for p in prompts:
    prompt_id = p.get("prompt_id", "")
    text = p.get("text", "")

    print(f"--- Prompt ID: {prompt_id} ---")
    print(f"Prompt: {text}")

    try:
        response = generate_response(text)
        print(f"Response: {response}")
    except Exception as e:
        print(f"❌ LLM failed: {e}")
        results.append({
            "Prompt ID": prompt_id,
            "Prompt": text,
            "Response": "",
            "Reference": "",
            "BLEU": 0.0,
            "F1": 0.0,
            "error": str(e),
            "raw_response": "",
            "Refined Prompt": ""
        })
        continue

    reference = p.get("reference", "").strip()
    if not reference:
        print(f"⚠️ Reference answer not found for {prompt_id}, skipping.")
        continue

    bleu = evaluate_bleu(reference, response)
    f1 = evaluate_f1(reference, response)

    try:
        chatgpt_eval = chatgpt_judge(text, [response])
    except Exception as e:
        chatgpt_eval = {"error": str(e), "raw_response": getattr(e, 'response', '')}

    # --- Refine Prompt using shared logic ---
    refined_prompt = ""
    try:
        if "error" not in chatgpt_eval:
            refined_prompt = refine_prompt(text, [response], save_to=REFINED_PATH)
            if not isinstance(refined_prompt, str):
                refined_prompt = ""
    except Exception as e:
        print(f"❌ Prompt refinement failed for {prompt_id}: {e}")
        refined_prompt = ""

    # --- Store Evaluation Results ---
    row = {
        "Prompt ID": prompt_id,
        "Prompt": text,
        "Response": response,
        "Reference": reference,
        "BLEU": bleu,
        "F1": f1,
        "error": chatgpt_eval.get("error", ""),
        "raw_response": chatgpt_eval.get("raw_response", ""),
        "Refined Prompt": refined_prompt
    }

    for field in ["relevance", "correctness", "completeness", "coherence", "creativity", "bias", "comment"]:
        row[field] = chatgpt_eval.get(field, None)

    results.append(row)

# --- Save Evaluation Results ---
results_df = pd.DataFrame(results)
results_df.to_csv(RESULTS_PATH, index=False)
print(f"\n✅ Evaluation results saved to: {RESULTS_PATH}")
