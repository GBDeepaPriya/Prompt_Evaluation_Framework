from evaluation.chatgpt_assisted import chatgpt_judge, chatgpt_refine_prompt
import yaml
import os

def refine_prompt(prompt: str, outputs: list[str], save_to: str = "output/refined_prompts.yaml") -> str:
    print(f"\n🔧 Evaluating Prompt:\n{prompt}\n")

    evaluation = chatgpt_judge(prompt, outputs)

    # --- If evaluation failed (e.g. no JSON block), fallback to heuristics ---
    if isinstance(evaluation, dict) and "error" in evaluation:
        print(f"[⚠️] Evaluation failed: {evaluation['error']}")

        # Check for vague/unhelpful response content
        vague_phrases = ["please provide", "I can't", "I'm sorry", "unclear", "incomplete", "couldn't"]
        response_text = outputs[0].lower()
        if any(phrase in response_text for phrase in vague_phrases):
            print("[⚠️] Detected vague/incomplete response. Triggering refinement anyway.")
        else:
            print("[ℹ️] No critical issues detected. Skipping refinement.")
            return ""

    else:
        # Score-Based Refinement Decision
        score_fields = ["relevance", "correctness", "completeness", "coherence"]
        low_scores = [
            evaluation.get(f, 5)
            for f in score_fields
            if isinstance(evaluation.get(f), int) and evaluation.get(f) < 4
        ]
        if not low_scores:
            print("[ℹ️] Prompt is strong enough — no refinement needed.")
            return ""

    print("[⚠️] Weak or unclear prompt detected — generating refinement...")

    # --- Build refinement instruction prompt ---
    suggestion_prompt = f"""
You are an expert prompt engineer.

Based on the following evaluation:
{evaluation}

Suggest an improved version of the original prompt:
\"{prompt}\"

Keep the original intent but improve clarity, specificity, or effectiveness.

Respond ONLY with the new prompt as plain text.
""".strip()

    try:
        refined_prompt = chatgpt_refine_prompt(suggestion_prompt).strip()

        if refined_prompt and not refined_prompt.lower().startswith("refinement failed"):
            entry = {"original_prompt": prompt, "refined_prompt": refined_prompt}
            existing = []

            if os.path.exists(save_to):
                with open(save_to, "r") as f:
                    existing = yaml.safe_load(f) or []

            existing.append(entry)
            with open(save_to, "w") as f:
                yaml.dump(existing, f)

            print(f"[✅] Refined prompt saved to: {save_to}")
            return refined_prompt
        else:
            print("[❌] Failed to generate a valid refined prompt.")
            return ""

    except Exception as e:
        print(f"[❌] Exception during refinement: {str(e)}")
        return f"Refinement failed: {str(e)}"
