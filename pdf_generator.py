import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

def generate_pdf(title, content, filename="static/article.pdf"):

    if not os.path.exists("static"):
        os.makedirs("static")

    doc = SimpleDocTemplate(filename, pagesize=A4)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1, 12))

    content = content.replace("\n", "<br/>")

    story.append(Paragraph(content, styles["BodyText"]))

    doc.build(story)

    return filename