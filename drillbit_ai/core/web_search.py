from ddgs import DDGS

def search(query):
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=3):
                results.append(r["href"])
        return results
    except Exception as e:
        print("Search Error:", e)
        return []