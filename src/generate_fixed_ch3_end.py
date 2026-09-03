import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_clean_ch3_end_pdf(output_path="output/pdf/clean_ch3_end.pdf"):
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

    table_cell_style = ParagraphStyle(
        'TableCellStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=13,
        textColor=colors.black
    )

    table_header_style = ParagraphStyle(
        'TableHeaderStyle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.black
    )

    story = []
    
    # 1. Benchmark Portfolios for Evaluation (under 3.3.5)
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
    
    # 3. 3.4 Description and Measurement of Study Variables
    story.append(Paragraph("3.4 Description and Measurement of Study Variables", section_title_style))
    story.append(Paragraph(
        "The variables utilized in this study are partitioned into the target variable, the thirteen machine learning feature inputs (extracted exclusively from the weekly OHLCV data), and the exogenous risk-free rate parameter required for portfolio evaluation.",
        body_style
    ))
    story.append(Paragraph(
        "Below is the tabular summary of all variables, their mathematical measurements, and their operational roles within the predictive and optimization models.",
        body_style
    ))
    
    # Table of Variables
    table_data = [
        [
            Paragraph("Variable Symbol", table_header_style),
            Paragraph("Variable Name", table_header_style),
            Paragraph("Category", table_header_style),
            Paragraph("Measurement / Mathematical Formulation", table_header_style),
            Paragraph("Operational Role", table_header_style)
        ],
        [
            Paragraph("<i>R<sub>i,t+1</sub></i>", table_cell_style),
            Paragraph("Weekly Logarithmic Return", table_cell_style),
            Paragraph("Target Variable", table_cell_style),
            Paragraph("ln(<i>P<sub>i,t</sub> / P<sub>i,t-1</sub></i>)", table_cell_style),
            Paragraph("The primary dependent variable. Represents continuous yield of asset <i>i</i> for upcoming week.", table_cell_style)
        ],
        [
            Paragraph("<i>MACD<sub>t</sub></i>", table_cell_style),
            Paragraph("Moving Average Convergence Divergence", table_cell_style),
            Paragraph("Momentum Predictor", table_cell_style),
            Paragraph("<i>EMA<sub>12</sub>(P<sub>t</sub>) - EMA<sub>26</sub>(P<sub>t</sub>)</i>", table_cell_style),
            Paragraph("Measures velocity of price changes to identify short-term momentum shifts.", table_cell_style)
        ],
        [
            Paragraph("<i>PPO<sub>t</sub></i>", table_cell_style),
            Paragraph("Percentage Price Oscillator", table_cell_style),
            Paragraph("Momentum Predictor", table_cell_style),
            Paragraph("[ <i>EMA<sub>12</sub>(P<sub>t</sub>) - EMA<sub>26</sub>(P<sub>t</sub>)</i> ] / <i>EMA<sub>26</sub>(P<sub>t</sub>)</i> × 100", table_cell_style),
            Paragraph("Normalized version of MACD, allowing models to compare momentum across assets of different prices.", table_cell_style)
        ],
        [
            Paragraph("<i>RSI<sub>t</sub></i>", table_cell_style),
            Paragraph("Relative Strength Index", table_cell_style),
            Paragraph("Momentum Predictor", table_cell_style),
            Paragraph("100 - [ 100 / (1 + RS) ] (where RS is average gain / average loss)", table_cell_style),
            Paragraph("Identifies overbought (>70) or oversold (<30) market conditions.", table_cell_style)
        ],
        [
            Paragraph("<i>STOCH<sub>t</sub></i>", table_cell_style),
            Paragraph("Stochastic Oscillator (%K)", table_cell_style),
            Paragraph("Momentum Predictor", table_cell_style),
            Paragraph("[ (<i>P<sub>t</sub> - L<sub>14</sub></i>) / (<i>H<sub>14</sub> - L<sub>14</sub></i>) ] × 100", table_cell_style),
            Paragraph("Evaluates closing price relative to high-low range over 14 weeks to predict turning points.", table_cell_style)
        ],
        [
            Paragraph("<i>R<sub>i,t-n</sub></i>", table_cell_style),
            Paragraph("Lagged Log Returns (Lags 1 to 4)", table_cell_style),
            Paragraph("Autoregressive Predictor", table_cell_style),
            Paragraph("<i>R<sub>i,t-1</sub>, R<sub>i,t-2</sub>, R<sub>i,t-3</sub>, R<sub>i,t-4</sub></i>", table_cell_style),
            Paragraph("Feeds past four weeks of price momentum directly into ML algorithms.", table_cell_style)
        ],
        [
            Paragraph("<i>SMA<sub>t</sub></i>", table_cell_style),
            Paragraph("Simple Moving Average", table_cell_style),
            Paragraph("Trend Predictor", table_cell_style),
            Paragraph("(1 / n) &Sigma;<sub>k=0..n-1</sub> <i>P<sub>t-k</sub></i>", table_cell_style),
            Paragraph("Smooths weekly price data to identify baseline market trend direction.", table_cell_style)
        ],
        [
            Paragraph("<i>ADX<sub>t</sub></i>", table_cell_style),
            Paragraph("Average Directional Index", table_cell_style),
            Paragraph("Trend Predictor", table_cell_style),
            Paragraph("100 × MA( |+DI - -DI| / (+DI + -DI) )", table_cell_style),
            Paragraph("Quantifies absolute strength of a trend, regardless of bullish or bearish.", table_cell_style)
        ],
        [
            Paragraph("<i>SAR<sub>t</sub></i>", table_cell_style),
            Paragraph("Parabolic Stop and Reverse", table_cell_style),
            Paragraph("Trend Predictor", table_cell_style),
            Paragraph("<i>SAR<sub>t-1</sub> + &alpha;(EP<sub>t-1</sub> - SAR<sub>t-1</sub>)</i>", table_cell_style),
            Paragraph("Identifies precise entry and exit points and signals potential trend reversals.", table_cell_style)
        ],
        [
            Paragraph("<i>ATR<sub>t</sub></i>", table_cell_style),
            Paragraph("Average True Range", table_cell_style),
            Paragraph("Volatility Predictor", table_cell_style),
            Paragraph("(1 / n) &Sigma;<sub>i=1..n</sub> <i>TR<sub>i</sub></i> (where TR incorporates gaps)", table_cell_style),
            Paragraph("Measures intra-week market volatility and true magnitude of price drops.", table_cell_style)
        ],
        [
            Paragraph("<i>OBV<sub>t</sub></i>", table_cell_style),
            Paragraph("On-Balance Volume", table_cell_style),
            Paragraph("Volume Predictor", table_cell_style),
            Paragraph("<i>OBV<sub>t-1</sub> &plusmn; V<sub>t</sub></i> (added on up weeks, subtracted on down)", table_cell_style),
            Paragraph("Confirms price trends by measuring underlying institutional liquidity and trading volume flow.", table_cell_style)
        ],
        [
            Paragraph("<i>R<sub>f</sub></i>", table_cell_style),
            Paragraph("Risk-Free Rate", table_cell_style),
            Paragraph("Exogenous Parameter", table_cell_style),
            Paragraph("(1 + <i>R<sub>annual</sub></i>)<sup>1/52</sup> - 1", table_cell_style),
            Paragraph("De-annualized CBN 91-day Treasury Bill yield. Used to calculate Sharpe and Sortino ratios.", table_cell_style)
        ]
    ]
    
    col_widths = [0.8*inch, 1.3*inch, 1.0*inch, 1.7*inch, 1.7*inch]
    var_table = Table(table_data, colWidths=col_widths, repeatRows=1)
    var_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F2F2F2')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    
    story.append(var_table)
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<i>(Note: In the formulations above, P<sub>t</sub> represents the weekly closing price, H is the high price, L is the low price, V<sub>t</sub> is the weekly volume, EMA is the Exponential Moving Average, and TR is the True Range).</i>",
        body_style
    ))
    
    # 4. 3.5 Data Preprocessing and Feature Scaling
    story.append(Paragraph("3.5 Data Preprocessing and Feature Scaling", section_title_style))
    story.append(Paragraph(
        "Prior to feeding the financial time-series data into the machine learning models, rigorous data preprocessing is required to ensure data integrity and model stability. First, missing values, which frequently arise in the Nigerian Exchange Group (NGX) due to market closures, public holidays, or reporting inconsistencies, will be handled using forward-fill imputation. This technique preserves the chronological continuity of historical price trends and prevents detrimental gaps in the sequential learning process of the algorithms.",
        body_style
    ))
    story.append(Paragraph(
        "Consequently, this study applies Min-Max normalization to transform all raw prices and technical indicators into a standardized range. The Min-Max scaling formula utilized is expressed as:",
        body_style
    ))
    
    formula_style = ParagraphStyle(
        'FormulaStyle2',
        parent=body_style,
        alignment=1, # Centered
        fontName='Times-Italic',
        spaceBefore=6,
        spaceAfter=10
    )
    story.append(Paragraph("x<sub>scaled</sub> = (x<sub>i</sub> - min(x)) / (max(x) - min(x))", formula_style))
    story.append(Paragraph(
        "where <i>x<sub>scaled</sub></i> represents the normalized value of the input feature <i>x<sub>i</sub></i>, and <i>min(x)</i> and <i>max(x)</i> represent the minimum and maximum values of that specific feature over the defined period, respectively.",
        body_style
    ))
    story.append(Paragraph(
        "Although tree-based ensemble models such as Random Forest and XGBoost are generally scale-invariant at the individual split level, Min-Max normalization is applied to ensure consistent data representation across all 13 technical indicators and to facilitate comparability across feature-derived indicators versus bounded oscillators such as RSI.",
        body_style
    ))
    
    # 5. 3.6 Software and Implementation Tools
    story.append(Paragraph("3.6 Software and Implementation Tools", section_title_style))
    story.append(Paragraph(
        "To ensure the complete reproducibility and accuracy of the empirical pipeline (from data preprocessing and hyperparameter tuning to machine learning predictions and Mean-CVaR portfolio optimization), all computational procedures in this study are executed programmatically. The methodology is implemented entirely within the Python programming language. Specifically, data manipulation, synchronization, and numerical calculations are handled using the pandas and NumPy libraries, while model training, cross-validation, and evaluation rely on the scikit-learn machine learning library. Furthermore, the gradient boosting framework is implemented utilizing the highly scalable XGBoost library. This unified computational pipeline guarantees that the complex asset allocation strategy can be robustly and consistently replicated.",
        body_style
    ))
    
    # 6. 3.7 Sources of Data
    story.append(Paragraph("3.7 Sources of Data", section_title_style))
    story.append(Paragraph(
        "The study is completely based on secondary data covering 2010-2025. Secondary data are appropriate for this study since the research entails stock trading data which are regularly published by reputable financial organizations.",
        body_style
    ))
    story.append(Paragraph(
        "The data on the stock trading history of the individual companies under the NGX Pension Index are sourced primarily from Investing.com. The primary dataset consists of the historical daily closing prices, high/low prices, and trading volumes for the selected assets, which were programmatically downloaded from the Investing.com financial database. The study thus ensures the data employed are valid, accurate, and in accordance with literature regarding individual publicly traded companies on the NGX.",
        body_style
    ))

    doc.build(story)
    print(f"[OK] Generated clean end of Chapter 3: {output_path}")

if __name__ == '__main__':
    generate_clean_ch3_end_pdf()
