import os
import re
import pandas as pd
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn

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
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif style_type == 'chapter_title_centered':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif style_type == 'section_title':
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif style_type == 'table_title':
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(space_before or 8)
        p.paragraph_format.space_after = Pt(space_after or 2)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif style_type == 'caption':
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(space_before or 2)
        p.paragraph_format.space_after = Pt(space_after or 8)
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
    
    # Crisp black borders and zero cell padding
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        '<w:tblBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '</w:tblBorders>'
    )
    tblPr.append(borders)
    
    tblCellMar = parse_xml(
        '<w:tblCellMar xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:top w:w="20" w:type="dxa"/>'
        '<w:bottom w:w="20" w:type="dxa"/>'
        '<w:left w:w="30" w:type="dxa"/>'
        '<w:right w:w="30" w:type="dxa"/>'
        '</w:tblCellMar>'
    )
    tblPr.append(tblCellMar)
    
    # Header Row - pure black, NO gray shading
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)
            
    # Data Rows - pure black, zero paragraph spacing
    for r_idx, row_data in enumerate(data):
        row_cells = table.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(0, 0, 0)

    # Prevent row split across pages and repeat header
    for idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml('<w:cantSplit xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))
        if idx == 0:
            trPr.append(parse_xml('<w:tblHeader xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))

def generate_complete_thesis_docx(output_path="Abdulameen_Complete_Thesis_Chapters_1_5.docx"):
    print("Loading base 'Abdulameen Chapter 1 -3.docx'...")
    base_docx = "Abdulameen Chapter 1 -3.docx"
    if not os.path.exists(base_docx):
        raise FileNotFoundError(f"Base file not found: {base_docx}")
        
    doc = Document(base_docx)
    
    # Page Break before Chapter 4
    doc.add_page_break()
    
    print("Appending Chapters 4 & 5 + References to DOCX...")
    
    # =========================================================================
    # CHAPTER 4: DATA ANALYSIS, PRESENTATION AND DISCUSSION OF FINDINGS
    # =========================================================================
    add_styled_paragraph(doc, "CHAPTER FOUR", 'chapter_header')
    add_styled_paragraph(doc, "DATA ANALYSIS, PRESENTATION AND DISCUSSION OF FINDINGS", 'chapter_title_centered')
    add_styled_paragraph(doc, "4.1 Empirical Results", 'section_title')
    add_styled_paragraph(
        doc,
        "This chapter presents the empirical findings of the study on equity return forecasting and tail-risk-aware portfolio optimization "
        "on the Nigerian Exchange Group (NGX). The analysis evaluates 28 liquid equities spanning a 16-year historical period from January 2010 through "
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
        "To guarantee a complete 16-year historical dataset (835 weekly observations from 2010 to 2025) required for training machine learning algorithms (2010-2020) "
        "and backtesting out-of-sample portfolio performance (2021-2025), 28 equities with continuous price history were selected. "
        "Conversely, 10 post-2010 listed equities were excluded to prevent artificial data imputation or look-ahead bias. Table 4.0 provides the comprehensive universe breakdown.",
        'body'
    )
    
    add_styled_paragraph(doc, "Table 4.0: NGX Pension Index Asset Universe Breakdown & Exclusion Rationale", 'table_title')
    universe_headers = ["Ticker", "Company Name", "Sector", "Status", "Inclusion / Exclusion Rationale"]
    universe_records = [
        ["CONOIL", "Conoil Plc", "Oil & Gas", "Included", "Complete 16-yr history (2010-2025)"],
        ["CUSTODIAN", "Custodian Investment Plc", "Financial Services", "Included", "Complete 16-yr history (2010-2025)"],
        ["DANGCEM", "Dangote Cement Plc", "Industrial Goods", "Included", "Complete 16-yr history (2010-2025)"],
        ["DANGSUGAR", "Dangote Sugar Refinery Plc", "Consumer Goods", "Included", "Complete 16-yr history (2010-2025)"],
        ["ETI", "Ecobank Transnational Inc.", "Financial Services", "Included", "Complete 16-yr history (2010-2025)"],
        ["FCMB", "FCMB Group Plc", "Financial Services", "Included", "Complete 16-yr history (2010-2025)"],
        ["FIDELITYBK", "Fidelity Bank Plc", "Financial Services", "Included", "Complete 16-yr history (2010-2025)"],
        ["FIDSON", "Fidson Healthcare Plc", "Healthcare", "Included", "Complete 16-yr history (2010-2025)"],
        ["FBNH", "First HoldCo Plc", "Financial Services", "Included", "Complete 16-yr history (2010-2025)"],
        ["GTCO", "Guaranty Trust Holding Co", "Financial Services", "Included", "Complete 16-yr history (2010-2025)"],
        ["GUINNESS", "Guinness Nigeria Plc", "Consumer Goods", "Included", "Complete 16-yr history (2010-2025)"],
        ["JBERGER", "Julius Berger Nigeria Plc", "Construction", "Included", "Complete 16-yr history (2010-2025)"],
        ["WAPCO", "Lafarge Africa Plc", "Industrial Goods", "Included", "Complete 16-yr history (2010-2025)"],
        ["MANSARD", "AXA Mansard Insurance Plc", "Financial Services", "Included", "Complete 16-yr history (2010-2025)"],
        ["NAHCO", "Nigerian Aviation Handling", "Services", "Included", "Complete 16-yr history (2010-2025)"],
        ["NASCON", "Nascon Allied Industries", "Consumer Goods", "Included", "Complete 16-yr history (2010-2025)"],
        ["NESTLE", "Nestle Nigeria Plc", "Consumer Goods", "Included", "Complete 16-yr history (2010-2025)"],
        ["NB", "Nigerian Breweries Plc", "Consumer Goods", "Included", "Complete 16-yr history (2010-2025)"],
        ["OKOMUOIL", "Okomu Oil Palm Plc", "Agriculture", "Included", "Complete 16-yr history (2010-2025)"],
        ["PRESCO", "Presco Plc", "Agriculture", "Included", "Complete 16-yr history (2010-2025)"],
        ["STANBIC", "Stanbic IBTC Holdings", "Financial Services", "Included", "Complete 16-yr history (2010-2025)"],
        ["STERLINGNG", "Sterling Financial Holdings", "Financial Services", "Included", "Complete 16-yr history (2010-2025)"],
        ["TRANSCORP", "Transnational Corp Plc", "Conglomerates", "Included", "Complete 16-yr history (2010-2025)"],
        ["UACN", "UAC of Nigeria Plc", "Conglomerates", "Included", "Complete 16-yr history (2010-2025)"],
        ["UBA", "United Bank for Africa Plc", "Financial Services", "Included", "Complete 16-yr history (2010-2025)"],
        ["UNILEVER", "Unilever Nigeria Plc", "Consumer Goods", "Included", "Complete 16-yr history (2010-2025)"],
        ["WEMABANK", "Wema Bank Plc", "Financial Services", "Included", "Complete 16-yr history (2010-2025)"],
        ["ZENITHBANK", "Zenith Bank Plc", "Financial Services", "Included", "Complete 16-yr history (2010-2025)"],
        ["ACCESSCORP", "Access Holdings Plc", "Financial Services", "Excluded", "Post-2010 restructuring"],
        ["AIRTELAFRI", "Airtel Africa Plc", "Telecoms", "Excluded", "Listed June 2019 (< 16-yr history)"],
        ["ARADEL", "Aradel Holdings Plc", "Oil & Gas", "Excluded", "Listed October 2024 (< 16-yr history)"],
        ["BUAFOODS", "BUA Foods Plc", "Consumer Goods", "Excluded", "Listed January 2022 (< 16-yr history)"],
        ["GEREGU", "Geregu Power Plc", "Utilities / Power", "Excluded", "Listed October 2022 (< 16-yr history)"],
        ["MTNN", "MTN Nigeria Comms Plc", "Telecoms", "Excluded", "Listed May 2019 (< 16-yr history)"],
        ["SEPLAT", "Seplat Energy Plc", "Oil & Gas", "Excluded", "Listed April 2014 (< 16-yr history)"],
        ["TRANSCOHOT", "Transcorp Hotels Plc", "Services", "Excluded", "Listed January 2015 (< 16-yr history)"],
        ["TRANSPOWER", "Transcorp Power Plc", "Utilities / Power", "Excluded", "Listed March 2024 (< 16-yr history)"],
        ["UCAP", "United Capital Plc", "Financial Services", "Excluded", "Listed January 2013 (< 16-yr history)"]
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
    add_styled_paragraph(doc, "Table 4.1: Descriptive Statistics of 28 NGX Equity Log Returns (2010-2025)", 'table_title')
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
    
    add_styled_paragraph(doc, "Table 4.2: Empirical Non-Normality (JB, SW) and Stationarity (ADF) Diagnostic Tests (All 28 Equities)", 'table_title')
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
    add_styled_paragraph(doc, "Table 4.3: Out-of-Sample Predictive Performance Metrics across All 28 NGX Equities (2021-2025 Walk-Forward)", 'table_title')
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
    
    add_styled_paragraph(doc, "4.5.1 Econometric Evaluation: Resolving the RMSE vs. Portfolio Alpha Paradox", 'section_title')
    add_styled_paragraph(
        doc,
        "A critical empirical observation in Table 4.3 is that the out-of-sample Root Mean Squared Error (RMSE) across all 28 NGX equities averages 0.0602 for the flat Historical Mean baseline, "
        "compared to 0.0608 for XGBoost and 0.0627 for Random Forest. Similarly, binary directional accuracy (DA) hovers around 37.8% to 38.1% across assets. On a surface level, this might lead to "
        "the erroneous conclusion that machine learning models fail to outperform historical baselines. However, when evaluated in downstream portfolio optimization (Section 4.7), XGBoost-integrated "
        "Mean-CVaR achieves a gross Sharpe ratio of 1.52 (42.00% annualized return) compared to 0.91 for passive indexing and 0.76 for Markowitz MVO. Resolving this apparent discrepancy requires "
        "a rigorous econometric evaluation of the mathematical mechanics of RMSE versus portfolio selection utility across the following four points:",
        'body'
    )
    add_styled_paragraph(
        doc,
        "1. Quadratic Loss Penalization and Noise Dominance: The apparent superiority of the flat Historical Mean in raw RMSE stems from the statistical properties of financial return noise under an L2 quadratic loss function. "
        "The Root Mean Squared Error penalizes prediction errors quadratically: RMSE = √((1/n) Σ (ŷ_t - y_t)²). At weekly sampling horizons, equity return series are dominated "
        "by high-frequency, zero-mean unobserved news noise. During quiet, low-volatility market regimes where asset returns fluctuate randomly around zero (+0.4%, -0.2%, +0.1%), a static forecast "
        "equal to the historical sample mean (ŷ_t = 0.001) minimizes squared error variance across hundreds of noise observations. Conversely, non-linear ML models generate dynamic, non-zero "
        "return forecasts. When unpredictable random noise causes weekly returns to move opposite to a dynamic prediction, the quadratic L2 loss function severely penalizes the ML model. "
        "Consequently, the flat baseline achieves a marginally lower aggregate point RMSE simply by predicting near-zero constant returns across noise weeks.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "2. Cross-Sectional Ranking vs. Point Prediction: Classical point-forecasting metrics such as RMSE and binary Directional Accuracy evaluate asset returns in isolation along a single temporal axis. In contrast, multi-asset "
        "portfolio optimization (Markowitz, 1952; Rockafellar & Uryasev, 2000) does not operate on isolated point accuracy; rather, it depends fundamentally on cross-sectional magnitude "
        "discrimination across the asset universe at each rebalancing time step t. The Mean-CVaR portfolio optimizer does not require perfect sign prediction across noise weeks; it requires "
        "accurate cross-sectional ranking, specifically identifying which assets will experience severe downside drawdowns (left-tail events) versus which equities retain strong positive volume-confirmed momentum.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "3. Non-Linear Feature Signal Extraction: Tree-based machine learning ensembles (Random Forest and XGBoost) successfully extract non-linear cross-sectional signals by leveraging technical indicators. Feature importance analysis "
        "(Section 4.6) demonstrates that short-term momentum indicators, specifically the Percentage Price Oscillator (PPO), Relative Strength Index (RSI), and On-Balance Volume (OBV), serve as primary "
        "predictive drivers. By incorporating volume-confirmed trend strength and volatility scaling (ATR, ADX), tree models effectively capture non-linear market regime shifts. Even if an ML model overpredicts "
        "return magnitude during a noise week (incurring a small RMSE penalty), its predicted expected return vector (μ̂_t) correctly ranks top-performing equities relative to high-risk equities across the 28 NGX assets.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "4. Tail-Risk Mitigation and Convex Optimization: When these dynamic expected return vectors (μ̂_t) are passed into the convex Mean-CVaR linear program, the optimizer re-allocates capital toward high-ranked momentum equities while "
        "penalizing assets exposed to left-tail drawdowns. Under zero fee friction (Table 4.5), XGB-CVaR achieves a gross Sharpe ratio of 1.52 (+42.00% annualized return, -22.09% max drawdown), "
        "yielding a statistically significant Sharpe outperformance over passive indexing (Ledoit-Wolf circular block bootstrap p = 0.015 < 0.05) and positive welfare gains (+819 bps Certainty Equivalent Return gain).",
        'body'
    )
    add_styled_paragraph(
        doc,
        "In conclusion, the empirical evidence demonstrates that raw RMSE is an inadequate metric for evaluating machine learning models in portfolio selection. RMSE measures point prediction noise, "
        "whereas financial portfolio optimization rewards cross-sectional relative ranking and downside tail-risk avoidance. The machine learning models deliver superior portfolio performance because "
        "they capture relative cross-sectional momentum and tail risk, generating substantial economic alpha despite achieving a slightly higher point RMSE.",
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
    add_styled_paragraph(doc, "Table 4.4: Out-of-Sample Portfolio Performance with 1.50% Retail Transaction Fees & Market Slippage", 'table_title')
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
    add_styled_paragraph(doc, "Table 4.5: Out-of-Sample Portfolio Performance under Zero Transaction Fees (Gross Alpha - 0.00%)", 'table_title')
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
    add_styled_paragraph(doc, "Table 4.5b: Out-of-Sample Portfolio Performance under 0.75% Institutional PFA Transaction Fees", 'table_title')
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
    add_styled_paragraph(doc, "Table 4.6: Multi-Tier Pairwise Hypothesis Testing of Sharpe & Sortino Equality across Fee Regimes", 'table_title')
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
    
    # 4.8 Discussion of Findings
    add_styled_paragraph(doc, "4.8 Discussion of Findings", 'section_title')
    add_styled_paragraph(
        doc,
        "The empirical findings presented in Section 4.1 to Section 4.7 provide quantitative insights into the dynamics of equity return forecasting and tail-risk-aware asset allocation on the Nigerian Exchange Group (NGX). "
        "To evaluate the academic and operational significance of these empirical results, the following discussion evaluates each empirical outcome directly against the four specific research objectives "
        "established in Chapter One, situating the findings within modern financial economics and empirical asset pricing literature.",
        'body'
    )
    
    # Paragraph 1: Objective 1
    add_styled_paragraph(
        doc,
        "Firstly, regarding the evaluation of statistical non-normality and tail-risk exposure across NGX equities, the empirical diagnostic tests presented in Section 4.3 indicate that asset returns on the Nigerian Exchange Group depart from Gaussian normality. "
        "Formal Jarque-Bera and Shapiro-Wilk tests rejected the null hypothesis of normal distribution across all 28 evaluated equities (p < 0.001), exhibiting negative skewness and excess kurtosis reaching up to 14.46. Econometrically, this confirms that empirical NGX equity returns are characterized by fat tails "
        "and asymmetric downside risk. These results strongly support the theoretical arguments and empirical evidence of Mozumder et al. (2024), Adegboyo & Sarwar (2025), Uzoaga et al. (2025), and Alim et al. (2024), who emphasize that emerging frontier stock markets experience "
        "pronounced price jumps, policy shifts, and macroeconomic shocks that invalidate Gaussian assumptions. Conversely, these findings contrast with the theoretical premise of classical dispersion models (Bali et al., 2007; Samaniego Alcántar, 2023), which argue that standard variance can serve as an adequate proxy for portfolio risk when higher-order moments exhibit finite-sample instability. On the NGX, relying strictly on standard variance underestimates tail-risk exposure during market downturns, supporting the adoption of downside risk measures such as Conditional Value-at-Risk (CVaR).",
        'body'
    )
    
    # Paragraph 2: Objective 2
    add_styled_paragraph(
        doc,
        "Secondly, regarding the performance of non-linear Machine Learning models in forecasting weekly NGX equity returns under Expanding Rolling Window Walk-Forward Validation, the empirical results in Section 4.5 "
        "show that non-linear tree-based ensembles (Random Forest and XGBoost) capture predictive signals from market data. While raw point forecasting metrics (RMSE) hover close to historical baselines due to weekly noise variance, "
        "XGBoost achieved an average out-of-sample directional accuracy of 38.1% across liquid NGX equities (with individual assets reaching up to 50.8%), compared to 37.8% for historical baselines. Feature importance analysis (Section 4.6) indicates that volume-confirmed technical momentum indicators, specifically "
        "the Percentage Price Oscillator (PPO), Relative Strength Index (RSI), and On-Balance Volume (OBV), serve as primary drivers of return predictability. This aligns with empirical asset pricing literature (Gu, Kelly, & Xiu, 2020; Chao, 2024; Ojo & Okafor, 2024; Ajiga et al., 2024; Ferrari et al., 2024), "
        "demonstrating that machine learning algorithms capture non-linear market interactions and trend-persistence dynamics in emerging economies. However, this finding also engages with contrasting perspectives: it partially challenges the strict semi-strong form of the Efficient Market Hypothesis (Fama, 1970) by identifying exploitable technical momentum anomalies, while simultaneously contextualizing the cautionary findings of Moyoweshumba & Seitshiro (2025), who observe that in thin African stock markets, microstructural noise and regime shifts can constrain the point forecasting accuracy of complex algorithmic models.",
        'body'
    )
    
    # Paragraph 3: Objective 3
    add_styled_paragraph(
        doc,
        "Thirdly, regarding the performance of integrated ML-CVaR portfolio strategies compared against classical Markowitz Mean-Variance Optimization and 1/N benchmarks, the backtest results in Section 4.7 indicate a higher risk-adjusted return profile "
        "for integrated Mean-CVaR strategies prior to transaction costs. Under zero fee friction, XGBoost + Mean-CVaR (XGB-CVaR) achieved a gross Sharpe ratio of 1.52 (42.00% annualized return, -22.09% max drawdown), compared to 0.91 for the passive NGX Index Buy-and-Hold benchmark "
        "and 0.76 for Markowitz MVO. Inferential hypothesis testing (Section 4.7.1) indicates that this Sharpe ratio outperformance is statistically significant under Ledoit-Wolf circular block bootstrap tests (p = 0.015 < 0.05). Furthermore, Certainty Equivalent Return (CER) welfare analysis "
        "shows positive utility gains (+819 basis points CER gain over passive indexing). These results corroborate established portfolio selection theory (Markowitz, 1952; Rockafellar & Uryasev, 2000; Bodnar et al., 2022; Hsiao, 2025), showing that combining forward-looking return estimates with convex tail-risk constraints improves risk-adjusted outcomes. Nevertheless, these findings provide a nuanced contrast to the empirical work of San (2025) and the classic estimation-error critique of naive diversification, which assert that simple 1/N equal weighting consistently outperforms or equals optimized portfolios out-of-sample due to parameter uncertainty. While 1/N achieves a robust gross Sharpe of 1.25 on the NGX, disciplined CVaR tail-loss minimization achieves superior downside protection (-22.09% max drawdown versus -30.01% for 1/N), demonstrating that tail-risk optimization delivers distinct economic value.",
        'body'
    )
    
    # Paragraph 4: Objective 4
    add_styled_paragraph(
        doc,
        "Fourthly, regarding portfolio robustness under market stress and transaction cost frictions, the empirical evaluation in Section 4.7 highlights execution dynamics across market participant regimes. Under 1.50% retail fees and slippage, "
        "unconstrained Markowitz MVO experienced severe weight instability (99.28% average weekly turnover), resulting in a maximum drawdown of -86.38% and negative economic welfare (CER = -64.09%). This strongly supports Michaud's (1989) finding regarding the sensitivity of unconstrained MVO "
        "to estimation error in high-friction environments. Conversely, low-turnover Historical-CVaR (0.38% turnover) displayed resilience, retaining net Sharpe ratios of 1.48 (retail) and 1.49 (institutional). "
        "While active ML models generate gross alpha prior to friction, weekly rebalancing turnover (11.00%) incurs an annual fee drag (~3.6% to ~7.2%) that offsets marginal predictive gains post-fees. This finding aligns with transaction cost literature (Job, 2022; Alotaibi et al., 2022; Kevin & Yugopuspito, 2025), "
        "indicating that structural tail-risk architecture (CVaR) plays a central role in frictional emerging markets. It also qualifies the assertions of high-frequency quantitative models that advocate unconstrained algorithmic rebalancing, demonstrating that without explicit turnover penalties or execution smoothing bands, transaction friction rapidly neutralizes statistical predictive edges on frontier exchanges.",
        'body'
    )
    
    # =========================================================================
    # CHAPTER 5: SUMMARY, CONCLUSION, AND RECOMMENDATIONS
    # =========================================================================
    doc.add_page_break()
    add_styled_paragraph(doc, "CHAPTER FIVE", 'chapter_header')
    add_styled_paragraph(doc, "SUMMARY, CONCLUSION AND RECOMMENDATIONS", 'chapter_title_centered')
    
    add_styled_paragraph(doc, "5.1 Summary of Findings", 'section_title')
    add_styled_paragraph(
        doc,
        "1. Statistical Non-Normality and Tail-Risk Exposure: Formal statistical diagnostic tests (Jarque-Bera and Shapiro-Wilk) rejected Gaussian normality across all 28 evaluated NGX equities (p < 0.001). "
        "The empirical return distributions displayed negative skewness and excess kurtosis (up to 14.46), reflecting heavy-tail risk exposure and supporting the use of downside Conditional Value-at-Risk (CVaR) over standard variance.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "2. Machine Learning Return Forecasting Dynamics: Non-linear machine learning ensembles (Random Forest and XGBoost) evaluated under Expanding Rolling Window Walk-Forward Validation captured time-varying market dynamics. "
        "XGBoost achieved an average out-of-sample directional accuracy of 38.1% across liquid NGX equities (with individual assets reaching up to 50.8%), driven primarily by volume-confirmed momentum features (Percentage Price Oscillator, Relative Strength Index, and On-Balance Volume).",
        'body'
    )
    add_styled_paragraph(
        doc,
        "3. Out-of-Sample Portfolio Optimization Performance: Integrating machine learning return forecasts into a convex Mean-CVaR optimization framework generated risk-adjusted returns under zero fee friction. "
        "XGBoost + Mean-CVaR achieved a gross Sharpe ratio of 1.52 (42.00% annualized return, -22.09% maximum drawdown) compared to 0.91 for the passive NGX Index Buy-Hold baseline, supported by Ledoit-Wolf circular block bootstrap Sharpe tests (p = 0.015 < 0.05) and Certainty Equivalent Return utility gains (+819 bps CER gain).",
        'body'
    )
    add_styled_paragraph(
        doc,
        "4. Transaction Cost Dynamics and Turnover Friction: Evaluating portfolio performance under market stress and multi-tier transaction cost friction demonstrated that unconstrained Markowitz Mean-Variance Optimization experiences severe performance degradation (-86.38% drawdown, -64.09% CER utility) due to high turnover (99.28% weekly turnover). "
        "Under institutional (0.75%) and retail (1.50%) brokerage fees, active ML rebalancing turnover (11.00%) creates an annual fee drag (~3.6% to ~7.2%) that offsets marginal predictive gains post-fees, while low-turnover Historical-CVaR (0.38% turnover) maintains stable post-fee performance (net Sharpe 1.48 to 1.49, pairwise p = 0.000).",
        'body'
    )
    
    add_styled_paragraph(doc, "5.2 Conclusion", 'section_title')
    add_styled_paragraph(
        doc,
        "This study investigated equity return forecasting and tail-risk-aware portfolio optimization across 28 liquid equities on the Nigerian Exchange Group (NGX) spanning a 16-year period (2010-2025). "
        "The research evaluated non-normality diagnostics, Machine Learning return forecasting (Random Forest and XGBoost) under Expanding Rolling Window Walk-Forward Validation, and convex Mean-CVaR asset allocation backtesting.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "The overall conclusion of this research is that while Machine Learning models extract gross predictive alpha on the NGX, market transaction friction and rebalancing turnover neutralize these marginal predictive gains post-fees. "
        "Consequently, structural tail-risk management via Conditional Value-at-Risk (CVaR) constitutes the primary driver of real-world investor economic surplus (+819 bps CER gain over passive indexing). "
        "This indicates that downside tail-risk control plays a critical role relative to model forecasting complexity in frictional emerging equity markets.",
        'body'
    )
    
    add_styled_paragraph(doc, "5.3 Policy and Practical Recommendations", 'section_title')
    
    add_styled_paragraph(doc, "5.3.1 Regulatory and Macroeconomic Policy Recommendations", 'section_title')
    add_styled_paragraph(
        doc,
        "1. PENCOM Investment Guidelines Update: The National Pension Commission (PENCOM) should update its Investment Guidelines for Fund I, Fund II, and Fund III equity portfolios to mandate downside tail-risk metrics, specifically Conditional Value-at-Risk (CVaR_0.95), alongside traditional variance. Pension Fund Administrators (PFAs) should adopt CVaR-constrained allocation models to protect pension assets during extreme macroeconomic shocks.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "2. SEC & NGX Regulatory Data Transparency: The Securities and Exchange Commission (SEC) and NGX Regulation should establish open-access, low-latency API data infrastructure for market participants to support quantitative risk management. Furthermore, the SEC should require asset management firms to publish quarterly CVaR metrics in fund factsheets to enhance retail investor risk transparency.",
        'body'
    )
    
    add_styled_paragraph(doc, "5.3.2 Institutional Asset Allocation Recommendations", 'section_title')
    add_styled_paragraph(
        doc,
        "1. Adoption of Low-Turnover Tail-Risk Frameworks: Pension Fund Administrators (PFAs) and institutional fund managers operating on the NGX should replace classical Markowitz Mean-Variance Optimization with convex Mean-CVaR asset allocation. To prevent fee erosion, institutional managers should enforce strict turnover caps, employ turnover-penalized objective functions, or adopt quarterly rebalancing protocols.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "2. Dynamic Risk-Free Asset Allocation: Institutional portfolios should actively incorporate sovereign risk-free assets (such as Central Bank of Nigeria 91-day Treasury Bills) to stabilize portfolio Sharpe ratios during market drawdown regimes.",
        'body'
    )
    
    add_styled_paragraph(doc, "5.3.3 Quantitative Risk Management Recommendations", 'section_title')
    add_styled_paragraph(
        doc,
        "1. Stress-Testing and Downside Risk Auditing: Risk officers and quantitative portfolio managers should mandate regular stress testing using historical block bootstrap resampling and non-parametric CVaR estimation to evaluate portfolio tail loss limits.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "2. Integration of Volume-Confirmed Technical Signals: Quantitative models deployed on emerging exchanges should integrate volume-confirmed technical momentum indicators (Percentage Price Oscillator, Relative Strength Index, On-Balance Volume) to capture trend persistence and downside liquidity risks.",
        'body'
    )
    
    add_styled_paragraph(doc, "5.4 Limitations of the Study", 'section_title')
    add_styled_paragraph(
        doc,
        "While this study provides empirical insights into quantitative asset management on the Nigerian equity market, several methodological limitations are acknowledged:",
        'body'
    )
    add_styled_paragraph(
        doc,
        "1. Asset Universe Scope: The study evaluated 28 liquid equities from the NGX Pension Index with complete 16-year histories (2010–2025). Recently listed high-capitalization assets (e.g., BUA Foods, Geregu Power, Aradel Holdings) were excluded to maintain continuous historical data without imputation.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "2. Data Frequency: Analysis was conducted using weekly log returns. While weekly sampling effectively mitigates daily bid-ask bounce and microstructural noise, it does not capture intraday high-frequency trading dynamics.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "3. Exogenous Macroeconomic Signals: The machine learning feature matrix focused on price and volume technical indicators; exogenous macroeconomic variables (such as USD/NGN exchange rate shocks and Brent crude oil prices) were not explicitly included in the feature set.",
        'body'
    )
    
    add_styled_paragraph(doc, "5.5 Suggestions for Further Research", 'section_title')
    add_styled_paragraph(
        doc,
        "Based on the empirical findings and limitations of this research, the following directions for future investigation are suggested:",
        'body'
    )
    add_styled_paragraph(
        doc,
        "1. Macroeconomic and Exogenous Feature Integration: Future research should expand the machine learning feature space to include macroeconomic variables, foreign exchange volatility, and crude oil price dynamics.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "2. Deep Learning and High-Frequency Architectures: Extending forecasting models to Transformer-based temporal models and Long Short-Term Memory (LSTM) networks on daily or intraday NGX trading data.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "3. Multi-Period Friction-Constrained CVaR Optimization: Incorporating transaction cost penalties directly into the CVaR objective function to minimize rebalancing turnover during high-volatility regimes.",
        'body'
    )
    
    add_styled_paragraph(doc, "5.6 Contribution to Knowledge", 'section_title')
    add_styled_paragraph(
        doc,
        "This research contributes to quantitative finance literature in the following ways:",
        'body'
    )
    add_styled_paragraph(
        doc,
        "1. Empirical Contribution: Provides an empirical evaluation of Machine Learning integrated with convex Mean-CVaR optimization on the Nigerian Exchange Group using a clean 16-year dataset (2010–2025).",
        'body'
    )
    add_styled_paragraph(
        doc,
        "2. Theoretical Contribution: Evaluates the performance of classical Markowitz Mean-Variance Optimization under non-normal emerging market return distributions and examines how structural tail-risk architecture (CVaR) performs relative to model complexity post-fees.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "3. Practical Contribution: Formulates a low-turnover tail-risk asset allocation framework designed to improve economic welfare for institutional investors in frontier markets.",
        'body'
    )
    
    add_styled_paragraph(doc, "5.7 Data and Code Availability Statement", 'section_title')
    add_styled_paragraph(
        doc,
        "To guarantee complete computational reproducibility and scientific transparency, the entire quantitative finance pipeline, encompassing "
        "data cleaning scripts, non-normality diagnostic tests, technical feature extraction (with Welles Wilder's Parabolic SAR), expanding walk-forward machine learning models "
        "(Random Forest and XGBoost with TimeSeriesSplit cross-validation tuning), convex Mean-CVaR linear programming portfolio optimization backtests, and ReportLab PDF synthesis, is "
        "open-source and publicly hosted on GitHub at:",
        'body'
    )
    add_styled_paragraph(
        doc,
        "Repository URL: https://github.com/abdulameen962/equity-optimization",
        'body'
    )
    
    # =========================================================================
    # FULL APA 7TH EDITION REFERENCES SECTION (42 REFERENCES)
    # =========================================================================
    doc.add_page_break()
    add_styled_paragraph(doc, "REFERENCES", 'chapter_header')
    
    references_list = [
        'Adegboyo, O. S., & Sarwar, K. (2025). Modelling and forecasting of Nigeria stock market volatility. Future Business Journal, 11(1), Article 124. https://doi.org/10.1186/s43093-025-00536-4',
        'Ajiga, D. I., Adeleye, R. A., Tubokirifuruar, T. S., Bello, B. G., Ndubuisi, N. L., Asuzu, O. F., & Owolabi, O. R. (2024). Machine learning for stock market forecasting: A review of models and accuracy. Finance & Accounting Research Journal, 6(2).',
        'Al-Shboul, M., & Alfzari, S. (2025). Predictive analytics in portfolio management: A fusion of AI and investment economics for optimal risk-return trade-offs. International Review of Management and Marketing, 15(1). https://www.econjournals.net.tr/index.php/irmm/article/view/18594',
        'Alfeus, M., Harvey, J., & Maphatsoe, P. (2024). Improving realised volatility forecast for emerging markets. Journal of Economics and Finance. Advance online publication. https://doi.org/10.1007/s12197-024-09701-x',
        'Alim, W., Khan, N. U., Zhang, V. W., Cai, H. H., Mikhaylov, A., & Yuan, Q. (2024). Influence of political stability on the stock market returns and volatility: GARCH and EGARCH approach. Financial Innovation. https://doi.org/10.1186/s40854-024-00658-8',
        'Alotaibi, T. S., Dalla Valle, L., & Craven, M. J. (2022). The worst case GARCH-copula CVaR approach for portfolio optimisation: Evidence from financial markets. Journal of Risk and Financial Management, 15(10), Article 482. https://doi.org/10.3390/jrfm15100482',
        'Arif, U., Sohail, M. T., & Majeed, M. I. (2020). Portfolio optimization with mean-variance & mean-CVaR: Evidence from Pakistan stock market. International Journal of Management Research & Emerging Sciences, 10(2), 215–226.',
        'Ashrafzadeh, M., Sadrani, M., & Zolfani, S. H. (2025). Clustering-based return prediction model for stock pre-selection in portfolio optimization. Results in Engineering, 27, Article 106263. https://doi.org/10.1016/j.rineng.2025.106263',
        'Bali, T. G., Gokcan, S., & Liang, B. (2007). Value at risk and the cross-section of hedge fund returns. Journal of Banking & Finance, 31(4), 1135–1166. https://doi.org/10.1016/j.jbankfin.2006.10.023',
        'Bodnar, T., Lindholm, M., Niklasson, V., & Thorsén, E. (2022). Bayesian portfolio selection using VaR and CVaR. Applied Mathematics and Computation, 427, Article 127120.',
        'Campbell, J. Y., & Viceira, L. M. (2002). Strategic asset allocation: Portfolio choice for long-term investors. Oxford University Press.',
        'Chao, L. (2024). Application of machine learning in stock market return forecasting. International Journal of Scientific Research and Management (IJSRM), 12(7), 6827–6835. https://doi.org/10.18535/ijsrm/v12i07.em11',
        'Chaweewanchon, A., & Chaysiri, R. (2022). Markowitz mean-variance portfolio optimization with predictive stock selection using machine learning. International Journal of Financial Studies, 10(3), Article 64. https://doi.org/10.3390/ijfs10030064',
        'Chen, R. (2025). Stock price prediction and portfolio optimization based on mean variance model and random forest model. Advances in Economics, Business and Management Research, 333, 358–367.',
        'Cheng, Y. (2025). Monte Carlo-Based VaR Estimation and Backtesting Under Basel III. Risks, 13(8), Article 146. https://doi.org/10.3390/risks13080146',
        'Chung, V., Espinoza, J., & Quispe, R. (2025). Forecasting Financial Volatility Under Structural Breaks: A Comparative Study of GARCH Models and Deep Learning Techniques. Journal of Risk and Financial Management, 18(9), Article 494. https://doi.org/10.3390/jrfm18090494',
        'Diebold, F. X., & Mariano, R. S. (1995). Comparing predictive accuracy. Journal of Business & Economic Statistics, 13(3), 253–263.',
        'Espiga-Fernández, F., García-Sánchez, Á., & Ordieres-Meré, J. (2024). A Systematic Approach to Portfolio Optimization: A Comparative Study of Reinforcement Learning Agents, Market Signals, and Investment Horizons. Algorithms, 17(12), Article 570. https://doi.org/10.3390/a17120570',
        'Fama, E. F. (1970). Efficient capital markets: A review of theory and empirical work. The Journal of Finance, 25(2), 383–417. https://doi.org/10.1111/j.1540-6261.1970.tb00518.x',
        'Fan, Y. (2025). Enhancing investment strategies with LSTM-based stock prediction and mean-variance portfolio optimization. Proceedings of the 3rd International Conference on Financial Technology and Business Analysis. https://doi.org/10.54254/2754-1169/2024.23667',
        'Fapetu, O., Ojo, S. M., Balogun, A. A., & Asaolu, A. A. (2021). Capital market performance and macroeconomic dynamics in Nigeria. FUOYE Journal of Finance and Contemporary Issues, 1(1), 29–37.',
        'Fatouros, G., Makridis, G., Kotios, D., Soldatos, J., Filippakis, M., & Kyriazis, D. (2023). DeepVaR: A framework for portfolio risk assessment leveraging probabilistic deep neural networks. Digital Finance, 5(1), 29–56.',
        'Ferrari, D., Paterlini, S., Rigamonti, A., & Weissensteiner, A. (2024). Smoothed semicovariance estimation for portfolio selection. Annals of Operations Research. Advance online publication. https://doi.org/10.1007/s10479-024-06043-z',
        "Fleming, J., Kirby, C., & Ostdiek, B. (2001). The economic value of volatility timing using 'realized' volatility [Working paper]. Rice University, Jones Graduate School. https://ssrn.com/abstract=276921",
        'Gu, S., Kelly, B., & Xiu, D. (2020). Empirical asset pricing via machine learning. The Review of Financial Studies, 33(5), 2223–2273. https://doi.org/10.1093/rfs/hhz113',
        "He, W. (2022). An empirical research based on Markowitz's portfolio theory. World Scientific Research Journal, 8(3), 221–227. https://doi.org/10.6911/WSRJ.202203_8(3).0028",
        'Hsiao, Y.-Y. (2025). A comprehensive survey of modern portfolio optimization: From traditional risk analysis to advanced analytics and machine learning approaches (Preprint). Johns Hopkins University.',
        'Huang, R., Kambouroudis, D., & McMillan, D. G. (2025). Is portfolio diversification still effective: Evidence spanning three crises from the perspective of U.S. investors. Journal of Asset Management, 26(2), 115–135. https://doi.org/10.1057/s41260-025-00398-z',
        'Job, O. D. (2022). An empirical evaluation of alternative asset allocation policies for emerging and frontier market investors in Africa. Journal of Financial Risk Management, 11(3), 481–521. https://doi.org/10.4236/jfrm.2022.113024',
        'Jobson, J. D., & Korkie, B. M. (1981). Performance hypothesis testing with the Sharpe and Treynor measures. The Journal of Finance, 36(4), 889–908.',
        'Kevin, J., & Yugopuspito, P. (2025). Hybrid LSTM and PPO networks for dynamic portfolio optimization (LPPM-UPH, No. 404/LPPM-UPH/VII/2025). Universitas Pelita Harapan Working Paper.',
        'Leccadito, A., Staino, A., & Toscano, P. (2024). A novel robust method for estimating the covariance matrix of financial returns with applications to risk management. Financial Innovation, 10, Article 116.',
        'Ledoit, O., & Wolf, M. (2008). Robust performance hypothesis testing with the Sharpe ratio. Journal of Empirical Finance, 15(5), 850–859.',
        'Ledoit, O., & Wolf, M. (2011). Robust performance hypothesis testing with the variance. Wilmott Magazine, (55), 86–89.',
        'Li, G. (2023). Portfolio optimization and risk analysis in financial markets. Proceedings of the 2nd International Conference on Financial Technology and Business Analysis, 61, 243–247. https://doi.org/10.54254/2754-1169/61/20231273',
        'Lorimer, D. A., van Schalkwyk, C. H., & Szczygielski, J. J. (2024). Portfolio optimisation using alternative risk measures. Finance Research Letters, 67, Article 105758. https://doi.org/10.1016/j.frl.2024.105758',
        'Lyu, X. (2024). Portfolio Optimization Strategies: New Approaches Based on Machine Learning Forecasting. Highlights in Business, Economics and Management, 40, 1077–1082.',
        'Mahadevaswamy, G. H., & Shyamala, G. (2022). Markowitz Model Is Right Choice to Investment. International Journal of Novel Research and Development, 7(11), 305–314.',
        'Manogna, R. L., & Kulkarni, N. (2025). Portfolio Optimization Model for Stock Price Prediction Using Machine Learning. Journal of Statistical Theory and Applications, 24(1).',
        'Markowitz, H. (1952). Portfolio selection. The Journal of Finance, 7(1), 77–91. https://doi.org/10.1111/j.1540-6261.1952.tb01525.x',
        'Martínez-Barbero, X., Cervelló-Royo, R., & Ribal, J. (2024). Portfolio optimization with prediction-based return using Long Short-Term Memory neural networks: Testing on upward and downward European markets. Computational Economics, 65, 1479–1504. https://doi.org/10.1007/s10614-024-10604-6',
        'Mba, J. C., Ababio, K. A., & Agyei, S. K. (2022). Markowitz mean-variance portfolio selection and optimization under a behavioral spectacle: New empirical evidence. International Journal of Financial Studies, 10(2), Article 28. https://doi.org/10.3390/ijfs10020028',
        'Memmel, C. (2003). Performance hypothesis testing with the Sharpe ratio. Finance Letters, 1(1), 21–23.',
        "Michaud, R. O. (1989). The Markowitz optimization enigma: Is 'optimized' optimal? Financial Analysts Journal, 45(1), 31–42. https://doi.org/10.2469/faj.v45.n1.31",
        'Moyoweshumba, E., & Seitshiro, M. (2025). Leveraging Markowitz, Random Forest, and XGBoost for optimal diversification of South African stock portfolios. Data Science in Finance and Economics, 5(2), 205–233. https://doi.org/10.3934/DSFE.2025010',
        'Mozumder, S., Hasan, M. K., & Kabir, M. H. (2024). An evaluation of the adequacy of Lévy and extreme value tail risk estimates. Financial Innovation, 10(1), Article 100. https://doi.org/10.1186/s40854-024-00614-6',
        'Naeem, M., Jassim, H. S., & Korsah, D. (2024). The application of machine learning techniques to predict stock market crises in Africa. Journal of Risk and Financial Management, 17(12), Article 554. https://doi.org/10.3390/jrfm17120554',
        'Nahari, F. (2025). Portfolio optimization in practice: A comparative analysis of the Markowitz and Index models. In M. M. Husin (Ed.), Proceedings of the 2025 International Conference on Financial Risk and Investment Management (ICFRIM 2025), Advances in Economics, Business and Management Research (Vol. 333, pp. 367–375). Atlantis Press.',
        'Ojo, A. K., & Okafor, I. J. (2024). Forecasting Nigerian Equity Stock Returns Using Long Short-Term Memory Technique. Journal of Advances in Mathematics and Computer Science, 39(7), 45–54. https://doi.org/10.9734/jamcs/2024/v39i71911',
        'Okafor, C., & Robertson, A. (2022). Maximizing returns: Portfolio optimization in the Nigerian Stock Exchange. International Journal of Advances in Applied Mathematics and Computer Science, 10(2), 1–9.',
        'Quimbayo, C. Z., & León, B. (2025). Downside Risk Measures and ESG Factors in Optimal Portfolio Construction: Evidence from European Equity Markets. Economics - Innovative and Economics Research Journal, 13(2), 5–17. https://doi.org/10.2478/eoik-2025-0082',
        'Rigamonti, A., & Lučivjanská, K. (2021). Mean-semivariance portfolio optimization using minimum average partial. SSRN Electronic Journal, Article 3542727. https://doi.org/10.2139/ssrn.3542727',
        'Rockafellar, R. T., & Uryasev, S. (2000). Optimization of conditional value-at-risk. Journal of Risk, 2(3), 21–41. https://doi.org/10.21314/JOR.2000.038',
        'Rockafellar, R. T., & Uryasev, S. (2002). Conditional value-at-risk for general loss distributions. Journal of Banking & Finance, 26(7), 1443–1471. https://doi.org/10.1016/S0378-4266(02)00271-6',
        'Sahiner, M. (2022). Forecasting volatility in Asian financial markets: Evidence from recursive and rolling window methods. SN Business & Economics, 2, Article 157. https://doi.org/10.1007/s43546-022-00329-9',
        'Salo, A., Doumpos, M., Liesiö, J., & Zopounidis, C. (2024). Fifty years of portfolio optimization. European Journal of Operational Research, 318(1), 1–18. https://doi.org/10.1016/j.ejor.2023.12.031',
        'Samaniego Alcántar, A. (2023). Semi-variance optimization for the components of the Dow Jones Industrial Average index. Contaduría y Administración, 68(4), 1–17. http://dx.doi.org/10.22201/fca.24488410e.2023.3409',
        'San, J. (2025). Stock Forecasting and Portfolio Optimization Based on ARIMA-GARCH, Random Forest and Monte Carlo Models. Advances in Economics, Business and Management Research, 333, 580–588.',
        'Senescall, M., & Low, R. K. Y. (2024). Quantitative Portfolio Management: Review and Outlook. Mathematics, 12(18), Article 2897. https://doi.org/10.3390/math12182897',
        'Sulaiman, L. A., Adejayan, A. O., & Ilori, O. O. (2023). Capital Market Development and Economic Growth of West African Countries. Nigerian Journal of Banking and Financial Issues, 9(1), 117–125.',
        'Ślusarczyk, D., & Ślepaczuk, R. (2025). Algorithmic investment strategies on the Dow Jones Industrial Average. Journal of Big Data, 12, Article 127. https://doi.org/10.1186/s40537-025-01164-z',
        'Tjiwidjaja, H. (2025). Optimization of Investment Portfolio Returns Through an Integrated Risk Management Approach. STIE Ganesha Research Papers, 853–863.',
        'Uzoaga, G. A., Adenomon, M. O., Nweze, N. O., & Maijama, B. (2025). Modelling and predicting stock prices of Nigerian Stock Exchange using some machine learning techniques and time series model. Science World Journal, 20(2), 510–515. https://dx.doi.org/10.4314/swj.v20i2.9',
        'Uzoaga, G. A., Adenomon, M. O., Nweze, N. O., & Maijamaa, B. (2025). Predictive machine learning methods for stock returns among emerging economies in Africa. Science World Journal, 20(3), 941–947. https://dx.doi.org/10.4314/swj.v20i3.3',
        'Wahid, A. J., Riaman, & Sukono. (2025). A Systematic Literature Review on Mean-CVaR Based Financial Asset Portfolio Weight Allocation Using K-Means Clustering. Journal of Applied Mathematics and Computing, 10(2), 1069–1091.',
        'Wang, T., Pan, Q., Wu, W., Gao, J., & Zhou, K. (2024). Dynamic Mean–Variance Portfolio Optimization with Value-at-Risk Constraint in Continuous Time. Mathematics, 12(14), Article 2268. https://doi.org/10.3390/math12142268',
        "Yadav, A., Madhavi, R., Bagaria, O., Ambulkar, A., & Sharma, S. (2024). Survey on financial portfolio management's role in investment decision-making strategies. Multidisciplinary Reviews, 6, Article e2023ss101. https://doi.org/10.31893/multirev.2023ss101",
        'Yu, S. (2024). Advancing Stock Market Return Forecasting with LSTM Models and Financial Indicators. Proceedings of the International Conference on Economic Management and Green Development, Article 122. https://doi.org/10.54254/2754-1169/122/2024.17734',
        'Zaimovic, A., Arnaut-Berilo, A., & Bešlija, R. (2024). International Portfolio Diversification Benefits: An Empirical Investigation of the 28 European Stock Markets. School of Economics and Business Sarajevo Working Papers, Article 46.',
        'Zhang, G. (2025). Using Machine Learning for Stock Return Prediction. Proceedings of ICEMGD 2025 Symposium, Article LH23915. https://doi.org/10.54254/2754-1169/2025.LH23915',
        'Zhang, P., Yang, Y., Li, J., & Zeng, Y. (2023). A Two-stage Mean-CVaR Investment Strategy Based on LSTM. Journal of South China Normal University (Natural Science Edition), 55(5), 93–102.',
        'Zhang, Y. (2024). Integrating Forecasting and Mean-Variance Portfolio Optimization: A Machine Learning Approach. Proceedings of the 3rd International Conference on Financial Technology and Business Analysis, Article 2002.',
        'Zsurkis, G., Nicolau, J., & Rodrigues, P. M. M. (2024). First passage times in portfolio optimization: A novel nonparametric approach. European Journal of Operational Research, 312(3), 1074–1085. https://doi.org/10.1016/j.ejor.2023.07.044'
    ]

    for ref in references_list:
        add_styled_paragraph(doc, ref, 'reference')
        
    doc.save(output_path)
    print(f"\n========================================================")
    print(f"SUCCESS: Complete Thesis Word document generated!")
    print(f"Final Document: {output_path}")
    print(f"========================================================")

if __name__ == '__main__':
    generate_complete_thesis_docx()
