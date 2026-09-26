import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_clean_ch3_intro_pdf(output_path="output/pdf/clean_ch3_intro.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=72,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()

    body_style = ParagraphStyle(
        'BlackBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=24,  # Double-spaced
        textColor=colors.HexColor('#000000'),
        alignment=4,  # TA_JUSTIFY
        spaceAfter=12
    )

    heading2_style = ParagraphStyle(
        'BlackHeading2',
        parent=styles['Heading2'],
        fontName='Times-Bold',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#000000'),
        spaceBefore=14,
        spaceAfter=10,
        keepWithNext=True
    )

    heading3_style = ParagraphStyle(
        'BlackHeading3',
        parent=styles['Heading3'],
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#000000'),
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    story = []

    # Section 3.1.1 Body Text
    story.append(Paragraph(
        "As established in Chapter 2, the foundation of portfolio selection lies in Harry Markowitz's "
        "Modern Portfolio Theory (MPT), which formalizes the risk-return trade-off by assuming "
        "normally distributed returns and relying on symmetric variance as the primary measure of risk "
        "(Markowitz, 1952).",
        body_style
    ))
    story.append(Paragraph(
        "However, the empirical reality of emerging markets like the Nigerian Exchange Group (NGX) "
        "fundamentally violates these strict assumptions; these markets are instead characterized by high "
        "volatility, low liquidity, asymmetric information, and leptokurtic distributions where extreme "
        "downside market events happen much more frequently than normal distributions would predict "
        "(Arif &amp; Sohail, 2020). To address these structural violations, Post-Modern Portfolio Theory "
        "(PMPT) offers a theoretical solution by redefining risk not as general symmetrical volatility, but "
        "specifically as the probability of financial loss, thereby distinguishing between desirable upside "
        "gains and detrimental downside drops (Alotaibi et al., 2022). Consequently, this methodology "
        "operationalizes PMPT by discarding the traditional mean-variance framework in favor of "
        "Conditional Value-at-Risk (CVaR), a coherent risk measure selected to specifically quantify and "
        "minimize the average severity of extreme tail losses occurring beyond a catastrophic threshold in "
        "the NGX (Rockafellar &amp; Uryasev, 2002).",
        body_style
    ))

    # Section 3.1.2
    story.append(Paragraph("3.1.2 Machine Learning Theories for Forecasting", heading2_style))
    story.append(Paragraph(
        "To address the limitations of the Efficient Market Hypothesis (EMH) outlined in Chapter 2, this "
        "methodology utilizes advanced statistical learning theories. The EMH and the associated "
        "Random Walk Hypothesis postulate that asset prices instantaneously reflect all available "
        "information and fluctuate randomly, theoretically rendering future price movements "
        "unpredictable and active forecasting futile (Fama, 1970).",
        body_style
    ))
    story.append(Paragraph(
        "However, substantial empirical evidence challenges these strict assumptions, particularly in "
        "emerging markets like the Nigerian Exchange Group (NGX), which exhibit market frictions, "
        "significant volatility clustering, frequent structural breaks, and complex non-linear correlations "
        "(Adegboyo &amp; Sarwar, 2025). Statistical learning theories offer a robust mathematical framework "
        "that bypasses rigid econometric assumptions, allowing for the extraction of meaningful, latent "
        "non-linear dependencies directly from noisy and high-dimensional financial data "
        "(Gu, Kelly, &amp; Xiu, 2019).",
        body_style
    ))
    story.append(Paragraph(
        "Consequently, this methodology adopts advanced ensemble machine learning algorithms, specifically "
        "Random Forest and eXtreme Gradient Boosting (XGBoost), to effectively operationalize statistical learning, "
        "thereby capturing the complex, non-stationary market patterns that traditional models and the EMH fail to identify "
        "(Manogna &amp; Kulkarni, 2025; Ashrafzadeh et al., 2025).",
        body_style
    ))

    # Section 3.2 Model Specification
    story.append(Paragraph("3.2 Model Specification", heading2_style))
    story.append(Paragraph("3.2.1 Predictive Models", heading3_style))
    story.append(Paragraph(
        "The aim of the predictive phase of the study is to forecast future returns of the component assets "
        "within the NGX Pension Index. To achieve this, the study frames return forecasting as a "
        "supervised multivariate time-series problem. Unlike traditional linear asset pricing models which "
        "assume a linear relationship between risk factors and returns, this methodology posits that "
        "financial time series are driven by complex, non-linear, and interacting market dynamics.",
        body_style
    ))

    doc.build(story)
    print(f"[OK] Generated clean solid black intro replacement pages: {output_path}")

if __name__ == '__main__':
    generate_clean_ch3_intro_pdf()
