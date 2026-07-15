from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import re
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

def create_roadmap_pdf(content, filename):

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        fontSize=18,
        spaceAfter=20
    )

    phase_style = ParagraphStyle(
        "PhaseStyle",
        parent=styles["Heading3"],
        fontSize=16,
        fontName="Helvetica-Bold",
        leading=20,
        textColor=colors.blue,
        spaceBefore=8,
        spaceAfter=4
    )

    sub_style = ParagraphStyle(
        "SubStyle",
        parent=styles["Normal"],
        fontSize=11,
        leading=16,
        spaceAfter=3
    )


    elements = []

    elements.append(
        Paragraph(
            "🚀 AI Career Roadmap",
            title_style
        )
    )
    content = re.sub(
        r"\s+(What to Learn:|What to Practice:|Goal to Complete:|Short Explanation:)",
        r"\n\1",
        content
    )

    lines = content.split("\n")
    

    for line in lines:

        line = line.strip()

        if not line:
            elements.append(
                Spacer(1,8)
            )
            continue


        if re.match(r"^\s*Phase\s+\d+", line, re.IGNORECASE):

            elements.append(
                Paragraph(
                    line,
                    phase_style
                )
            )


        elif line.startswith("Short Explanation"):

            elements.append(Spacer(1,8))

            parts = line.split(":", 1)

            if len(parts) == 2:
                elements.append(
                    Paragraph(
                        f"<b>Short Explanation:</b> {parts[1].strip()}",
                        sub_style
                    )
                )
            else:
                elements.append(
                    Paragraph(line, sub_style)
                )

        elif (
            line.startswith("What to Learn")
            or
            line.startswith("What to Practice")
            or
            line.startswith("Goal to Complete")
        ):

            elements.append(Spacer(1,8))

            elements.append(
                Paragraph(
                    line,
                    phase_style
                )
            )


        else:

            elements.append(
                Paragraph(
                    line.replace("-", "•"),
                    sub_style
                )
            )


        elements.append(
            Spacer(1,8)
        )

    doc.build(elements)



# ==========================================================
# FULL CAREER REPORT PDF GENERATOR
# ==========================================================

def create_full_report_pdf(
    name,
    qualification,
    skills,
    career_goal,
    report,
    prep_questions,
    prep_answers,
    prep_score,
    filename
):

    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer
    )

    from reportlab.lib.styles import (
        getSampleStyleSheet,
        ParagraphStyle
    )

    from reportlab.lib.pagesizes import letter
    from reportlab.lib.enums import TA_CENTER


    doc = SimpleDocTemplate(
        filename,
        pagesize=letter
    )


    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(
        "FullTitle",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=20
    )


    header_style = ParagraphStyle(
        "HeaderStyle",
        parent=styles["Heading2"],
        fontSize=16,
        spaceBefore=15,
        spaceAfter=10
    )


    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontSize=11,
        leading=16
    )


    elements = []


    elements.append(
        Paragraph(
            "🚀 AI Career Roadmap Generator",
            title_style
        )
    )


    elements.append(
        Paragraph(
            "✨ Build Your Career In Just Minutes",
            normal_style
        )
    )

    elements.append(Spacer(1,20))


    user_details = [
        f"👤 Name: {name}",
        f"🎓 Qualification: {qualification}",
        f"📚 Skills: {skills}",
        f"🎯 Career Goal: {career_goal}"
    ]


    for item in user_details:

        elements.append(
            Paragraph(
                item,
                normal_style
            )
        )

        elements.append(
            Spacer(1,8)
        )


    elements.append(
        Paragraph(
            "🎯 Your Personalized Career Report",
            header_style
        )
    )
    

    lines = report.split("\n")


    for line in lines:

        line = line.strip()

        if not line:
            continue


        if (
            line.startswith("🎯")
            or line.startswith("📊")
            or line.startswith("🌱")
            or line.startswith("🗺️")
            or line.startswith("💼")
            or line.startswith("📚")
            or line.startswith("🤖")
            or line.startswith("💰")
            or line.startswith("✅")
            or line.startswith("🌟")
            or line.startswith("Phase")
        ):

            elements.append(
                Paragraph(
                    f"<b>{line}</b>",
                    header_style
                )
            )

        else:

            elements.append(
                Paragraph(
                    line.replace("-", "•"),
                    normal_style
                )
            )


        elements.append(
            Spacer(1,8)
        )
    elements.append(Spacer(1, 15))

    if prep_answers:

        elements.append(
            Paragraph(
                "<b>📊 Career Preparation Result</b>",
                header_style
            )
        )

        elements.append(
            Paragraph(
                f"📝 Your Answers: {prep_answers}",
                normal_style
            )
        )
    if prep_score:

        elements.append(
            Paragraph(
                f"<b>🏆 Preparation Score: {prep_score}%</b>",
                normal_style
            )
        )

    elements.append(
        Spacer(1,15)
    )

    doc.build(elements)

