
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -----------------------------
# 🔥 MAIN SIMILARITY FUNCTION
# -----------------------------
def compute_similarity(text1, text2):
    try:
        if not text1 or not text2:
            return 0

        text1 = str(text1).strip()
        text2 = str(text2).strip()

        if len(text1) < 10 or len(text2) < 10:
            return 0

        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf = vectorizer.fit_transform([text1, text2])

        score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

        return round(score * 100, 2)

    except:
        return 0


# -----------------------------
# 🔥 SENTENCE LEVEL MATCHING (IMPROVED)
# -----------------------------
def compare_sentences(text, source_text):

    if not text or not source_text:
        return []

    # split both texts into sentences
    input_sentences = text.split(".")
    source_sentences = source_text.split(".")

    matched = []

    for sent1 in input_sentences:
        sent1 = sent1.strip()

        if len(sent1) < 20:
            continue

        best_score = 0

        for sent2 in source_sentences:

            sent2 = sent2.strip()

            if len(sent2) < 20:
                continue

            sim = compute_similarity(sent1, sent2)

            if sim > best_score:
                best_score = sim

        # 🔥 smarter threshold
        if best_score > 20:
            matched.append({
                "sentence": sent1,
                "similarity": round(best_score, 2)
            })

    return matched

