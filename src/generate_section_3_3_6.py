import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_section_3_3_6_pdf(output_path="output/pdf/section_3_3_6.pdf"):
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
        fontSize=13,
        leading=17,
        textColor=colors.black,
        spaceBefore=12,
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'AcademicBodyStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=18, # 1.5 line spacing matching original thesis
        textColor=colors.black,
        spaceAfter=10,
        alignment=4 # Justified
    )
    
    bullet_style = ParagraphStyle(
        'AcademicBulletStyle',
        parent=body_style,
        leftIndent=15,
        spaceAfter=8
    )

    story = []
    
    story.append(Paragraph("3.3.6 Hypothesis Testing and Statistical Significance Framework", section_title_style))
    story.append(Paragraph(
        "To determine whether observed differences in risk-adjusted performance (Sharpe and Sortino ratios) and weekly portfolio returns between candidate strategies and baseline benchmarks are statistically meaningful or merely artifacts of sampling variation, this study implements a decision-theoretic inferential hypothesis testing framework. In emerging equity markets such as the NGX—where asset returns display pronounced non-normality, negative skewness, and heavy tails—traditional parametric Z-tests can yield misleading p-values. Therefore, both parametric and robust non-parametric bootstrap procedures are employed:",
        body_style
    ))
    
    story.append(Paragraph(
        "1. <b>Jobson and Korkie (1981) Test with Memmel (2007) Correction:</b><br/>"
        "Evaluates the null hypothesis of Sharpe ratio equality H<sub>0</sub>: Sharpe<sub>A</sub> = Sharpe<sub>B</sub> for two correlated portfolios. Memmel (2007) corrects the asymptotic variance under portfolio correlation &rho;:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>Z = (Sharpe<sub>A</sub> - Sharpe<sub>B</sub>) / &radic;( (1 / T) [ 2(1 - &rho;) + 0.5(Sharpe<sub>A</sub><sup>2</sup> + Sharpe<sub>B</sub><sup>2</sup> - 2 Sharpe<sub>A</sub> Sharpe<sub>B</sub> &rho;<sup>2</sup>) ] )</i><br/>"
        "where <i>T</i> is the number of out-of-sample weekly observations.",
        bullet_style
    ))
    
    story.append(Paragraph(
        "2. <b>Ledoit and Wolf (2008) Circular Block Bootstrap Test for Sharpe Ratio Equality:</b><br/>"
        "Resamples overlapping blocks of length <i>b</i> = 5 weeks across <i>B</i> = 2,000 bootstrap replicates to preserve time-series autocorrelation and conditional heteroskedasticity (GARCH effects). The empirical p-value evaluates H<sub>0</sub>: Sharpe<sub>A</sub> - Sharpe<sub>B</sub> = 0.",
        bullet_style
    ))
    
    story.append(Paragraph(
        "3. <b>Ledoit and Wolf (2011) Bootstrap Test for Sortino Ratio Equality:</b><br/>"
        "Extends non-parametric block bootstrapping to downside risk, evaluating H<sub>0</sub>: Sortino<sub>A</sub> - Sortino<sub>B</sub> = 0 to verify excess return per unit of downside risk.",
        bullet_style
    ))
    
    story.append(Paragraph(
        "4. <b>Non-Parametric Wilcoxon Signed-Rank Test and Paired t-Test:</b><br/>"
        "Evaluates whether weekly differential returns &Delta;R<sub>t</sub> = R<sub>A,t</sub> - R<sub>B,t</sub> significantly deviate from zero (H<sub>0</sub>: E[&Delta;R<sub>t</sub>] = 0).",
        bullet_style
    ))
    
    story.append(Paragraph(
        "5. <b>Diebold and Mariano (1995) Test for Predictive Accuracy:</b><br/>"
        "Evaluates whether out-of-sample forecasting loss (RMSE) differentials between machine learning models (Random Forest, XGBoost) and the Historical Mean baseline are statistically significant.",
        bullet_style
    ))

    doc.build(story)
    print(f"[OK] Generated standalone Section 3.3.6 page: {output_path}")

if __name__ == '__main__':
    generate_section_3_3_6_pdf()
