import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_clean_page_47_pdf(output_path="output/pdf/clean_page_47.pdf"):
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
        spaceBefore=12,
        spaceAfter=6
    )
    
    subsection_title_style = ParagraphStyle(
        'SubSectionTitleStyle',
        parent=styles['Heading3'],
        fontName='Times-Bold',
        fontSize=12,
        leading=24,
        textColor=colors.black,
        spaceBefore=10,
        spaceAfter=6
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
    
    bullet_style = ParagraphStyle(
        'AcademicBulletStyle',
        parent=body_style,
        leftIndent=15,
        spaceAfter=6
    )

    story = []
    
    # 1. Benchmark Portfolios for Evaluation
    story.append(Paragraph("3. Benchmark Portfolios for Evaluation", subsection_title_style))
    story.append(Paragraph(
        "To rigorously evaluate the economic value and true out-of-sample performance of the advanced ML-CVaR optimization strategy, it is essential to measure its results against standard baseline portfolios. By utilizing these benchmarks alongside the metrics above, the study empirically validates whether the non-linear machine learning forecasts, combined with CVaR tail-risk constraints, genuinely deliver superior risk-adjusted performance on the Nigerian Exchange.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>The 1/N Equally Weighted Portfolio (EWP):</b> In this naive diversification strategy, investment capital is simply divided uniformly across all selected stocks without relying on any parameter estimation or complex optimization algorithms. In an EWP strategy, each asset in the portfolio holds an equal weight of <i>w<sub>i</sub> = 1/N</i>. This rule is chosen as a primary benchmark because it is easy to implement and continues to be a standard, highly effective allocation rule utilized by investors.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>The Buy-and-Hold Market Index Strategy:</b> This is a passive strategy that involves buying and holding the market index itself (in this case, the NGX Pension Index). This serves as a critical baseline to demonstrate whether active portfolio management based on machine learning predictions genuinely provides superior risk-adjusted returns compared to general market movements. Initialized at equal weights <i>w<sub>0,i</sub> = 1/N</i> at <i>t = 0</i>, Buy-and-Hold weights drift passively with asset price returns (<i>w<sub>t+1,i</sub> &prop; w<sub>t,i</sub>(1 + R<sub>t+1,i</sub>)</i>) with zero rebalancing turnover post week 0.",
        bullet_style
    ))
    
    # 2. 3.3.6 Hypothesis Testing and Statistical Significance Framework
    story.append(Paragraph("3.3.6 Hypothesis Testing and Statistical Significance Framework", section_title_style))
    story.append(Paragraph(
        "To determine whether observed differences in risk-adjusted performance (Sharpe and Sortino ratios) and weekly portfolio returns between candidate strategies and baseline benchmarks are statistically meaningful or merely artifacts of sampling variation, this study implements a decision-theoretic inferential hypothesis testing framework. In emerging equity markets such as the NGX, where asset returns display pronounced non-normality, negative skewness, and heavy tails, traditional parametric Z-tests can yield misleading p-values. Therefore, both parametric and robust non-parametric bootstrap procedures are employed:",
        body_style
    ))
    
    story.append(Paragraph(
        "1. <b>Jobson and Korkie (1981) Test with Memmel (2007) Correction:</b> Evaluates the null hypothesis of Sharpe ratio equality H<sub>0</sub>: Sharpe<sub>A</sub> = Sharpe<sub>B</sub> for two correlated portfolios. Memmel (2007) corrects the asymptotic variance under portfolio correlation &rho;:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>Z = (Sharpe<sub>A</sub> - Sharpe<sub>B</sub>) / &radic;( (1 / T) [ 2(1 - &rho;) + 0.5(Sharpe<sub>A</sub><sup>2</sup> + Sharpe<sub>B</sub><sup>2</sup> - 2 Sharpe<sub>A</sub> Sharpe<sub>B</sub> &rho;<sup>2</sup>) ] )</i><br/>"
        "where <i>T</i> is the number of out-of-sample weekly observations.",
        bullet_style
    ))
    story.append(Paragraph(
        "2. <b>Ledoit and Wolf (2008) Circular Block Bootstrap Test for Sharpe Ratio Equality:</b> Resamples overlapping blocks of length <i>b = 5</i> weeks across <i>B = 2,000</i> bootstrap replicates to preserve time-series autocorrelation and conditional heteroskedasticity (GARCH effects). The empirical p-value evaluates H<sub>0</sub>: Sharpe<sub>A</sub> - Sharpe<sub>B</sub> = 0.",
        bullet_style
    ))
    story.append(Paragraph(
        "3. <b>Ledoit and Wolf (2011) Bootstrap Test for Sortino Ratio Equality:</b> Extends non-parametric block bootstrapping to downside risk, evaluating H<sub>0</sub>: Sortino<sub>A</sub> - Sortino<sub>B</sub> = 0 to verify excess return per unit of downside risk.",
        bullet_style
    ))
    story.append(Paragraph(
        "4. <b>Non-Parametric Wilcoxon Signed-Rank Test and Paired t-Test:</b> Evaluates whether weekly differential returns &Delta;R<sub>t</sub> = R<sub>A,t</sub> - R<sub>B,t</sub> significantly deviate from zero (H<sub>0</sub>: E[&Delta;R<sub>t</sub>] = 0).",
        bullet_style
    ))
    story.append(Paragraph(
        "5. <b>Diebold and Mariano (1995) Test for Predictive Accuracy:</b> Evaluates whether out-of-sample forecasting loss (RMSE) differentials between machine learning models (Random Forest, XGBoost) and the Historical Mean baseline are statistically significant.",
        bullet_style
    ))
    
    # 3. 3.4 Description and Measurement of Study Variables intro text
    story.append(Paragraph("3.4 Description and Measurement of Study Variables", section_title_style))
    story.append(Paragraph(
        "The variables utilized in this study are partitioned into the target variable, the thirteen machine learning feature inputs (extracted exclusively from the weekly OHLCV data), and the exogenous risk-free rate parameter required for portfolio evaluation.",
        body_style
    ))

    doc.build(story)
    print(f"[OK] Generated clean replacement page 47: {output_path}")

if __name__ == '__main__':
    generate_clean_page_47_pdf()
