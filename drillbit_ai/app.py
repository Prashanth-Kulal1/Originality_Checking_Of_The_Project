from flask import Flask, request, jsonify, send_file, render_template
import webbrowser

from core.extractor import extract_text
from core.processor import extract_paragraphs
from core.web_search import search
from core.scraper import get_text
from core.similarity import compute_similarity, compare_sentences
from core.ai_detector import detect_ai
from core.report_generator import generate_pdf

app = Flask(__name__)


# -------------------------
# 🔥 NORMALIZER
# -------------------------
def normalize_text(data):
    if isinstance(data, list):
        cleaned = []
        for item in data:
            if isinstance(item, dict):
                cleaned.append(item.get("text", ""))
            else:
                cleaned.append(str(item))
        return " ".join(cleaned)

    return str(data)


@app.route("/")
def home():
    return render_template("index.html")


import random

@app.route("/analyze", methods=["POST"])
def analyze():

    print("🔥 OPTIMIZED ANALYZE STARTED")

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    # -------------------------
    # STEP 1: Extract
    # -------------------------
    pages = extract_text(file)
    chunks = extract_paragraphs(pages)

    # -------------------------
    # STEP 2: SMART SAMPLING
    # -------------------------
    chunks = [c for c in chunks if len(c.get("text", "")) > 80]

    sample_chunks = random.sample(chunks, min(15, len(chunks)))

    results = []
    highlighted_sentences = []
    full_text = ""

    visited_urls = {}  # 🔥 CACHE

    # -------------------------
    # STEP 3: CHECK
    # -------------------------
    for chunk in sample_chunks:

        chunk_text = chunk.get("text", "")
        full_text += chunk_text + " "

        # 🔥 SKIP USELESS CONTENT
        if any(word in chunk_text.lower() for word in [
            "certificate", "department", "college",
            "university", "signature", "acknowledgement"
        ]):
            continue

        # -------------------------
        # 🔥 SMART QUERY
        # -------------------------
        words = chunk_text.split()

        query = " ".join([
            w for w in words
            if w.isalpha() and len(w) > 5
        ][:10])

        if not query:
            continue

        links = search(query)

        print("🔎 Query:", query)
        print("🌐 Links:", len(links))

        for link in links:

            # -------------------------
            # 🔥 CACHE HIT
            # -------------------------
            if link in visited_urls:
                page_text = visited_urls[link]
            else:
                page_text = get_text(link)
                page_text = normalize_text(page_text)
                visited_urls[link] = page_text

            if not page_text or len(page_text.split()) < 50:
                continue

            sim = compute_similarity(chunk_text, page_text)

            print("SIM:", sim)

            # -------------------------
            # 🔥 BETTER THRESHOLD
            # -------------------------
            if sim > 8:

                sentence_matches = compare_sentences(chunk_text, page_text)

                if sentence_matches:
                    results.append({
                        "page": chunk.get("page", "N/A"),   # ✅ FIX
                        "source": link,
                        "similarity": round(sim, 2),
                        "matches": sentence_matches
                    })

                    for s in sentence_matches:
                        highlighted_sentences.append(s["sentence"])

    # -------------------------
    # STEP 4: AI DETECTION
    # -------------------------
    ai_result = detect_ai(full_text)

    # -------------------------
    # STEP 5: SCORE
    # -------------------------
    unique_hits = len(set(highlighted_sentences))
    total_sentences = max(len(full_text.split(".")), 1)

    score = min((unique_hits / total_sentences) * 100 * 2, 100)

    # -------------------------
    # STEP 6: REPORT
    # -------------------------
    generate_pdf(results, ai_result, round(score, 2))

    return jsonify({
        "ai_detection": ai_result,
        "plagiarism_score": round(score, 2),
        "matches": results,
        "highlighted": highlighted_sentences,
        "download_report": "/download"
    })


@app.route("/download")
def download():
    return send_file("outputs/reports/report.pdf", as_attachment=True)


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)