from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from sklearn.metrics import f1_score

def evaluate_bleu(reference: str, candidate: str) -> float:
    """
    Compute BLEU score between reference and candidate response.
    """
    smoothie = SmoothingFunction().method4
    return sentence_bleu([reference.split()], candidate.split(), smoothing_function=smoothie)

def evaluate_f1(reference: str, candidate: str) -> float:
    """
    Compute F1 score based on token overlap.
    """
    ref_tokens = reference.split()
    cand_tokens = candidate.split()
    labels = list(set(ref_tokens + cand_tokens))
    
    y_true = [1 if token in ref_tokens else 0 for token in labels]
    y_pred = [1 if token in cand_tokens else 0 for token in labels]

    return f1_score(y_true, y_pred)
