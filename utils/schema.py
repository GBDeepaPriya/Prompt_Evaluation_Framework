from pydantic import BaseModel
from typing import Literal

class Prompt(BaseModel):
    prompt_id: str
    text: str
    intent: Literal["Q&A", "summarization", "reasoning", "code generation", "creative writing"]
    strategy: Literal["zero-shot", "few-shot", "chain-of-thought"]
    complexity: Literal["simple", "compound", "multi-turn"]
