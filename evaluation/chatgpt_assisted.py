import os
import json
import re
import requests
from models.llm_interface import API_KEY

# --- OpenRouter API Setup ---
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "https://yourdomain.com",  # ✅ Customize this
    "X-Title": "PromptEval ChatGPT Evaluation"
}
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

def chatgpt_judge(prompt_text, responses):
    """
    Evaluate an LLM response using a structured rubric and return evaluation JSON.
    """
    try:
        response_text = responses[0] if responses else ""
        eval_prompt = f"""
Evaluate the following LLM response. Score from 1–5.

Prompt: {prompt_text}

Response: {response_text}

Respond ONLY with valid JSON in this format (no commentary):

{{
  "relevance": int,
  "correctness": int,
  "completeness": int,
  "coherence": int,
  "creativity": int,
  "bias": int,
  "comment": "..."
}}
""".strip()

        data = {
            "model": "meta-llama/llama-3-70b-instruct",
            "messages": [{"role": "user", "content": eval_prompt}]
        }

        response = requests.post(ENDPOINT, headers=HEADERS, json=data)
        result = response.json()

        # Extract message content
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        # Normalize content to extract JSON
        content = content.strip("```").replace("json", "").strip()
        match = re.search(r'{.*}', content, re.DOTALL)

        if not match:
            return {"error": "Could not find JSON block in response.", "raw_response": content}

        json_block = match.group()

        try:
            parsed = json.loads(json_block)
            required = {"relevance", "correctness", "completeness", "coherence", "creativity", "bias", "comment"}
            if required.issubset(parsed.keys()):
                return parsed
            else:
                return {"error": "Missing keys in parsed JSON.", "raw_response": json_block}
        except json.JSONDecodeError as e:
            return {"error": f"JSON decode error: {e}", "raw_response": json_block}

    except Exception as e:
        return {"error": str(e), "raw_response": response.text if 'response' in locals() else ''}


def chatgpt_refine_prompt(instruction_prompt: str) -> str:
    """
    Request a refined prompt from the LLM based on an instruction. Returns plain text.
    """
    try:
        data = {
            "model": "meta-llama/llama-3-70b-instruct",
            "messages": [{"role": "user", "content": instruction_prompt}]
        }

        response = requests.post(ENDPOINT, headers=HEADERS, json=data)
        result = response.json()

        content = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        # Optional: Filter out accidental code blocks
        content = content.strip("```").replace("text", "").strip()

        return content

    except Exception as e:
        return f"Refinement failed with exception: {str(e)}"
