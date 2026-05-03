def extract_paragraphs(pages):
    paragraphs = []

    for p in pages:

        # ----------------------------
        # FIX 1: normalize input type
        # ----------------------------
        if isinstance(p, str):
            text = p
            page_num = None

        elif isinstance(p, dict):
            text = p.get("text", "")
            page_num = p.get("page", None)

        else:
            continue  # skip garbage input

        if not text:
            continue

        lines = text.split("\n")
        buffer = ""

        for line in lines:
            line = line.strip()

            if len(line) < 40:
                continue

            buffer += " " + line

            if len(buffer) > 200:
                paragraphs.append({
                    "page": page_num,
                    "text": buffer.strip()
                })
                buffer = ""

        # flush remaining buffer
        if buffer.strip():
            paragraphs.append({
                "page": page_num,
                "text": buffer.strip()
            })

    return paragraphs