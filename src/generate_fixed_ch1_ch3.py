import os
import re
from pypdf import PdfReader

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def clean_extracted_text(text):
    # 1. Diacritics & Author Names
    text = re.sub(r'[\?\ufffdn]*l\s*usarczyk', 'Slusarczyk', text, flags=re.IGNORECASE)
    text = re.sub(r'[\?\ufffdn]*lepaczuk', 'Slepaczuk', text, flags=re.IGNORECASE)
    text = re.sub(r'Mart[\?\ufffd\si]*nez\s*-\s*Barbero', 'Martínez-Barbero', text, flags=re.IGNORECASE)
    text = re.sub(r'Mart[\?\ufffd\si]*nez\s*Barbero', 'Martínez-Barbero', text, flags=re.IGNORECASE)
    text = re.sub(r'Mart[\?\ufffd\si]*nez', 'Martínez', text, flags=re.IGNORECASE)
    text = re.sub(r'Markowitz[\?\ufffd]?s', "Markowitz's", text, flags=re.IGNORECASE)
    
    # 2. Hyphenations & PDF line break split words
    text = re.sub(r'optimiza-\s*tion', 'optimization', text, flags=re.IGNORECASE)
    text = re.sub(r'predict-\s*ive', 'predictive', text, flags=re.IGNORECASE)
    text = re.sub(r'diversifica-\s*tion', 'diversification', text, flags=re.IGNORECASE)
    text = re.sub(r'characteris-\s*tics', 'characteristics', text, flags=re.IGNORECASE)
    text = re.sub(r'methodol-\s*ogy', 'methodology', text, flags=re.IGNORECASE)

    # 3. Clean Bullet Symbols (convert \uf0b7, \uf0a7, ? bullet symbols)
    text = re.sub(r'[\uf0b7\uf0a7]\s*', '• ', text)

    # 4. Fix Garbled Math Formulas
    if 'nn+1' in text or 'nnnnn' in text or 'n nn+1' in text or 'nn =' in text:
        text = text.replace(
            "defined as: nn+1 = n(nn)+ nn+1 Where:",
            "defined as:<br/>&nbsp;&nbsp;&nbsp;&nbsp;<b><i>R<sub>i,t+1</sub> = f(x<sub>t</sub>) + &epsilon;<sub>t+1</sub></i></b><br/>Where:"
        )
        text = text.replace(
            "n nn+1is the dependent variable",
            "<i>R<sub>i,t+1</sub></i> is the dependent variable"
        )
        text = text.replace(
            "at time n + 1 . n n represents",
            "at time <i>t + 1</i>. <i>f</i>(<b>x</b><sub>t</sub>) represents"
        )
        text = text.replace(
            "n nn is the multi-dimensional feature vector containing the independent variables strictly observed at the end of week n . n nn+1 is",
            "<b>x</b><sub>t</sub> is the multi-dimensional feature vector containing the independent variables strictly observed at the end of week <i>t</i>. &epsilon;<sub>t+1</sub> is"
        )
        text = text.replace(
            "at timen+ 1 , which are independent of the information set at time n .",
            "at time <i>t + 1</i>, which are independent of the information set at time <i>t</i>."
        )
        text = text.replace(
            "The feature vectornnis mathematically defined as a 13× 1 column vector:",
            "The feature vector <b>x</b><sub>t</sub> is mathematically defined as a 13 &times; 1 column vector:"
        )
        text = text.replace(
            "nn = [ n1,n n2,n .. . n13,n] = [ nnnnn nnnn nnnn nnnn nnnnnn nnnn nn nn−1 nn−2 nn−3 nnnn nnnn nnnn ]",
            "<b>x</b><sub>t</sub> = [ <i>x</i><sub>1,t</sub>, <i>x</i><sub>2,t</sub>, ..., <i>x</i><sub>13,t</sub> ]<sup>T</sup> = [ MACD<sub>t</sub>, PPO<sub>t</sub>, RSI<sub>t</sub>, STOCH<sub>t</sub>, R<sub>t-1</sub>, R<sub>t-2</sub>, R<sub>t-3</sub>, R<sub>t-4</sub>, SMA<sub>t</sub>, ADX<sub>t</sub>, SAR<sub>t</sub>, ATR<sub>t</sub>, OBV<sub>t</sub> ]<sup>T</sup>"
        )
        text = text.replace("The variables within nn are", "The variables within <b>x</b><sub>t</sub> are")

    return text

def generate_clean_chapters_1_3_pdf(output_path="output/pdf/clean_chapters_1_3.pdf"):
    """
    Programmatically generates Chapters 1 to 3 starting directly from Page 2 (excluding Page 1 Title Page).
    All body text is rendered with TA_JUSTIFY alignment, clean bullet list styles, and restored math equations.
    """
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
    
    chapter_header_style = ParagraphStyle(
        'ChapterHeaderStyle',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=14,
        leading=24,
        textColor=colors.black,
        spaceBefore=14,
        spaceAfter=12,
        alignment=1 # Centered
    )

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
        alignment=4 # JUSTIFIED
    )

    bullet_style = ParagraphStyle(
        'AcademicBulletStyle',
        parent=body_style,
        leftIndent=20,
        firstLineIndent=-10,
        spaceAfter=6,
        alignment=4 # JUSTIFIED
    )

    formula_style = ParagraphStyle(
        'FormulaStyle',
        parent=body_style,
        alignment=1, # Centered
        fontName='Times-Italic',
        spaceBefore=6,
        spaceAfter=10
    )

    table_cell_style = ParagraphStyle(
        'TableCellStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=12,
        textColor=colors.black
    )

    table_header_style = ParagraphStyle(
        'TableHeaderStyle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.black
    )

    story = []

    # Read original PDF pages for early text extraction
    pdf_path = "Abdulameen Chapter 1 -3.pdf"
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Source file not found: {pdf_path}")
        
    reader = PdfReader(pdf_path)
    print("Parsing Chapters 1-3 text starting from Page 2 for full ReportLab justification, clean lists & math...")
    
    # Start from Page 2 of original PDF (0-indexed: index 1..41) to keep Page 1 cover page separate
    for p_idx in range(1, 42):
        page_num = p_idx + 1
        
        # Replace page 15 (index 14) with clean page 15 content
        if page_num == 15:
            story.append(Paragraph(
                "resilient portfolio outcomes. While these improved methods exist, their applications in emerging "
                "markets such as the Nigerian Exchange Group (NGX) remains under-explored (Moyoweshumba "
                "& Seitshiro, 2025). This necessitates the study not only for academics and researchers but also "
                "for real decision-making.",
                body_style
            ))
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
            story.append(Spacer(1, 10))
            story.append(Paragraph("CHAPTER TWO", chapter_header_style))
            continue

        raw_text = reader.pages[p_idx].extract_text()
        if not raw_text:
            continue
            
        cleaned_text = clean_extracted_text(raw_text)
        lines = [l.strip() for l in cleaned_text.split('\n') if l.strip()]
        
        # Filter out standalone page numbers
        valid_lines = [l for l in lines if not (l.isdigit() and len(l) <= 3)]
        
        # Build paragraphs
        current_para = []
        for line in valid_lines:
            # Check for bullet item
            is_bullet = line.startswith('•') or line.startswith('-') or line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('4.')
            # Check for section or chapter heading
            is_chapter = bool(re.match(r'^(CHAPTER|Chapter)\s+([A-Z]+|\d+)', line))
            is_section = bool(re.match(r'^\d\.\d(\.\d)?\s+', line)) or (line.isupper() and len(line) < 50 and not line.endswith('.'))
            
            if is_chapter or is_section or is_bullet:
                if current_para:
                    story.append(Paragraph(" ".join(current_para), body_style))
                    current_para = []
                if is_chapter:
                    story.append(Spacer(1, 10))
                    story.append(Paragraph(line, chapter_header_style))
                elif is_section:
                    story.append(Paragraph(line, section_title_style))
                elif is_bullet:
                    story.append(Paragraph(line, bullet_style))
            else:
                current_para.append(line)
                # End paragraph if line ends with period or colon and current has substantial length
                if (line.endswith('.') or line.endswith(':')) and len(" ".join(current_para)) > 200:
                    story.append(Paragraph(" ".join(current_para), body_style))
                    current_para = []
                    
        if current_para:
            story.append(Paragraph(" ".join(current_para), body_style))

    # Append Clean Replacement Pages 43-44 Content
    story.append(Paragraph(
        "shifts forward by one week. The oldest weekly observation is discarded, the most recent observation is absorbed, and the models are retrained.",
        body_style
    ))
    story.append(Paragraph("3.3.2 Model Training and Hyperparameter Tuning", section_title_style))
    story.append(Paragraph(
        "Out-of-the-box machine learning algorithms rarely capture the complex dynamics of financial time series optimally. Therefore, this study employs a Randomized Search Cross-Validation strategy within the training window to efficiently identify the optimal hyperparameter configurations for both models.",
        body_style
    ))
    story.append(Paragraph("The tuning process focuses on penalizing model complexity to prevent overfitting:", body_style))
    story.append(Paragraph(
        "• <b>Random Forest Parameters:</b> The search optimizes the number of trees in the forest (<i>n_estimators</i>), the maximum depth of each tree (<i>max_depth</i>), and the minimum number of samples required to split an internal node (<i>min_samples_split</i>).",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>XGBoost Parameters:</b> The search optimizes the learning rate or step size shrinkage (<i>learning_rate</i>), the maximum tree depth (<i>max_depth</i>), and the minimum loss reduction required to make a further partition (<i>gamma</i>), which directly controls the structural regularization.",
        bullet_style
    ))
    
    story.append(Paragraph("3.3.3 Portfolio Turnover and Transaction Costs", section_title_style))
    story.append(Paragraph(
        "To ensure that the optimized Mean-CVaR portfolio strategy is economically viable and not merely theoretically profitable, it is imperative to account for real-world trading frictions, such as brokerage fees and slippage on the Nigerian Exchange Group (NGX) (Ashrafzadeh et al., 2025). This requires measuring the portfolio turnover, which mathematically quantifies the absolute change in the portfolio's asset weights from one weekly rebalancing period to the next (Zsurkis, Nicolau, & Rodrigues, 2024):",
        body_style
    ))
    story.append(Paragraph("Turnover<sub>t</sub> = &Sigma;<sub>i=1..N</sub> |w<sub>t,i</sub> - w<sub>t<sup>-</sup>,i</sub>|", formula_style))
    story.append(Paragraph(
        "Following standard empirical finance procedures, transaction costs are deducted from gross returns to construct net returns. This study evaluates portfolio performance across three execution-cost regimes: a gross frictionless baseline (0.00%), an institutional PFA execution scenario applying a fixed 75 basis points (0.75%) per rebalancing trade, and a retail execution friction scenario applying 150 basis points (1.50%) to account for brokerage commissions and market slippage on the NGX. Finally, a Net Returns feature column will be constructed by deducting these calculated transaction costs from the gross portfolio returns, providing a rigorous and realistic evaluation of the portfolio's actual out-of-sample performance.",
        body_style
    ))
    
    story.append(Paragraph("3.3.4 Feature Importance Extraction", section_title_style))
    story.append(Paragraph(
        "Due to the criticism of ensemble models of being black boxes in traditional econometrics and to ensure economic interpretability, this study extracts the built-in feature importance scores from the optimized models to determine which of the thirteen technical indicators exert the strongest predictive influence on NGX equity returns.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Random Forest Interpretation:</b> Importance is calculated using the Mean Decrease in Impurity (Gini Importance). It measures the total reduction of the Mean Squared Error (MSE) brought by that specific feature across all trees in the forest.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>XGBoost Interpretation:</b> Importance is measured using Information Gain. It evaluates the relative contribution of each feature to the model by calculating the improvement in accuracy it provides to the branches it is on.",
        bullet_style
    ))
    story.append(Paragraph("3.3.5 Evaluation Metrics for Forecasting and Portfolio Performance", section_title_style))

    # Append Pages 45 & 46 Content (indices 44 & 45 in reader)
    for p_idx in [44, 45]:
        raw_text = reader.pages[p_idx].extract_text()
        if not raw_text:
            continue
        cleaned_text = clean_extracted_text(raw_text)
        lines = [l.strip() for l in cleaned_text.split('\n') if l.strip()]
        valid_lines = [l for l in lines if not (l.isdigit() and len(l) <= 3)]
        current_para = []
        for line in valid_lines:
            is_section = bool(re.match(r'^\d\.\d(\.\d)?\s+', line))
            if is_section:
                if current_para:
                    story.append(Paragraph(" ".join(current_para), body_style))
                    current_para = []
                story.append(Paragraph(line, section_title_style))
            else:
                current_para.append(line)
                if line.endswith('.') and len(" ".join(current_para)) > 200:
                    story.append(Paragraph(" ".join(current_para), body_style))
                    current_para = []
        if current_para:
            story.append(Paragraph(" ".join(current_para), body_style))

    # Append Clean End of Chapter 3 (Section 3.3.5 Benchmarks to 3.7 Data Sources)
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
    
    story.append(Paragraph("3.5 Data Preprocessing and Feature Scaling", section_title_style))
    story.append(Paragraph(
        "Prior to feeding the financial time-series data into the machine learning models, rigorous data preprocessing is required to ensure data integrity and model stability. First, missing values, which frequently arise in the Nigerian Exchange Group (NGX) due to market closures, public holidays, or reporting inconsistencies, will be handled using forward-fill imputation. This technique preserves the chronological continuity of historical price trends and prevents detrimental gaps in the sequential learning process of the algorithms.",
        body_style
    ))
    story.append(Paragraph(
        "Consequently, this study applies Min-Max normalization to transform all raw prices and technical indicators into a standardized range. The Min-Max scaling formula utilized is expressed as:",
        body_style
    ))
    story.append(Paragraph("x<sub>scaled</sub> = (x<sub>i</sub> - min(x)) / (max(x) - min(x))", formula_style))
    story.append(Paragraph(
        "where <i>x<sub>scaled</sub></i> represents the normalized value of the input feature <i>x<sub>i</sub></i>, and <i>min(x)</i> and <i>max(x)</i> represent the minimum and maximum values of that specific feature over the defined period, respectively.",
        body_style
    ))
    story.append(Paragraph(
        "Although tree-based ensemble models such as Random Forest and XGBoost are generally scale-invariant at the individual split level, Min-Max normalization is applied to ensure consistent data representation across all 13 technical indicators and to facilitate comparability across feature-derived indicators versus bounded oscillators such as RSI.",
        body_style
    ))
    
    story.append(Paragraph("3.6 Software and Implementation Tools", section_title_style))
    story.append(Paragraph(
        "To ensure the complete reproducibility and accuracy of the empirical pipeline (from data preprocessing and hyperparameter tuning to machine learning predictions and Mean-CVaR portfolio optimization), all computational procedures in this study are executed programmatically. The methodology is implemented entirely within the Python programming language. Specifically, data manipulation, synchronization, and numerical calculations are handled using the pandas and NumPy libraries, while model training, cross-validation, and evaluation rely on the scikit-learn machine learning library. Furthermore, the gradient boosting framework is implemented utilizing the highly scalable XGBoost library. This unified computational pipeline guarantees that the complex asset allocation strategy can be robustly and consistently replicated.",
        body_style
    ))
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
    print(f"[OK] Generated clean fully-justified Chapters 1-3 PDF (Starting Page 2) with clean lists & math: {output_path}")

if __name__ == '__main__':
    generate_clean_chapters_1_3_pdf()
