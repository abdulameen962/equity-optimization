import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_clean_page15_pdf(output_path="output/pdf/clean_page15.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=1.0*inch,
        rightMargin=1.0*inch,
        topMargin=1.0*inch,
        bottomMargin=1.0*inch
    )
    
    styles = getSampleStyleSheet()
    
    section_title_style = ParagraphStyle(
        'AcademicSectionTitle',
        parent=styles['Heading2'],
        fontName='Times-Bold',
        fontSize=12,
        leading=24,
        textColor=colors.black,
        spaceBefore=14,
        spaceAfter=6
    )
    
    chapter_header_style = ParagraphStyle(
        'ChapterHeaderStyle',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=14,
        leading=24,
        textColor=colors.black,
        spaceBefore=20,
        spaceAfter=12,
        alignment=0 # Left-aligned
    )

    body_style = ParagraphStyle(
        'AcademicBodyStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=24, # Double spaced (12pt font x 2 = 24pt leading)
        textColor=colors.black,
        spaceAfter=10,
        alignment=4 # Justified
    )

    story = []
    
    # 1. Continuation from bottom of Page 14
    story.append(Paragraph(
        "resilient portfolio outcomes. While these improved methods exist, their applications in emerging "
        "markets such as the Nigerian Exchange Group (NGX) remains under-explored (Moyoweshumba "
        "& Seitshiro, 2025). This necessitates the study not only for academics and researchers but also "
        "for real decision-making.",
        body_style
    ))
    
    # 2. 1.6 Scope of the Study
    story.append(Paragraph("1.6 Scope of the Study", section_title_style))
    story.append(Paragraph(
        "This study examines the effect of equity-return forecasting on tail-risk aware optimization on the "
        "Nigerian Exchange Group (NGX). Weekly price data on selected companies in the NGX Pension Index "
        "between the period of 2010 - 2025 will be utilized for the study. This study could not "
        "extend beyond the selected time frame due to unavailability of price data due to the date of "
        "companies' listings. Most available data on price data on publicly listed companies were sourced "
        "from ng.investing.com which was limited to the timeframe of the study.",
        body_style
    ))
    
    # 3. 1.7 Organization of the Study
    story.append(Paragraph("1.7 Organization of the Study", section_title_style))
    story.append(Paragraph(
        "This study is divided into five chapters. The first chapter of this study provides the background "
        "of the study, which will further prove the need for the study. Chapter two presents the theoretical "
        "and empirical review of relevant studies in the study's subject matter. The theoretical perspective "
        "in the second chapter will introduce the adopted models in chapter three. Data analysis and "
        "presentation will be carried out in chapter four, while the concluding comments that include "
        "summary, conclusion, recommendations, and suggestions for further studies will be made in "
        "chapter five.",
        body_style
    ))
    
    # 4. CHAPTER TWO Header
    story.append(Spacer(1, 10))
    story.append(Paragraph("CHAPTER TWO", chapter_header_style))

    doc.build(story)
    print(f"[OK] Generated clean replacement page 15: {output_path}")

if __name__ == '__main__':
    generate_clean_page15_pdf()
