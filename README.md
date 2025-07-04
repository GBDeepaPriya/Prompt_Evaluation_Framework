# 🧠 Prompt Evaluation Framework

Prompt Evaluation framework for evaluating and refining prompts using both **automated metrics** (BLEU, F1) and **LLM-assisted evaluation (ChatGPT)**. It helps identify weak prompts, generate improved versions, and visualize the results in a dashboard.

---

## 📁 Project Structure

```
Prompt_Evaluation_Framework/
│
├── data/
│   └── prompts.yaml               # Input prompts with metadata and references
│
├── output/
│   ├── results.csv                # Auto-generated evaluation results
│   └── refined_prompts.yaml       # Auto-generated improved prompts
│
├── models/
│   └── llm_interface.py           # API call to LLM (OpenRouter / ChatGPT)
│
├── evaluation/
│   ├── metrics.py                 # BLEU and F1 evaluation functions
│   └── chatgpt_assisted.py        # ChatGPT-based structured judgment + refinement
│
├── tuner/
│   └── prompt_tuner.py            # refine_prompt() logic with conditional refinement
│
├── dashboard/
│   └── app.py                     # Streamlit dashboard for exploring evaluation results
│
├── main.py                        # Main script for running prompt evaluation pipeline
├── requirements.txt
└── README.md
```

---

## ✅ Features

- 🔍 **Prompt Evaluation** using:
  - BLEU and F1 for automatic scoring
  - ChatGPT-assisted judgment (relevance, correctness, completeness, etc.)
- 🛠️ **Prompt Refinement** only when:
  - Evaluation scores are poor
  - Response is vague or incomplete
- 📊 **Streamlit Dashboard** to explore:
  - Original & refined prompts
  - Model responses and reference answers
  - Evaluation scores & LLM feedback

---

## ⚙️ Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

> ⚠️ Requires Python 3.8+

---

## 🚀 Running the Evaluation

1. **Add prompts** in `data/prompts.yaml`:

```yaml
- prompt_id: QA_001
  text: What is the capital of France?
  intent: factual_qa
  strategy: direct
  complexity: low
  reference: Paris
```

2. **Run the main evaluation script**:

```bash
python main.py
```

This will:

- Generate model responses
- Evaluate using BLEU, F1, and ChatGPT
- Refine weak prompts and save results to:
  - `output/results.csv`
  - `output/refined_prompts.yaml`

---

## 📊 Launch the Dashboard

```bash
streamlit run dashboard/app.py
```

Features:

- Toggle and explore each prompt block
- View model responses vs reference
- See ChatGPT feedback and suggested improvements

---

## 🔧 LLM Configuration

LLM API is accessed via `models/llm_interface.py` using OpenRouter or any supported LLM endpoint.

### Example using OpenRouter:

```python
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {your_openrouter_api_key}",
    "Content-Type": "application/json"
}
```

## 🧪 Key Components

| File                  | Description                                              |
| --------------------- | -------------------------------------------------------- |
| `main.py`             | full pipeline: LLM → metrics → ChatGPT eval → refinement |
| `prompt_tuner.py`     | Smart logic to only refine weak or vague prompts         |
| `chatgpt_assisted.py` | Handles structured evaluation + refinement via ChatGPT   |
| `app.py`              | Interactive UI to analyze prompts, outputs, and feedback |

---

## 🧠 Example: Refinement Logic

A prompt like:

> `Summarize the article: The solar system consists of...`

Will trigger refinement if the model responds:

> `"Please provide the full article..."`

🔄 The framework will automatically improve it to:

> `Summarize this passage about the solar system: [insert text here]`

---

## 🧼 Cleanup Output

To start fresh:

```bash
rm output/results.csv
rm output/refined_prompts.yaml
```

---

## 📌 Requirements

```txt
streamlit
pandas
pyyaml
requests
scikit-learn
openai
```

---

## 📬 Contact

Feel free to reach out if you need help integrating this with your custom LLM backend or want to extend the refinement logic.
