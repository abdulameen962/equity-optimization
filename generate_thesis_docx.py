import os
import re
import pandas as pd
from pypdf import PdfReader

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, hex_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def add_styled_paragraph(doc, text, style_type='body', space_before=0, space_after=0):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    
    if style_type == 'body':
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif style_type == 'chapter_header':
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif style_type == 'chapter_header_center':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif style_type == 'section_title':
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif style_type == 'bullet':
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Inches(0.25)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif style_type == 'formula':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.italic = True
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif style_type == 'caption':
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        run.font.italic = True
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif style_type == 'reference':
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_table_to_docx(doc, headers, data):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'
    
    # Header Row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], 'F2F2F2')
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)
            
    # Data Rows
    for r_idx, row_data in enumerate(data):
        row_cells = table.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def clean_extracted_text(text):
    text = re.sub(r'[\?\ufffdn]*l\s*usarczyk', 'Slusarczyk', text, flags=re.IGNORECASE)
    text = re.sub(r'[\?\ufffdn]*lepaczuk', 'Slepaczuk', text, flags=re.IGNORECASE)
    text = re.sub(r'Mart[\?\ufffd\si]*nez\s*-\s*Barbero', 'Martínez-Barbero', text, flags=re.IGNORECASE)
    text = re.sub(r'Mart[\?\ufffd\si]*nez\s*Barbero', 'Martínez-Barbero', text, flags=re.IGNORECASE)
    text = re.sub(r'Mart[\?\ufffd\si]*nez', 'Martínez', text, flags=re.IGNORECASE)
    return text

def generate_complete_thesis_docx(output_path="Abdulameen_Complete_Thesis_Chapters_1_5.docx"):
    print("Building complete thesis DOCX document...")
    doc = Document()
    
    # 1. Page Margins (1.0 inch all sides)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Configure Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    # Standalone Centered Title / Cover Page (Page 1)
    add_styled_paragraph(
        doc,
        "Equity Return Forecasting on Tail-Risk-Aware Portfolio Optimization on the\nNigerian Exchange Group (NGX)",
        'chapter_header_center',
        space_before=100,
        space_after=24
    )
    add_styled_paragraph(doc, "BY", 'chapter_header_center', space_before=12, space_after=12)
    add_styled_paragraph(doc, "SANNI ABDUL-AMEEN OLUWADARASIMI", 'chapter_header_center', space_before=12, space_after=6)
    add_styled_paragraph(doc, "ECN/2021/158", 'chapter_header_center', space_before=6, space_after=100)
    doc.add_page_break()
    
    # =========================================================================
    # PART 1: CHAPTERS 1 - 3 (EARLY SECTIONS FROM ORIGINAL PDF + FIXES)
    # =========================================================================
    pdf_path = "Abdulameen Chapter 1 -3.pdf"
    if os.path.exists(pdf_path):
        reader = PdfReader(pdf_path)
        print(f"Processing early PDF chapters ({len(reader.pages)} pages source)...")
        
        for p_idx in range(1, len(reader.pages)):
            page_num = p_idx + 1
            
            # Skip page 15 (we use clean Page 15 fix)
            if page_num == 15:
                # Clean Page 15 replacement
                add_styled_paragraph(
                    doc,
                    "resilient portfolio outcomes. While these improved methods exist, their applications in emerging "
                    "markets such as the Nigerian Exchange Group (NGX) remains under-explored (Moyoweshumba "
                    "& Seitshiro, 2025). This necessitates the study not only for academics and researchers but also "
                    "for real decision-making.",
                    'body'
                )
                add_styled_paragraph(doc, "1.6 Scope of the Study", 'section_title')
                add_styled_paragraph(
                    doc,
                    "This study examines the effect of equity-return forecasting on tail-risk aware optimization on the "
                    "Nigerian Exchange Group (NGX). Weekly price data on selected companies in the NGX Pension Index "
                    "between the period of 2010 - 2025 will be utilized for the study. This study could not "
                    "extend beyond the selected time frame due to unavailability of price data due to the date of "
                    "companies' listings. Most available data on price data on publicly listed companies were sourced "
                    "from ng.investing.com which was limited to the timeframe of the study.",
                    'body'
                )
                add_styled_paragraph(doc, "1.7 Organization of the Study", 'section_title')
                add_styled_paragraph(
                    doc,
                    "This study is divided into five chapters. The first chapter of this study provides the background "
                    "of the study, which will further prove the need for the study. Chapter two presents the theoretical "
                    "and empirical review of relevant studies in the study's subject matter. The theoretical perspective "
                    "in the second chapter will introduce the adopted models in chapter three. Data analysis and "
                    "presentation will be carried out in chapter four, while the concluding comments that include "
                    "summary, conclusion, recommendations, and suggestions for further studies will be made in "
                    "chapter five.",
                    'body'
                )
                add_styled_paragraph(doc, "CHAPTER TWO", 'chapter_header_center')
                continue
                
            # Skip pages 43 & 44 (we use clean replacement below)
            if page_num in [43, 44]:
                continue
                
            # Stop PDF processing at page 47 (end of Ch3 early text, replaced by clean_ch3_end)
            if page_num >= 47:
                break
                
            raw_text = reader.pages[p_idx].extract_text()
            if not raw_text:
                continue
                
            cleaned_text = clean_extracted_text(raw_text)
            lines = [l.strip() for l in cleaned_text.split('\n') if l.strip()]
            
            # Filter out stray single digits (page numbers) at top/bottom
            valid_lines = []
            for l in lines:
                if l.isdigit() and len(l) <= 3:
                    continue
                valid_lines.append(l)
                
            if not valid_lines:
                continue
                
            # Group into paragraphs
            current_para = []
            for line in valid_lines:
                # Heading detection
                if (re.match(r'^(Chapter|CHAPTER|\d\.\d|\d\.\d\.\d)', line) or line.isupper()) and len(line) < 80:
                    if current_para:
                        add_styled_paragraph(doc, " ".join(current_para), 'body')
                        current_para = []
                    if line.startswith("CHAPTER") or line.startswith("Chapter"):
                        add_styled_paragraph(doc, line, 'chapter_header')
                    else:
                        add_styled_paragraph(doc, line, 'section_title')
                else:
                    current_para.append(line)
                    
            if current_para:
                add_styled_paragraph(doc, " ".join(current_para), 'body')

    # Add Clean Replacement Pages 43 - 44 Content
    add_styled_paragraph(
        doc,
        "shifts forward by one week. The oldest weekly observation is discarded, the most recent observation is absorbed, and the models are retrained.",
        'body'
    )
    add_styled_paragraph(doc, "3.3.2 Model Training and Hyperparameter Tuning", 'section_title')
    add_styled_paragraph(
        doc,
        "Out-of-the-box machine learning algorithms rarely capture the complex dynamics of financial time series optimally. Therefore, this study employs a Randomized Search Cross-Validation strategy within the training window to efficiently identify the optimal hyperparameter configurations for both models.",
        'body'
    )
    add_styled_paragraph(doc, "The tuning process focuses on penalizing model complexity to prevent overfitting:", 'body')
    add_styled_paragraph(
        doc,
        "• Random Forest Parameters: The search optimizes the number of trees in the forest (n_estimators), the maximum depth of each tree (max_depth), and the minimum number of samples required to split an internal node (min_samples_split).",
        'bullet'
    )
    add_styled_paragraph(
        doc,
        "• XGBoost Parameters: The search optimizes the learning rate or step size shrinkage (learning_rate), the maximum tree depth (max_depth), and the minimum loss reduction required to make a further partition (gamma), which directly controls the structural regularization.",
        'bullet'
    )
    
    add_styled_paragraph(doc, "3.3.3 Portfolio Turnover and Transaction Costs", 'section_title')
    add_styled_paragraph(
        doc,
        "To ensure that the optimized Mean-CVaR portfolio strategy is economically viable and not merely theoretically profitable, it is imperative to account for real-world trading frictions, such as brokerage fees and slippage on the Nigerian Exchange Group (NGX) (Ashrafzadeh et al., 2025). This requires measuring the portfolio turnover, which mathematically quantifies the absolute change in the portfolio's asset weights from one weekly rebalancing period to the next (Zsurkis, Nicolau, & Rodrigues, 2024):",
        'body'
    )
    add_styled_paragraph(doc, "Turnover_t = Sum_{i=1..N} |w_{t,i} - w_{t^-,i}|", 'formula')
    add_styled_paragraph(
        doc,
        "Following standard empirical finance procedures, transaction costs are deducted from gross returns to construct net returns. This study evaluates portfolio performance across three execution-cost regimes: a gross frictionless baseline (0.00%), an institutional PFA execution scenario applying a fixed 75 basis points (0.75%) per rebalancing trade, and a retail execution friction scenario applying 150 basis points (1.50%) to account for brokerage commissions and market slippage on the NGX. Finally, a Net Returns feature column will be constructed by deducting these calculated transaction costs from the gross portfolio returns, providing a rigorous and realistic evaluation of the portfolio's actual out-of-sample performance.",
        'body'
    )
    
    add_styled_paragraph(doc, "3.3.4 Feature Importance Extraction", 'section_title')
    add_styled_paragraph(
        doc,
        "Due to the criticism of ensemble models of being black boxes in traditional econometrics and to ensure economic interpretability, this study extracts the built-in feature importance scores from the optimized models to determine which of the thirteen technical indicators exert the strongest predictive influence on NGX equity returns.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "• Random Forest Interpretation: Importance is calculated using the Mean Decrease in Impurity (Gini Importance). It measures the total reduction of the Mean Squared Error (MSE) brought by that specific feature across all trees in the forest.",
        'bullet'
    )
    add_styled_paragraph(
        doc,
        "• XGBoost Interpretation: Importance is measured using Information Gain. It evaluates the relative contribution of each feature to the model by calculating the improvement in accuracy it provides to the branches it is on.",
        'bullet'
    )
    add_styled_paragraph(doc, "3.3.5 Evaluation Metrics for Forecasting and Portfolio Performance", 'section_title')

    # =========================================================================
    # PART 2: END OF CHAPTER 3 (BENCHMARKS, HYPOTHESIS TESTING, VARIABLES TABLE)
    # =========================================================================
    add_styled_paragraph(doc, "3. Benchmark Portfolios for Evaluation", 'section_title')
    add_styled_paragraph(
        doc,
        "To rigorously evaluate the economic value and true out-of-sample performance of the advanced ML-CVaR optimization strategy, it is essential to measure its results against standard baseline portfolios. By utilizing these benchmarks alongside the metrics above, the study empirically validates whether the non-linear machine learning forecasts, combined with CVaR tail-risk constraints, genuinely deliver superior risk-adjusted performance on the Nigerian Exchange.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "• The 1/N Equally Weighted Portfolio (EWP): In this naive diversification strategy, investment capital is simply divided uniformly across all selected stocks without relying on any parameter estimation or complex optimization algorithms. In an EWP strategy, each asset in the portfolio holds an equal weight of w_i = 1/N. This rule is chosen as a primary benchmark because it is easy to implement and continues to be a standard, highly effective allocation rule utilized by investors.",
        'bullet'
    )
    add_styled_paragraph(
        doc,
        "• The Buy-and-Hold Market Index Strategy: This is a passive strategy that involves buying and holding the market index itself (in this case, the NGX Pension Index). This serves as a critical baseline to demonstrate whether active portfolio management based on machine learning predictions genuinely provides superior risk-adjusted returns compared to general market movements. Initialized at equal weights w_{0,i} = 1/N at t = 0, Buy-and-Hold weights drift passively with asset price returns (w_{t+1,i} proportional to w_{t,i}(1 + R_{t+1,i})) with zero rebalancing turnover post week 0.",
        'bullet'
    )
    
    add_styled_paragraph(doc, "3.3.6 Hypothesis Testing and Statistical Significance Framework", 'section_title')
    add_styled_paragraph(
        doc,
        "To determine whether observed differences in risk-adjusted performance (Sharpe and Sortino ratios) and weekly portfolio returns between candidate strategies and baseline benchmarks are statistically meaningful or merely artifacts of sampling variation, this study implements a decision-theoretic inferential hypothesis testing framework. In emerging equity markets such as the NGX, where asset returns display pronounced non-normality, negative skewness, and heavy tails, traditional parametric Z-tests can yield misleading p-values. Therefore, both parametric and robust non-parametric bootstrap procedures are employed:",
        'body'
    )
    add_styled_paragraph(
        doc,
        "1. Jobson and Korkie (1981) Test with Memmel (2007) Correction: Evaluates the null hypothesis of Sharpe ratio equality H0: Sharpe_A = Sharpe_B for two correlated portfolios. Memmel (2007) corrects the asymptotic variance under portfolio correlation rho: Z = (Sharpe_A - Sharpe_B) / sqrt( (1 / T) [ 2(1 - rho) + 0.5(Sharpe_A^2 + Sharpe_B^2 - 2 Sharpe_A Sharpe_B rho^2) ] ) where T is the number of out-of-sample weekly observations.",
        'bullet'
    )
    add_styled_paragraph(
        doc,
        "2. Ledoit and Wolf (2008) Circular Block Bootstrap Test for Sharpe Ratio Equality: Resamples overlapping blocks of length b = 5 weeks across B = 2,000 bootstrap replicates to preserve time-series autocorrelation and conditional heteroskedasticity (GARCH effects). The empirical p-value evaluates H0: Sharpe_A - Sharpe_B = 0.",
        'bullet'
    )
    add_styled_paragraph(
        doc,
        "3. Ledoit and Wolf (2011) Bootstrap Test for Sortino Ratio Equality: Extends non-parametric block bootstrapping to downside risk, evaluating H0: Sortino_A - Sortino_B = 0 to verify excess return per unit of downside risk.",
        'bullet'
    )
    add_styled_paragraph(
        doc,
        "4. Non-Parametric Wilcoxon Signed-Rank Test and Paired t-Test: Evaluates whether weekly differential returns Delta R_t = R_{A,t} - R_{B,t} significantly deviate from zero (H0: E[Delta R_t] = 0).",
        'bullet'
    )
    add_styled_paragraph(
        doc,
        "5. Diebold and Mariano (1995) Test for Predictive Accuracy: Evaluates whether out-of-sample forecasting loss (RMSE) differentials between machine learning models (Random Forest, XGBoost) and the Historical Mean baseline are statistically significant.",
        'bullet'
    )
    
    add_styled_paragraph(doc, "3.4 Description and Measurement of Study Variables", 'section_title')
    add_styled_paragraph(
        doc,
        "The variables utilized in this study are partitioned into the target variable, the thirteen machine learning feature inputs (extracted exclusively from the weekly OHLCV data), and the exogenous risk-free rate parameter required for portfolio evaluation.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "Below is the tabular summary of all variables, their mathematical measurements, and their operational roles within the predictive and optimization models.",
        'body'
    )
    
    # Table of Variables
    var_headers = ["Variable Symbol", "Variable Name", "Category", "Measurement / Formulation", "Operational Role"]
    var_rows = [
        ["R_{i,t+1}", "Weekly Log Return", "Target Variable", "ln(P_{i,t} / P_{i,t-1})", "Primary dependent variable. Continuous yield for upcoming week."],
        ["MACD_t", "Moving Average Conv Divergence", "Momentum", "EMA_12(P_t) - EMA_26(P_t)", "Measures velocity of price changes to identify short-term momentum shifts."],
        ["PPO_t", "Percentage Price Oscillator", "Momentum", "[EMA_12 - EMA_26] / EMA_26 * 100", "Normalized MACD for cross-asset comparison."],
        ["RSI_t", "Relative Strength Index", "Momentum", "100 - [100 / (1 + RS)]", "Identifies overbought (>70) or oversold (<30) market conditions."],
        ["STOCH_t", "Stochastic Oscillator (%K)", "Momentum", "[(P_t - L_14) / (H_14 - L_14)] * 100", "Evaluates closing price relative to 14-week high-low range."],
        ["R_{i,t-n}", "Lagged Returns (Lags 1-4)", "Autoregressive", "R_{i,t-1}, R_{i,t-2}, R_{i,t-3}, R_{i,t-4}", "Feeds past 4 weeks of return momentum into ML algorithms."],
        ["SMA_t", "Simple Moving Average", "Trend", "(1/n) Sum_{k=0..n-1} P_{t-k}", "Smooths weekly price data to identify baseline trend direction."],
        ["ADX_t", "Average Directional Index", "Trend", "100 * MA(|+DI - -DI| / (+DI + -DI))", "Quantifies absolute strength of a trend."],
        ["SAR_t", "Parabolic SAR", "Trend", "SAR_{t-1} + alpha(EP_{t-1} - SAR_{t-1})", "Signals entry/exit points and trend reversals."],
        ["ATR_t", "Average True Range", "Volatility", "(1/n) Sum TR_i", "Measures intra-week market volatility and drop magnitude."],
        ["OBV_t", "On-Balance Volume", "Volume", "OBV_{t-1} +/- V_t", "Measures underlying institutional liquidity and volume flow."],
        ["R_f", "Risk-Free Rate", "Exogenous", "(1 + R_annual)^(1/52) - 1", "De-annualized CBN 91-day T-Bill yield for Sharpe/Sortino."]
    ]
    add_table_to_docx(doc, var_headers, var_rows)
    add_styled_paragraph(
        doc,
        "(Note: In the formulations above, P_t represents the weekly closing price, H is the high price, L is the low price, V_t is the weekly volume, EMA is the Exponential Moving Average, and TR is the True Range).",
        'caption'
    )
    
    add_styled_paragraph(doc, "3.5 Data Preprocessing and Feature Scaling", 'section_title')
    add_styled_paragraph(
        doc,
        "Prior to feeding the financial time-series data into the machine learning models, rigorous data preprocessing is required to ensure data integrity and model stability. First, missing values, which frequently arise in the Nigerian Exchange Group (NGX) due to market closures, public holidays, or reporting inconsistencies, will be handled using forward-fill imputation. This technique preserves the chronological continuity of historical price trends and prevents detrimental gaps in the sequential learning process of the algorithms.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "Consequently, this study applies Min-Max normalization to transform all raw prices and technical indicators into a standardized range. The Min-Max scaling formula utilized is expressed as:",
        'body'
    )
    add_styled_paragraph(doc, "x_scaled = (x_i - min(x)) / (max(x) - min(x))", 'formula')
    add_styled_paragraph(
        doc,
        "where x_scaled represents the normalized value of the input feature x_i, and min(x) and max(x) represent the minimum and maximum values of that specific feature over the defined period, respectively.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "Although tree-based ensemble models such as Random Forest and XGBoost are generally scale-invariant at the individual split level, Min-Max normalization is applied to ensure consistent data representation across all 13 technical indicators and to facilitate comparability across feature-derived indicators versus bounded oscillators such as RSI.",
        'body'
    )
    
    add_styled_paragraph(doc, "3.6 Software and Implementation Tools", 'section_title')
    add_styled_paragraph(
        doc,
        "To ensure the complete reproducibility and accuracy of the empirical pipeline (from data preprocessing and hyperparameter tuning to machine learning predictions and Mean-CVaR portfolio optimization), all computational procedures in this study are executed programmatically. The methodology is implemented entirely within the Python programming language. Specifically, data manipulation, synchronization, and numerical calculations are handled using the pandas and NumPy libraries, while model training, cross-validation, and evaluation rely on the scikit-learn machine learning library. Furthermore, the gradient boosting framework is implemented utilizing the highly scalable XGBoost library. This unified computational pipeline guarantees that the complex asset allocation strategy can be robustly and consistently replicated.",
        'body'
    )
    
    add_styled_paragraph(doc, "3.7 Sources of Data", 'section_title')
    add_styled_paragraph(
        doc,
        "The study is completely based on secondary data covering 2010-2025. Secondary data are appropriate for this study since the research entails stock trading data which are regularly published by reputable financial organizations.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "The data on the stock trading history of the individual companies under the NGX Pension Index are sourced primarily from Investing.com. The primary dataset consists of the historical daily closing prices, high/low prices, and trading volumes for the selected assets, which were programmatically downloaded from the Investing.com financial database. The study thus ensures the data employed are valid, accurate, and in accordance with literature regarding individual publicly traded companies on the NGX.",
        'body'
    )

    # =========================================================================
    # PART 3: CHAPTERS 4 & 5 (EMPIRICAL RESULTS, TABLES, FIGURES, CONCLUSION)
    # =========================================================================
    print("Adding Chapters 4 & 5 to DOCX...")
    add_styled_paragraph(doc, "Chapter 4", 'chapter_header')
    add_styled_paragraph(doc, "4.1 Empirical Results and Discussion", 'section_title')
    add_styled_paragraph(
        doc,
        "This chapter presents the empirical findings of the study on equity return forecasting and tail-risk-aware portfolio optimization "
        "on the Nigerian Exchange Group (NGX). The analysis evaluates 28 liquid equities spanning a 15-year historical period from January 2010 through "
        "December 2025 (835 weekly observations per asset). The dataset encompasses asset universe selection breakdowns, statistical non-normality diagnostics, "
        "machine learning return forecasting under Expanding Rolling Window Walk-Forward Validation, feature importance analysis, and out-of-sample portfolio optimization backtests.",
        'body'
    )
    
    # 4.1.1 Universe Breakdown
    add_styled_paragraph(doc, "4.1.1 Asset Universe Breakdown and Selection Rationale", 'section_title')
    add_styled_paragraph(
        doc,
        "To establish a robust quantitative asset allocation model free from temporal distortion and survivorship bias, "
        "the constituent equities of the NGX Pension Index were evaluated for sample inclusion. A total of 38 equities were audited. "
        "To guarantee a complete 15-year historical dataset (835 weekly observations from 2010 to 2025) required for training machine learning algorithms (2010-2020) "
        "and backtesting out-of-sample portfolio performance (2021-2025), 28 equities with continuous price history were selected. "
        "Conversely, 10 post-2010 listed equities were excluded to prevent artificial data imputation or look-ahead bias. Table 4.0 provides the comprehensive universe breakdown.",
        'body'
    )
    
    add_styled_paragraph(doc, "Table 4.0: NGX Pension Index Asset Universe Breakdown & Exclusion Rationale", 'section_title')
    universe_headers = ["Ticker", "Company Name", "Sector", "Status", "Inclusion / Exclusion Rationale"]
    universe_records = [
        ["CONOIL", "Conoil Plc", "Oil & Gas", "Included", "Complete 15-yr history (2010-2025)"],
        ["CUSTODIAN", "Custodian Investment Plc", "Financial Services", "Included", "Complete 15-yr history (2010-2025)"],
        ["DANGCEM", "Dangote Cement Plc", "Industrial Goods", "Included", "Complete 15-yr history (2010-2025)"],
        ["DANGSUGAR", "Dangote Sugar Refinery Plc", "Consumer Goods", "Included", "Complete 15-yr history (2010-2025)"],
        ["ETI", "Ecobank Transnational Inc.", "Financial Services", "Included", "Complete 15-yr history (2010-2025)"],
        ["FCMB", "FCMB Group Plc", "Financial Services", "Included", "Complete 15-yr history (2010-2025)"],
        ["FIDELITYBK", "Fidelity Bank Plc", "Financial Services", "Included", "Complete 15-yr history (2010-2025)"],
        ["FIDSON", "Fidson Healthcare Plc", "Healthcare", "Included", "Complete 15-yr history (2010-2025)"],
        ["FBNH", "First HoldCo Plc", "Financial Services", "Included", "Complete 15-yr history (2010-2025)"],
        ["GTCO", "Guaranty Trust Holding Co", "Financial Services", "Included", "Complete 15-yr history (2010-2025)"],
        ["GUINNESS", "Guinness Nigeria Plc", "Consumer Goods", "Included", "Complete 15-yr history (2010-2025)"],
        ["JBERGER", "Julius Berger Nigeria Plc", "Construction", "Included", "Complete 15-yr history (2010-2025)"],
        ["WAPCO", "Lafarge Africa Plc", "Industrial Goods", "Included", "Complete 15-yr history (2010-2025)"],
        ["MANSARD", "AXA Mansard Insurance Plc", "Financial Services", "Included", "Complete 15-yr history (2010-2025)"],
        ["NAHCO", "Nigerian Aviation Handling", "Services", "Included", "Complete 15-yr history (2010-2025)"],
        ["NASCON", "Nascon Allied Industries", "Consumer Goods", "Included", "Complete 15-yr history (2010-2025)"],
        ["NESTLE", "Nestle Nigeria Plc", "Consumer Goods", "Included", "Complete 15-yr history (2010-2025)"],
        ["NB", "Nigerian Breweries Plc", "Consumer Goods", "Included", "Complete 15-yr history (2010-2025)"],
        ["OKOMUOIL", "Okomu Oil Palm Plc", "Agriculture", "Included", "Complete 15-yr history (2010-2025)"],
        ["PRESCO", "Presco Plc", "Agriculture", "Included", "Complete 15-yr history (2010-2025)"],
        ["STANBIC", "Stanbic IBTC Holdings", "Financial Services", "Included", "Complete 15-yr history (2010-2025)"],
        ["STERLINGNG", "Sterling Financial Holdings", "Financial Services", "Included", "Complete 15-yr history (2010-2025)"],
        ["TRANSCORP", "Transnational Corp Plc", "Conglomerates", "Included", "Complete 15-yr history (2010-2025)"],
        ["UACN", "UAC of Nigeria Plc", "Conglomerates", "Included", "Complete 15-yr history (2010-2025)"],
        ["UBA", "United Bank for Africa Plc", "Financial Services", "Included", "Complete 15-yr history (2010-2025)"],
        ["UNILEVER", "Unilever Nigeria Plc", "Consumer Goods", "Included", "Complete 15-yr history (2010-2025)"],
        ["WEMABANK", "Wema Bank Plc", "Financial Services", "Included", "Complete 15-yr history (2010-2025)"],
        ["ZENITHBANK", "Zenith Bank Plc", "Financial Services", "Included", "Complete 15-yr history (2010-2025)"],
        ["ACCESSCORP", "Access Holdings Plc", "Financial Services", "Excluded", "Post-2010 restructuring"],
        ["AIRTELAFRI", "Airtel Africa Plc", "Telecoms", "Excluded", "Listed June 2019 (< 15-yr history)"],
        ["ARADEL", "Aradel Holdings Plc", "Oil & Gas", "Excluded", "Listed October 2024 (< 15-yr history)"],
        ["BUAFOODS", "BUA Foods Plc", "Consumer Goods", "Excluded", "Listed January 2022 (< 15-yr history)"],
        ["GEREGU", "Geregu Power Plc", "Utilities / Power", "Excluded", "Listed October 2022 (< 15-yr history)"],
        ["MTNN", "MTN Nigeria Comms Plc", "Telecoms", "Excluded", "Listed May 2019 (< 15-yr history)"],
        ["SEPLAT", "Seplat Energy Plc", "Oil & Gas", "Excluded", "Listed April 2014 (< 15-yr history)"],
        ["TRANSCOHOT", "Transcorp Hotels Plc", "Services", "Excluded", "Listed January 2015 (< 15-yr history)"],
        ["TRANSPOWER", "Transcorp Power Plc", "Utilities / Power", "Excluded", "Listed March 2024 (< 15-yr history)"],
        ["UCAP", "United Capital Plc", "Financial Services", "Excluded", "Listed January 2013 (< 15-yr history)"]
    ]
    add_table_to_docx(doc, universe_headers, universe_records)
    add_styled_paragraph(doc, "Source: Author's classification based on NGX listing records (2026).", 'caption')
    
    # 4.2 Descriptive Statistics
    add_styled_paragraph(doc, "4.2 Descriptive Statistics and Market Characteristics", 'section_title')
    add_styled_paragraph(
        doc,
        "Descriptive statistics were calculated for all 28 evaluated equities to establish distributional properties including mean weekly returns, "
        "standard deviation, minimum, maximum, skewness, and excess kurtosis. As presented in Table 4.1, weekly equity returns on the NGX "
        "exhibit significant dispersion and notable deviations from standard Gaussian properties across all 28 assets.",
        'body'
    )
    
    desc_df = pd.read_csv('output/tables/descriptive_and_diagnostic_stats.csv')
    add_styled_paragraph(doc, "Table 4.1: Descriptive Statistics of 28 NGX Equity Log Returns (2010-2025)", 'section_title')
    t1_headers = ["Ticker", "Mean (%)", "Std Dev (%)", "Min (%)", "Max (%)", "Skewness", "Kurtosis"]
    t1_rows = []
    for _, row in desc_df.iterrows():
        t1_rows.append([
            str(row['Ticker']),
            f"{row['Mean (%)']:.3f}",
            f"{row['Std Dev (%)']:.2f}",
            f"{row['Min (%)']:.2f}",
            f"{row['Max (%)']:.2f}",
            f"{row['Skewness']:.2f}",
            f"{row['Kurtosis']:.2f}"
        ])
    add_table_to_docx(doc, t1_headers, t1_rows)
    add_styled_paragraph(doc, "Source: Author's computation (2026). Note: Kurtosis represents excess kurtosis across all 28 assets.", 'caption')
    
    # 4.3 Diagnostic Tests
    add_styled_paragraph(doc, "4.3 Statistical Non-Normality and Stationarity Diagnostic Tests", 'section_title')
    add_styled_paragraph(
        doc,
        "To evaluate whether the empirical asset return distributions satisfy the classic Markowitz Mean-Variance assumption of Gaussian normality, "
        "formal statistical hypothesis tests were conducted. The Jarque-Bera (JB) test and Shapiro-Wilk (SW) test were evaluated against the null hypothesis "
        "of normality, while the Augmented Dickey-Fuller (ADF) test evaluated time-series stationarity across all 28 assets.",
        'body'
    )
    
    add_styled_paragraph(doc, "Table 4.2: Empirical Non-Normality (JB, SW) and Stationarity (ADF) Diagnostic Tests (All 28 Equities)", 'section_title')
    t2_headers = ["Ticker", "JB Stat", "JB p-val", "SW Stat", "ADF Stat", "ADF p-val", "Stationary"]
    t2_rows = []
    for _, row in desc_df.iterrows():
        t2_rows.append([
            str(row['Ticker']),
            f"{row['JB Stat']:.1f}",
            "< 0.001" if row['JB p-value'] < 0.001 else f"{row['JB p-value']:.3f}",
            f"{row['SW Stat']:.3f}",
            f"{row['ADF Stat']:.2f}",
            "< 0.001" if row['ADF p-value'] < 0.001 else f"{row['ADF p-value']:.3f}",
            str(row['Stationary'])
        ])
    add_table_to_docx(doc, t2_headers, t2_rows)
    add_styled_paragraph(doc, "Source: Author's computation (2026). Rejection of normality across 100% of 28 equities at p < 0.001.", 'caption')
    
    # 4.4 Correlation
    add_styled_paragraph(doc, "4.4 Sectoral Correlation and Multi-Asset Diversification", 'section_title')
    add_styled_paragraph(
        doc,
        "Figure 4.1 displays the 28x28 pairwise return correlation matrix across the sample period. Intra-sector equities (such as Tier-1 Banks GTCO, ZENITHBANK, and UBA) "
        "exhibit strong positive pairwise correlation (ranging from 0.55 to 0.78). Conversely, cross-sector correlations between Industrial Goods (DANGCEM, WAPCO) "
        "and Consumer Goods (NESTLE, DANGSUGAR) remain moderate (0.15 to 0.35), offering substantial structural diversification benefits for multi-asset portfolio construction.",
        'body'
    )
    
    img1_path = 'output/figures/correlation_heatmap.png'
    if os.path.exists(img1_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(img1_path, width=Inches(6.0))
        add_styled_paragraph(doc, "Figure 4.1: NGX 28 Equity Log Return Pairwise Correlation Matrix (2010-2025)", 'caption')
        
    # 4.5 ML Forecasting
    add_styled_paragraph(doc, "4.5 Machine Learning Return Forecasting Results (Walk-Forward Validation)", 'section_title')
    add_styled_paragraph(
        doc,
        "Machine learning models (Random Forest and XGBoost Regressors) were evaluated under a rigorous Expanding Rolling Window Walk-Forward Validation protocol. "
        "To guarantee zero temporal data leakage, feature Min-Max scaling was fit strictly on expanding training windows, and model hyperparameters were optimized "
        "using 5-fold TimeSeriesSplit cross-validation on the initial 2010-2020 training period. Out-of-sample forecasting was conducted across 2021-2025 (~260 weekly steps) "
        "with quarterly model refitting. Table 4.3 presents the predictive performance comparison across all 28 equities against the Historical Mean baseline.",
        'body'
    )
    
    ml_perf_df = pd.read_csv('output/tables/ml_forecasting_performance.csv')
    add_styled_paragraph(doc, "Table 4.3: Out-of-Sample Predictive Performance Metrics across All 28 NGX Equities (2021-2025 Walk-Forward)", 'section_title')
    t3_headers = ["Ticker", "Base RMSE", "RF RMSE", "XGB RMSE", "Base DA (%)", "RF DA (%)", "XGB DA (%)"]
    t3_rows = []
    for _, row in ml_perf_df.iterrows():
        t3_rows.append([
            str(row['Ticker']),
            f"{row['Base RMSE']:.4f}",
            f"{row['RF RMSE']:.4f}",
            f"{row['XGB RMSE']:.4f}",
            f"{row['Base DA (%)']:.1f}%",
            f"{row['RF DA (%)']:.1f}%",
            f"{row['XGB DA (%)']:.1f}%"
        ])
    t3_rows.append([
        "AVERAGE",
        f"{ml_perf_df['Base RMSE'].mean():.4f}",
        f"{ml_perf_df['RF RMSE'].mean():.4f}",
        f"{ml_perf_df['XGB RMSE'].mean():.4f}",
        f"{ml_perf_df['Base DA (%)'].mean():.1f}%",
        f"{ml_perf_df['RF DA (%)'].mean():.1f}%",
        f"{ml_perf_df['XGB DA (%)'].mean():.1f}%"
    ])
    add_table_to_docx(doc, t3_headers, t3_rows)
    add_styled_paragraph(doc, "Source: Author's computation (2026). DA (%) denotes Directional Accuracy across all 28 assets.", 'caption')
    
    add_styled_paragraph(doc, "Econometric Evaluation of Forecasting Performance & Directional Accuracy Mechanics:", 'section_title')
    add_styled_paragraph(
        doc,
        "As reported in Table 4.3, the out-of-sample Root Mean Squared Error (RMSE) across all 28 NGX equities averages 0.0602 for the Historical Mean baseline, "
        "0.0608 for XGBoost, and 0.0627 for Random Forest, while binary directional accuracy hovers around ~37.8%--38.1%. Econometrically, directional accuracy (DA) is a symmetric binary metric that treats minor zero-mean noise (+0.1%) identically to major crash movements (-10%). "
        "At weekly sampling horizons, financial return series are dominated by unobserved news noise, causing flat historical baselines to minimize squared error during quiescent periods. "
        "However, Mean-CVaR portfolio optimization does not rely on binary sign prediction across noise weeks; rather, it depends on cross-sectional magnitude discrimination during extreme left-tail drawdowns. "
        "Tree-based models utilize volume-confirmed momentum (PPO, OBV) and volatility scaling (ATR, ADX) to correctly rank and penalize the bottom assets facing severe downside tail risk. "
        "Consequently, while ML models do not beat the baseline in raw point RMSE or binary directional accuracy, their value lies in providing dynamic expected return vectors into the portfolio optimizer to reorder relative cross-sectional weights during tail events.",
        'body'
    )
    
    # 4.6 Feature Importance
    add_styled_paragraph(doc, "4.6 Feature Importance and Predictive Driver Analysis", 'section_title')
    add_styled_paragraph(
        doc,
        "Figure 4.2 illustrates the relative feature importances derived from Mean Decrease Impurity (MDI) across all trained tree models. "
        "Short-term price momentum features, specifically the Percentage Price Oscillator (PPO) and Relative Strength Index (RSI), alongside On-Balance Volume (OBV) "
        "emerged as the primary drivers of return predictability. Lagged return features (Lag 1 to Lag 4) provided supplementary predictive weight.",
        'body'
    )
    
    img2_path = 'output/figures/feature_importance_bar.png'
    if os.path.exists(img2_path):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.add_run().add_picture(img2_path, width=Inches(5.8))
        add_styled_paragraph(doc, "Figure 4.2: Feature Importance Breakdown across Technical Indicators", 'caption')
        
    # 4.7 Portfolio Backtest
    add_styled_paragraph(doc, "4.7 Out-of-Sample Portfolio Optimization Backtest and Sensitivity Analysis", 'section_title')
    add_styled_paragraph(
        doc,
        "Six portfolio strategies were backtested out-of-sample over the 2021-2025 period: RF-CVaR, XGB-CVaR, Historical-CVaR, Markowitz Mean-Variance Optimization (MVO), "
        "1/N Equal Weighting, and NGX Index Buy-and-Hold. Backtests were evaluated under three distinct market fee regimes: (i) a 1.50% retail transaction fee and market slippage model (150 bps), "
        "(ii) a 0.75% institutional PFA brokerage fee model (75 bps), and (iii) a zero-transaction-cost environment (0.00%) to evaluate gross alpha generation. All strategies incorporated the weekly CBN 91-day T-Bill risk-free rate (0.319% / 18.00% annualized).",
        'body'
    )
    
    port_perf_df = pd.read_csv('output/tables/portfolio_performance_summary.csv')
    add_styled_paragraph(doc, "Table 4.4: Out-of-Sample Portfolio Performance with 1.50% Retail Transaction Fees & Market Slippage", 'section_title')
    t4_headers = ["Strategy", "Ann. Ret (%)", "Ann. Vol (%)", "Sharpe", "Sortino", "VaR 95%", "CVaR 95%", "Max DD (%)"]
    t4_rows = []
    for _, row in port_perf_df.iterrows():
        t4_rows.append([
            str(row['Strategy']),
            f"{row['Annualized Return (%)']:.2f}%",
            f"{row['Annualized Volatility (%)']:.2f}%",
            f"{row['Sharpe Ratio']:.2f}",
            f"{row['Sortino Ratio']:.2f}",
            f"{row['VaR (95%) (%)']:.2f}%",
            f"{row['CVaR (95%) (%)']:.2f}%",
            f"{row['Max Drawdown (%)']:.2f}%"
        ])
    add_table_to_docx(doc, t4_headers, t4_rows)
    add_styled_paragraph(doc, "Source: Author's computation (2026). Backtested under 1.50% retail transaction fee and 0.319% weekly Rf rate.", 'caption')
    
    port_zero_df = pd.read_csv('output/tables/portfolio_performance_zero_cost.csv')
    add_styled_paragraph(doc, "Table 4.5: Out-of-Sample Portfolio Performance under Zero Transaction Fees (Gross Alpha - 0.00%)", 'section_title')
    t5_rows = []
    for _, row in port_zero_df.iterrows():
        t5_rows.append([
            str(row['Strategy']),
            f"{row['Annualized Return (%)']:.2f}%",
            f"{row['Annualized Volatility (%)']:.2f}%",
            f"{row['Sharpe Ratio']:.2f}",
            f"{row['Sortino Ratio']:.2f}",
            f"{row['VaR (95%) (%)']:.2f}%",
            f"{row['CVaR (95%) (%)']:.2f}%",
            f"{row['Max Drawdown (%)']:.2f}%"
        ])
    add_table_to_docx(doc, t4_headers, t5_rows)
    add_styled_paragraph(doc, "Source: Author's computation (2026). Gross performance under zero transaction fee friction.", 'caption')
    
    inst_df = pd.read_csv('output/tables/portfolio_performance_institutional.csv')
    add_styled_paragraph(doc, "Table 4.5b: Out-of-Sample Portfolio Performance under 0.75% Institutional PFA Transaction Fees", 'section_title')
    t5b_headers = ["Strategy", "Ann. Return (%)", "Ann. Vol (%)", "Sharpe", "Sortino", "VaR 95%", "CVaR 95%", "Max DD (%)", "Wk Turnover (%)"]
    t5b_rows = []
    for _, row in inst_df.iterrows():
        t5b_rows.append([
            str(row['Strategy']),
            f"{row['Annualized Return (%)']:.2f}%",
            f"{row['Annualized Volatility (%)']:.2f}%",
            f"{row['Sharpe Ratio']:.2f}",
            f"{row['Sortino Ratio']:.2f}",
            f"{row['VaR (95%) (%)']:.2f}%",
            f"{row['CVaR (95%) (%)']:.2f}%",
            f"{row['Max Drawdown (%)']:.2f}%",
            f"{row['Avg Weekly Turnover (%)']:.2f}%"
        ])
    add_table_to_docx(doc, t5b_headers, t5b_rows)
    add_styled_paragraph(doc, "Source: Author's computation (2026). Out-of-sample period: 2021-2025. 0.75% transaction fee rate reflects institutional PFA brokerage execution.", 'caption')
    
    img3_path = 'output/figures/portfolio_equity_curves.png'
    if os.path.exists(img3_path):
        p_img3 = doc.add_paragraph()
        p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img3.add_run().add_picture(img3_path, width=Inches(6.0))
        add_styled_paragraph(doc, "Figure 4.3: Out-of-Sample Cumulative Wealth Growth Curves (2021-2025)", 'caption')
        
    # 4.7.1 Statistical Significance
    add_styled_paragraph(doc, "4.7.1 Statistical Significance of Portfolio Outperformance across Market Fee Regimes", 'section_title')
    add_styled_paragraph(
        doc,
        "To evaluate whether the risk-adjusted outperformance of active Mean-CVaR strategies over passive benchmarks is statistically significant, "
        "inferential hypothesis testing was conducted across all three market fee regimes. Table 4.6 presents the p-values from Jobson-Korkie (Memmel 2007 correction) Z-tests, "
        "Ledoit-Wolf (2008) circular block bootstrap Sharpe tests, Ledoit-Wolf (2011) downside block bootstrap Sortino tests, and non-parametric Wilcoxon signed-rank tests.",
        'body'
    )
    
    sig_df = pd.read_csv('output/tables/portfolio_significance_tests.csv')
    add_styled_paragraph(doc, "Table 4.6: Multi-Tier Pairwise Hypothesis Testing of Sharpe & Sortino Equality across Fee Regimes", 'section_title')
    t6_headers = ["Fee Regime", "Strategy", "Benchmark", "Sharpe Diff", "Jobson-Korkie p", "LW Sharpe p", "LW Sortino p", "Wilcoxon p"]
    t6_rows = []
    for _, row in sig_df.iterrows():
        t6_rows.append([
            str(row['Fee Regime']),
            str(row['Strategy']),
            str(row['Benchmark']),
            f"{row['Sharpe Diff']:+.2f}",
            f"{row['Jobson-Korkie p-val']:.3f}",
            f"{row['Ledoit-Wolf Sharpe p-val']:.3f}",
            f"{row['Ledoit-Wolf Sortino p-val']:.3f}",
            f"{row['Wilcoxon p-val']:.3f}"
        ])
    add_table_to_docx(doc, t6_headers, t6_rows)
    add_styled_paragraph(doc, "Source: Author's computation (2026). p-values indicate statistical significance (Ledoit-Wolf 2,000 block resamples).", 'caption')
    
    # 4.7.2 Welfare Analysis
    add_styled_paragraph(doc, "4.7.2 Economic Interpretation of Results and Investor Welfare Analysis", 'section_title')
    add_styled_paragraph(
        doc,
        "While empirical portfolio performance is commonly presented in statistical terms (Sharpe ratios, p-values, standard deviations), "
        "it is essential for institutional pension trustees, retail investors, and policy regulators to translate these statistical metrics into direct economic terms and welfare gains. "
        "This section evaluates the practical financial implications of the empirical findings through (i) economic risk-reward interpretation, "
        "(ii) Certainty Equivalent Return (CER) welfare utility analysis, and (iii) real-world Naira wealth accumulation.",
        'body'
    )
    
    add_styled_paragraph(doc, "Table 4.7: Investor Economic Welfare Utility and Certainty Equivalent Return (CER) Analysis across Market Regimes (gamma = 3)", 'section_title')
    welfare_headers = ["Strategy & Regime", "Ann. Return", "Ann. Vol", "Variance Penalty", "CER Utility", "Welfare Gain vs Index"]
    welfare_rows = [
        ["Historical-CVaR (Inst. 0.75%)", "42.12%", "16.15%", "3.91%", "38.21%", "+8.19% (+819 bps)"],
        ["Historical-CVaR (Retail 1.50%)", "41.97%", "16.15%", "3.91%", "38.06%", "+8.17% (+817 bps)"],
        ["RF-CVaR (Inst. 0.75%)", "38.33%", "16.09%", "3.88%", "34.45%", "+4.43% (+443 bps)"],
        ["XGB-CVaR (Inst. 0.75%)", "37.71%", "15.85%", "3.77%", "33.94%", "+3.92% (+392 bps)"],
        ["1/N Equal Weight (Inst. 0.75%)", "37.42%", "18.29%", "5.02%", "32.40%", "+2.38% (+238 bps)"],
        ["RF-CVaR (Retail 1.50%)", "35.37%", "16.17%", "3.92%", "31.45%", "+1.56% (+156 bps)"],
        ["NGX Index Buy-Hold", "35.88%", "19.77%", "5.86%", "30.02%", "Baseline (0 bps)"],
        ["XGB-CVaR (Retail 1.50%)", "33.42%", "15.98%", "3.83%", "29.59%", "-0.30% (-30 bps)"],
        ["Markowitz MVO (Retail 1.50%)", "-20.48%", "53.92%", "43.61%", "-64.09%", "-93.98% (-9398 bps)"]
    ]
    add_table_to_docx(doc, welfare_headers, welfare_rows)
    add_styled_paragraph(doc, "Source: Author's computation (2026). Risk-aversion coefficient gamma = 3. Delta CER represents annual economic welfare gain.", 'caption')
    
    # CHAPTER 5
    add_styled_paragraph(doc, "Chapter 5", 'chapter_header')
    add_styled_paragraph(doc, "5.1 Summary, Conclusion, and Policy Recommendations", 'section_title')
    add_styled_paragraph(doc, "5.1 Summary of the Study", 'section_title')
    add_styled_paragraph(
        doc,
        "This study investigated equity return forecasting and tail-risk-aware portfolio optimization across 28 liquid equities on the Nigerian Exchange Group (NGX) "
        "spanning a 15-year period (2010-2025). The research evaluated non-normality diagnostics, Machine Learning return forecasting (Random Forest and XGBoost) "
        "under Expanding Rolling Window Walk-Forward Validation, and convex Mean-CVaR asset allocation backtesting.",
        'body'
    )
    
    add_styled_paragraph(doc, "5.2 Summary of Empirical Findings and Research Hypotheses", 'section_title')
    add_styled_paragraph(
        doc,
        "1. Non-Normality of NGX Equities: Formal Jarque-Bera and Shapiro-Wilk tests rejected Gaussian normality across 100% of NGX equities (p < 0.001), exhibiting severe negative skewness and excess kurtosis up to 14.46.\n"
        "2. Failure of Markowitz MVO: Unconstrained Markowitz MVO generated severe downside volatility (53.87% - 53.92%) and catastrophic maximum drawdowns (-86.38% retail 1.50% / -71.07% institutional 0.75%), statistically underperforming naively diversified 1/N Equal Weight (Ledoit-Wolf p = 0.025, Wilcoxon p = 0.008) and destroying economic welfare (CER = -64.09%).\n"
        "3. Statistically Significant Gross ML Alpha: Under zero fee friction (0.00%), XGBoost + Mean-CVaR (XGB-CVaR) achieves a statistically significant Sharpe ratio outperformance over passive NGX Index Buy-Hold (1.52 vs 0.91, Ledoit-Wolf bootstrap p = 0.015 < 0.05), empirically confirming that machine learning models extract genuine predictive alpha prior to transaction friction.\n"
        "4. Turnover Drag & Fee Regime Dynamics: Under 0.75% institutional fees, active ML weekly turnover (11.00%) creates a ~3.6% annual fee drag that reduces XGB-CVaR net Sharpe to 1.24 (p = 0.181). Under 1.50% retail fees and slippage, fee drag reaches ~7.2% annually, causing XGB-CVaR net Sharpe to drop to 0.96 (p = 0.770). Across both fee regimes, low-turnover Historical-CVaR (0.38% turnover) retains top net Sharpe ratios (1.48--1.49, p = 0.022) and statistically dominates active ML (pairwise Ledoit-Wolf p = 0.000).\n"
        "5. Economic Welfare & Source of Value: The primary driver of real-world economic surplus on the NGX is tail-risk optimization via CVaR (+819 bps CER gain, +N11.44M net profit per N10M invested over 5 years), rather than dynamic point-forecasting. Market friction neutralizes the marginal predictive gains of ML, making passive tail-risk management the most economically robust strategy post-fees.\n"
        "6. Refutation of Post-Fee ML Superiority: Contrary to naive theoretical assumptions, active Machine Learning forecasting does NOT deliver superior net investment returns under realistic transaction costs (0.75%--1.50%). The research hypothesis proposing net post-fee ML outperformance is empirically rejected. Rather than a limitation, this finding constitutes a primary academic contribution: it cautions market participants against deploying high-turnover predictive models in illiquid, high-friction emerging markets, establishing that structural tail-risk architecture (CVaR) dominates forecasting complexity.",
        'body'
    )
    
    add_styled_paragraph(doc, "5.3 Policy Recommendations", 'section_title')
    add_styled_paragraph(
        doc,
        "Based on the empirical findings, the following policy recommendations are formulated for institutional regulators, fund managers, and market participants:\n\n"
        "1. For Pension Fund Administrators (PFAs) & PENCOM: The National Pension Commission (PENCOM) should update its Investment Guidelines for Fund I, Fund II, and Fund III equity portfolios "
        "to mandate downside tail-risk metrics, specifically Conditional Value-at-Risk (CVaR_0.95), alongside traditional variance. PFAs should adopt CVaR-constrained allocation models to protect pension assets during extreme macroeconomic shocks.\n\n"
        "2. For Securities & Exchange Commission (SEC) & NGX Regulation: Financial market regulators should establish open-access, low-latency API data infrastructure for market participants "
        "to support quantitative risk management. Furthermore, SEC should require asset management firms to publish quarterly CVaR metrics in fund factsheets to enhance retail investor risk transparency.\n\n"
        "3. For Retail & Corporate Investors: Investors should refrain from concentrated single-stock speculation and implement multi-asset sector diversification. Utilizing technical momentum indicators (PPO, RSI) "
        "and volume signals (OBV) provides measurable downside protection against market corrections.",
        'body'
    )
    
    add_styled_paragraph(doc, "5.4 Contribution to Knowledge", 'section_title')
    add_styled_paragraph(
        doc,
        "This research contributes to quantitative finance literature by providing the first comprehensive empirical evaluation of Machine Learning integrated with convex Mean-CVaR optimization "
        "on the Nigerian Exchange Group using a 15-year clean weekly dataset (2010-2025). It establishes the empirical limitations of Markowitz MVO under non-normal market conditions and provides a actionable tail-risk framework for emerging market asset allocation.",
        'body'
    )
    
    add_styled_paragraph(doc, "5.5 Limitations and Suggestions for Further Research", 'section_title')
    add_styled_paragraph(
        doc,
        "1. Macroeconomic Feature Integration: Future research should incorporate macroeconomic factors (such as USD/NGN exchange rate volatility, inflation rates, and Brent crude oil prices) into the ML feature matrix.\n"
        "2. Deep Learning & High-Frequency Architectures: Extending forecasting models to Transformer-based temporal models and Long Short-Term Memory (LSTM) networks on daily or intraday NGX trading data.\n"
        "3. Multi-Period Transaction Cost Optimization: Incorporating transaction cost penalties directly into the CVaR objective function to minimize turnover during high-volatility regimes.",
        'body'
    )
    
    add_styled_paragraph(doc, "5.6 Data and Code Availability Statement", 'section_title')
    add_styled_paragraph(
        doc,
        "To guarantee complete computational reproducibility and scientific transparency, the entire quantitative finance pipeline, encompassing "
        "data cleaning scripts, non-normality diagnostic tests, technical feature extraction (with Welles Wilder's Parabolic SAR), expanding walk-forward machine learning models "
        "(Random Forest and XGBoost with TimeSeriesSplit cross-validation tuning), convex Mean-CVaR linear programming portfolio optimization backtests, and ReportLab PDF synthesis, is "
        "open-source and publicly hosted on GitHub at:\n\n"
        "Repository URL: https://github.com/abdulameen962/equity-optimization",
        'body'
    )
    
    # REFERENCES SECTION
    doc.add_page_break()
    add_styled_paragraph(doc, "References", 'section_title')
    
    references_list = [
        "Adegboyo, O. S., & Sarwar, K. (2025). Modelling and forecasting of Nigeria stock market volatility. Future Business Journal, 11(1), Article 124. https://doi.org/10.1186/s43093-025-00536-4",
        "Ajiga, D. I., Adeleye, R. A., Tubokirifuruar, T. S., Bello, B. G., Ndubuisi, N. L., Asuzu, O. F., & Owolabi, O. R. (2024). Machine learning for stock market forecasting: A review of models and accuracy. Finance & Accounting Research Journal, 6(2).",
        "Al-Shboul, M., & Alfzari, S. (2025). Predictive analytics in portfolio management: A fusion of AI and investment economics for optimal risk-return trade-offs. International Review of Management and Marketing, 15(1).",
        "Alim, W., Khan, N. U., Zhang, V. W., Cai, H. H., Mikhaylov, A., & Yuan, Q. (2024). Influence of political stability on the stock market returns and volatility: GARCH and EGARCH approach. Financial Innovation.",
        "Alotaibi, T. S., Dalla Valle, L., & Craven, M. J. (2022). The worst case GARCH-copula CVaR approach for portfolio optimisation: Evidence from financial markets. Journal of Risk and Financial Management, 15(10), Article 482.",
        "Arif, U., Sohail, M. T., & Majeed, M. I. (2020). Portfolio optimization with mean-variance & mean-CVaR: Evidence from Pakistan stock market. International Journal of Management Research & Emerging Sciences, 10(2), 215-226.",
        "Ashrafzadeh, M., Sadrani, M., & Zolfani, S. H. (2025). Clustering-based return prediction model for stock pre-selection in portfolio optimization. Results in Engineering, 27, Article 106263.",
        "Bodnar, T., Lindholm, M., Niklasson, V., & Thorsen, E. (2022). Bayesian portfolio selection using VaR and CVaR. Applied Mathematics and Computation, 427, Article 127120.",
        "Campbell, J. Y., & Viceira, L. M. (2002). Strategic asset allocation: Portfolio choice for long-term investors. Oxford University Press.",
        "Chaweewanchon, A., & Chaysiri, R. (2022). Markowitz mean-variance portfolio optimization with predictive stock selection using machine learning. International Journal of Financial Studies, 10(3), Article 64.",
        "Diebold, F. X., & Mariano, R. S. (1995). Comparing predictive accuracy. Journal of Business & Economic Statistics, 13(3), 253-263."
    ]
    
    for ref in references_list:
        add_styled_paragraph(doc, ref, 'reference')
        
    doc.save(output_path)
    print(f"[OK] Successfully generated complete thesis DOCX: {output_path}")

if __name__ == '__main__':
    generate_complete_thesis_docx()
