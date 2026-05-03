import re

def detect_ai(text):
    sentences = re.split(r'[.!?]', text)

    avg_len = sum(len(s.split()) for s in sentences) / (len(sentences) + 1)
    unique_ratio = len(set(text.split())) / (len(text.split()) + 1)

    if avg_len > 20 and unique_ratio < 0.45:
        return "Likely AI Generated"
    elif avg_len > 15:
        return "Possibly AI Assisted"
    else:
        return "Likely Human Written"