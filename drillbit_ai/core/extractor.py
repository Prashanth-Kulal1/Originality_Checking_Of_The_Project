import PyPDF2

def extract_text(file):
    reader = PyPDF2.PdfReader(file)

    pages = []

    for i, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""

        pages.append({
            "page": i + 1,
            "text": page_text
        })

    return pages