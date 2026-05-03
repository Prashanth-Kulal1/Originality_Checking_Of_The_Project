from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(results, ai, score):
    doc = SimpleDocTemplate("outputs/reports/report.pdf")
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph(f"AI Detection: {ai}", styles["Title"]))
    content.append(Spacer(1, 10))
    content.append(Paragraph(f"Plagiarism Score: {score}%", styles["Normal"]))

    for r in results:
        content.append(Spacer(1, 10))
        content.append(Paragraph(f"Page {r['page']}", styles["Heading2"]))

        for m in r["matches"]:
            content.append(Paragraph(
                f"{m['sentence']} ({m['similarity']}%)",
                styles["Normal"]
            ))

    doc.build(content)