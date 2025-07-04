import requests

# ✅ Your OpenRouter API key (starts with `org-` or `sk-or-`)
API_KEY = "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"

# ✅ Your model name
MODEL = "meta-llama/llama-3-70b-instruct"  # Or another model from https://openrouter.ai/docs#models

def generate_response(prompt_text: str, model: str = MODEL) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",  # Optional: use your GitHub page or project URL
        "X-Title": "PromptEval",                   # Optional: visible on OpenRouter dashboard
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt_text}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"OpenRouter API error {response.status_code}: {response.text}")
