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
        p.paragraph_format.first_line_indent = Inches(0.5)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif style_type == 'chapter_header':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.page_break_before = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif style_type == 'chapter_title_centered':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif style_type == 'section_title':
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif style_type == 'table_title':
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.keep_with_next = True
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
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(space_before or 2)
        p.paragraph_format.space_after = Pt(space_after or 8)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        run.font.italic = True
        run.font.color.rgb = RGBColor(0, 0, 0)
    elif style_type == 'reference':
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
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
    
    # Enforce Times New Roman document-wide in Normal style and default font attributes
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    
    rPr = normal_style._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), 'Times New Roman')
    rFonts.set(qn('w:hAnsi'), 'Times New Roman')
    rFonts.set(qn('w:cs'), 'Times New Roman')
    
    # Chapter 4 begins on new page via chapter_header page_break_before
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
        "machine learning return forecasting under Expanding-Window Walk-Forward Validation, feature importance analysis, and out-of-sample portfolio optimization backtests.",
        'body'
    )
    
    # 4.1.1 Universe Breakdown
    add_styled_paragraph(doc, "4.1.1 Asset Universe Breakdown and Selection Rationale", 'section_title')
    add_styled_paragraph(
        doc,
        "To construct a balanced historical panel without imputing missing price histories, "
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
        "exhibit significant dispersion and notable deviations from standard Gaussian properties across all 28 assets. "
        "Extreme weekly log return realizations (specifically MANSARD at -127.16%, TRANSCORP at +139.61%, and WEMABANK at +106.29%) "
        "arise from historical exchange corporate actions such as share capital reconstructions and low-priced equity re-pricings. "
        "Prices were not adjusted for corporate actions; these observations reflect mechanical price changes rather than economic returns and inflate the reported kurtosis for these three assets.",
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
    add_styled_paragraph(
        doc,
        "Source: Author's computation (2026). Note: Kurtosis denotes excess kurtosis across all 28 assets. "
        "Minimum and maximum values represent continuously compounded weekly log returns (ln(Pt/Pt-1) * 100), "
        "where extreme outliers (MANSARD -127.16%, TRANSCORP +139.61%, WEMABANK +106.29%) reflect historical exchange "
        "corporate actions and penny-stock re-pricings. Prices were not adjusted for corporate actions; these observations "
        "reflect mechanical price changes rather than economic returns and inflate the reported kurtosis for these three assets.",
        'caption'
    )
    
    # 4.3 Diagnostic Tests
    add_styled_paragraph(doc, "4.3 Statistical Non-Normality and Stationarity Diagnostic Tests", 'section_title')
    add_styled_paragraph(
        doc,
        "To evaluate whether the empirical asset return distributions satisfy the classic Markowitz Mean-Variance assumption of Gaussian normality, "
        "formal statistical hypothesis tests were conducted. The Jarque-Bera (JB) test (Jarque & Bera, 1987) and Shapiro-Wilk (SW) test (Shapiro & Wilk, 1965) were evaluated against the null hypothesis "
        "of normality, while the Augmented Dickey-Fuller (ADF) test (Dickey & Fuller, 1979) evaluated time-series stationarity across all 28 assets.",
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
    add_styled_paragraph(doc, "Source: Author's computation (2026). Note: JB = Jarque–Bera test for normality (Jarque & Bera, 1987); SW = Shapiro–Wilk test for normality (Shapiro & Wilk, 1965); ADF = Augmented Dickey–Fuller test for time-series stationarity (Dickey & Fuller, 1979). Rejection of normality across 100% of 28 equities at p < 0.001.", 'caption')
    
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
        p_img.paragraph_format.keep_with_next = True
        p_img.add_run().add_picture(img1_path, width=Inches(6.0))
        add_styled_paragraph(doc, "Figure 4.1: NGX 28 Equity Log Return Pairwise Correlation Matrix (2010-2025)", 'caption')
        
    # 4.5 ML Forecasting
    add_styled_paragraph(doc, "4.5 Machine Learning Return Forecasting Results (Walk-Forward Validation)", 'section_title')
    add_styled_paragraph(
        doc,
        "Machine learning models (Random Forest and XGBoost Regressors) were evaluated under a rigorous Expanding-Window Walk-Forward Validation protocol. "
        "Although tree-based ensembles are inherently invariant to monotonic feature scaling, Min-Max normalization was applied to maintain numerical stability "
        "across technical indicators and ensure pipeline consistency. To guarantee zero temporal data leakage, feature scalers were fit strictly on expanding training windows, "
        "and model hyperparameters were optimized using 5-fold TimeSeriesSplit cross-validation on the initial 2010-2020 training period. Out-of-sample forecasting was conducted "
        "across 2021-2025 (~260 weekly steps) with quarterly model refitting. Table 4.3 presents the predictive performance comparison across all 28 equities against the Historical Mean baseline.",
        'body'
    )
    
    ml_perf_df = pd.read_csv('output/tables/ml_forecasting_performance.csv')
    add_styled_paragraph(doc, "Table 4.3: Out-of-Sample Predictive Performance Metrics across All 28 NGX Equities (2021-2025 Walk-Forward)", 'table_title')
    t3_headers = ["Ticker", "Base RMSE", "RF RMSE", "XGB RMSE", "Base DA (%)", "RF DA (%)", "XGB DA (%)", "Diebold-Mariano Stat", "Diebold-Mariano p-val"]
    t3_rows = []
    for _, row in ml_perf_df.iterrows():
        t3_rows.append([
            str(row['Ticker']),
            f"{row['Base RMSE']:.4f}",
            f"{row['RF RMSE']:.4f}",
            f"{row['XGB RMSE']:.4f}",
            f"{row['Base DA (%)']:.1f}%",
            f"{row['RF DA (%)']:.1f}%",
            f"{row['XGB DA (%)']:.1f}%",
            f"{row['DM_Stat']:.2f}",
            f"{row['DM_p_val']:.3f}"
        ])
    t3_rows.append([
        "AVERAGE",
        f"{ml_perf_df['Base RMSE'].mean():.4f}",
        f"{ml_perf_df['RF RMSE'].mean():.4f}",
        f"{ml_perf_df['XGB RMSE'].mean():.4f}",
        f"{ml_perf_df['Base DA (%)'].mean():.1f}%",
        f"{ml_perf_df['RF DA (%)'].mean():.1f}%",
        f"{ml_perf_df['XGB DA (%)'].mean():.1f}%",
        f"{ml_perf_df['DM_Stat'].mean():.2f}",
        f"{ml_perf_df['DM_p_val'].mean():.3f}"
    ])
    add_table_to_docx(doc, t3_headers, t3_rows)
    add_styled_paragraph(doc, "Source: Author's computation (2026). Note: Base = Historical sample mean return baseline; RF = Random Forest regressor; XGB = eXtreme Gradient Boosting regressor; RMSE = Root Mean Squared Error; DA (%) = Binary Directional Accuracy. Diebold-Mariano Stat and Diebold-Mariano p-val evaluate the null hypothesis of equal forecast accuracy between XGBoost and the Historical Mean baseline under quadratic loss with Newey–West HAC standard errors (Diebold & Mariano, 1995).", 'caption')
    
    add_styled_paragraph(doc, "4.5.1 Econometric Evaluation: Forecast Accuracy and Portfolio Value", 'section_title')
    add_styled_paragraph(
        doc,
        "A critical empirical observation in Table 4.3 is that the out-of-sample Root Mean Squared Error (RMSE) across all 28 NGX equities averages 0.0602 for the flat Historical Mean baseline, "
        "compared to 0.0608 for XGBoost and 0.0627 for Random Forest. Crucially, the formal Diebold–Mariano (1995) test reveals that for 25 out of the 28 equities (89.3%), the forecast accuracy "
        "differential between XGBoost and the Historical Mean baseline is statistically indistinguishable from zero (p > 0.05). In the three assets where equal accuracy is formally rejected "
        "(FIDSON, JBERGER, and NESTLE), the negative DM test statistic indicates that XGBoost exhibited significantly larger squared forecast errors (inferior accuracy) than the historical baseline. "
        "Furthermore, Random Forest was not evaluated under the Diebold–Mariano test despite exhibiting a higher overall RMSE (0.0627). Similarly, binary directional accuracy (DA) averages 38.1% for Random Forest "
        "and 37.8% for XGBoost vs 37.9% for the flat Historical Mean baseline across all 28 assets (peaking at 50.8% on liquid large-caps). For illiquid equities such as CONOIL (DA = 13.8%) and NESTLE (17.3%), "
        "this below-50% accuracy reflects weeks with zero or near-zero returns: when the actual return is exactly zero, any non-zero forecast is counted as a directional miss, depressing the measured accuracy below the 50% random-walk threshold. "
        "Evaluating the relationship between statistical point prediction accuracy and downstream portfolio performance requires a rigorous econometric examination across the following four points:",
        'body'
    )
    p_rmse_intro = add_styled_paragraph(
        doc,
        "1. Quadratic Loss Penalization and Noise Dominance: The apparent superiority of the flat Historical Mean in raw RMSE stems from the statistical properties of financial return noise under an L2 quadratic loss function. "
        "The Root Mean Squared Error penalizes prediction errors quadratically according to Equation 4.1:",
        'body'
    )
    
    # Native OMML Display Equation for RMSE
    rmse_omml_xml = """<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
      <w:pPr>
        <w:spacing w:before="120" w:after="120" w:line="480" w:lineRule="auto"/>
        <w:jc w:val="center"/>
        <w:rPr>
          <w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
          <w:color w:val="000000"/>
        </w:rPr>
      </w:pPr>
      <m:oMathPara>
        <m:oMath>
          <m:r>
            <w:rPr>
              <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
              <w:color w:val="000000"/>
            </w:rPr>
            <m:t>RMSE=</m:t>
          </m:r>
          <m:rad>
            <m:radPr>
              <m:degHide m:val="1"/>
              <m:ctrlPr>
                <w:rPr>
                  <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
                  <w:color w:val="000000"/>
                </w:rPr>
              </m:ctrlPr>
            </m:radPr>
            <m:deg/>
            <m:e>
              <m:f>
                <m:fPr>
                  <m:ctrlPr>
                    <w:rPr>
                      <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
                      <w:color w:val="000000"/>
                    </w:rPr>
                  </m:ctrlPr>
                </m:fPr>
                <m:num>
                  <m:r>
                    <w:rPr>
                      <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
                      <w:color w:val="000000"/>
                    </w:rPr>
                    <m:t>1</m:t>
                  </m:r>
                </m:num>
                <m:den>
                  <m:r>
                    <w:rPr>
                      <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
                      <w:color w:val="000000"/>
                    </w:rPr>
                    <m:t>n</m:t>
                  </m:r>
                </m:den>
              </m:f>
              <m:nary>
                <m:naryPr>
                  <m:chr m:val="∑"/>
                  <m:ctrlPr>
                    <w:rPr>
                      <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
                      <w:color w:val="000000"/>
                    </w:rPr>
                  </m:ctrlPr>
                </m:naryPr>
                <m:sub>
                  <m:r>
                    <w:rPr>
                      <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
                      <w:color w:val="000000"/>
                    </w:rPr>
                    <m:t>t=1</m:t>
                  </m:r>
                </m:sub>
                <m:sup>
                  <m:r>
                    <w:rPr>
                      <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
                      <w:color w:val="000000"/>
                    </w:rPr>
                    <m:t>n</m:t>
                  </m:r>
                </m:sup>
                <m:e>
                  <m:sSup>
                    <m:sSupPr>
                      <m:ctrlPr>
                        <w:rPr>
                          <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
                          <w:color w:val="000000"/>
                        </w:rPr>
                      </m:ctrlPr>
                    </m:sSupPr>
                    <m:e>
                      <m:d>
                        <m:dPr>
                          <m:ctrlPr>
                            <w:rPr>
                              <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
                              <w:color w:val="000000"/>
                            </w:rPr>
                          </m:ctrlPr>
                        </m:dPr>
                        <m:e>
                          <m:acc>
                            <m:accPr>
                              <m:ctrlPr>
                                <w:rPr>
                                  <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
                                  <w:color w:val="000000"/>
                                </w:rPr>
                              </m:ctrlPr>
                            </m:accPr>
                            <m:e>
                              <m:sSub>
                                <m:sSubPr>
                                  <m:ctrlPr>
                                    <w:rPr>
                                      <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
                                      <w:color w:val="000000"/>
                                    </w:rPr>
                                  </m:ctrlPr>
                                </m:sSubPr>
                                <m:e>
                                  <m:r>
                                    <w:rPr>
                                      <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
                                      <w:color w:val="000000"/>
                                    </w:rPr>
                                    <m:t>y</m:t>
                                  </m:r>
                                </m:e>
                                <m:sub>
                                  <m:r>
                                    <w:rPr>
                                      <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
                                      <w:color w:val="000000"/>
                                    </w:rPr>
                                    <m:t>t</m:t>
                                  </m:r>
                                </m:sub>
                              </m:sSub>
                            </m:e>
                          </m:acc>
                          <m:r>
                            <w:rPr>
                              <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
                              <w:color w:val="000000"/>
                            </w:rPr>
                            <m:t>-</m:t>
                          </m:r>
                          <m:sSub>
                            <m:sSubPr>
                              <m:ctrlPr>
                                <w:rPr>
                                  <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
                                  <w:color w:val="000000"/>
                                </w:rPr>
                              </m:ctrlPr>
                            </m:sSubPr>
                            <m:e>
                              <m:r>
                                <w:rPr>
                                  <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
                                  <w:color w:val="000000"/>
                                </w:rPr>
                                <m:t>y</m:t>
                              </m:r>
                            </m:e>
                            <m:sub>
                              <m:r>
                                <w:rPr>
                                  <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
                                  <w:color w:val="000000"/>
                                </w:rPr>
                                <m:t>t</m:t>
                              </m:r>
                            </m:sub>
                          </m:sSub>
                        </m:e>
                      </m:d>
                    </m:e>
                    <m:sup>
                      <m:r>
                        <w:rPr>
                          <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
                          <w:color w:val="000000"/>
                        </w:rPr>
                        <m:t>2</m:t>
                      </m:r>
                    </m:sup>
                  </m:sSup>
                </m:e>
              </m:nary>
            </m:e>
          </m:rad>
        </m:oMath>
      </m:oMathPara>
    </w:p>"""
    p_rmse_intro._p.addnext(parse_xml(rmse_omml_xml))
    
    add_styled_paragraph(
        doc,
        "where the forecast error is evaluated over out-of-sample weekly test steps. At weekly sampling horizons, equity return series are dominated "
        "by high-frequency, zero-mean unobserved news noise. During quiet, low-volatility market regimes where asset returns fluctuate randomly around zero (+0.4%, -0.2%, +0.1%), a static forecast "
        "equal to the historical sample mean (with a constant forecasted weekly return of 0.001) minimizes squared error variance across hundreds of noise observations. Conversely, non-linear ML models generate dynamic, non-zero "
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
        "3. Technical Indicator Dynamics and Parity with Historical Means: Tree-based machine learning ensembles (Random Forest and XGBoost) extract non-linear cross-sectional signals from technical indicators. Feature importance analysis "
        "(Section 4.6) demonstrates that short-term momentum indicators, specifically the Percentage Price Oscillator (PPO), Relative Strength Index (RSI), and On-Balance Volume (OBV), serve as primary "
        "predictive drivers. However, contrary to the hypothesis that dynamic return rankings would generate a superior portfolio edge, downstream optimization reveals that this technical signal does not significantly improve portfolio outcomes over static historical means: "
        "XGB-CVaR and Historical-CVaR achieve statistically indistinguishable gross Sharpe ratios (difference +0.02, q = 0.591).",
        'body'
    )
    add_styled_paragraph(
        doc,
        "4. Tail-Risk Mitigation and Convex Optimization: When these dynamic expected return vectors are passed into the convex Mean-CVaR linear program, the optimizer re-allocates capital toward high-ranked momentum equities while "
        "penalizing assets exposed to left-tail drawdowns. Under zero fee friction (Table 4.5), XGB-CVaR achieves a gross Sharpe ratio of 1.52 (+42.00% annualized return, -22.09% max drawdown), "
        "yielding a Sharpe outperformance over passive indexing that is statistically significant at the unadjusted level (Ledoit-Wolf circular block bootstrap p = 0.015) but marginal after Benjamini–Hochberg False Discovery Rate correction for 18 simultaneous comparisons (q = 0.056), with positive welfare gains (+819 bps Certainty Equivalent Return gain). "
        "Crucially, when transaction costs are introduced, the CVaR optimization structure itself delivers the robustly significant result: under institutional fees, active XGB-CVaR is significantly outperformed by low-turnover Historical-CVaR (Sharpe diff -0.25, FDR q = 0.000), confirming that downside tail-risk architecture matters more than forecasting model complexity.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "Consistent with the Diebold–Mariano results, the machine learning forecasts do not add statistically significant value at the portfolio level: XGB-CVaR and Historical-CVaR, which share the same optimizer and differ only in their return inputs, have statistically indistinguishable gross Sharpe ratios (difference +0.02, q = 0.591). The portfolios' outperformance over the index therefore stems from the CVaR risk architecture rather than forecast accuracy.",
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
        p_img2.paragraph_format.keep_with_next = True
        p_img2.add_run().add_picture(img2_path, width=Inches(5.8))
        add_styled_paragraph(doc, "Figure 4.2: Feature Importance Breakdown across Technical Indicators", 'caption')
        
    # 4.7 Portfolio Backtest
    add_styled_paragraph(doc, "4.7 Out-of-Sample Portfolio Optimization Backtest and Sensitivity Analysis", 'section_title')
    add_styled_paragraph(
        doc,
        "Six portfolio strategies were backtested out-of-sample over the 2021-2025 period: RF-CVaR, XGB-CVaR, Historical-CVaR, Markowitz Mean-Variance Optimization (MVO), "
        "1/N Equal Weighting, and NGX Index Buy-and-Hold. Backtests were evaluated under three distinct market fee regimes: (i) a 1.50% retail transaction fee and market slippage model (150 bps), "
        "(ii) a 0.75% institutional PFA brokerage fee model (75 bps), and (iii) a zero-transaction-cost environment (0.00%) to evaluate gross portfolio performance. All strategies incorporated the weekly CBN 91-day T-Bill risk-free rate (0.319% / 18.00% annualized).",
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
    add_styled_paragraph(doc, "Source: Author's computation (2026). Note: Ann. Ret = Annualized Return; Ann. Vol = Annualized Volatility; Sharpe = Sharpe Ratio (Sharpe, 1966) using 18.00% annual (0.319% weekly) CBN 91-day T-bill risk-free rate; Sortino = Sortino Ratio (Sortino & Price, 1994); VaR 95% = 95% Value-at-Risk; CVaR 95% = 95% Conditional Value-at-Risk; Max DD (%) = Maximum Peak-to-Trough Drawdown. Evaluated under 1.50% (150 bps) retail transaction fee and execution slippage.", 'caption')
    
    port_zero_df = pd.read_csv('output/tables/portfolio_performance_zero_cost.csv')
    add_styled_paragraph(doc, "Table 4.5: Out-of-Sample Portfolio Performance under Zero Transaction Fees (Gross Performance - 0.00%)", 'table_title')
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
    add_styled_paragraph(doc, "Source: Author's computation (2026). Note: Ann. Ret = Annualized Return; Ann. Vol = Annualized Volatility; Sharpe = Sharpe Ratio (Sharpe, 1966); Sortino = Sortino Ratio (Sortino & Price, 1994); VaR 95% = 95% Value-at-Risk; CVaR 95% = 95% Conditional Value-at-Risk; Max DD (%) = Maximum Peak-to-Trough Drawdown. Gross performance evaluated under 0.00% transaction fee friction.", 'caption')
    
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
    add_styled_paragraph(doc, "Source: Author's computation (2026). Note: Ann. Return = Annualized Return; Ann. Vol = Annualized Volatility; Sharpe = Sharpe Ratio (Sharpe, 1966); Sortino = Sortino Ratio (Sortino & Price, 1994); VaR 95% = 95% Value-at-Risk; CVaR 95% = 95% Conditional Value-at-Risk; Max DD (%) = Maximum Peak-to-Trough Drawdown; Wk Turnover (%) = Average Weekly Portfolio Turnover. Evaluated under 0.75% (75 bps) institutional PFA brokerage execution fees.", 'caption')
    
    img3_path = 'output/figures/portfolio_equity_curves.png'
    if os.path.exists(img3_path):
        p_img3 = doc.add_paragraph()
        p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img3.paragraph_format.keep_with_next = True
        p_img3.add_run().add_picture(img3_path, width=Inches(6.0))
        add_styled_paragraph(doc, "Figure 4.3: Out-of-Sample Cumulative Wealth Growth Curves (2021-2025)", 'caption')
        
    # 4.7.1 Statistical Significance
    add_styled_paragraph(doc, "4.7.1 Statistical Significance of Portfolio Outperformance across Market Fee Regimes", 'section_title')
    add_styled_paragraph(
        doc,
        "To evaluate whether the risk-adjusted outperformance of active Mean-CVaR strategies over passive benchmarks is statistically significant, "
        "inferential hypothesis testing was conducted across all three market fee regimes. The pairwise Sharpe ratio equality was evaluated using the asymptotic "
        "Jobson and Korkie (1981) test with Memmel (2003) correction, the Ledoit and Wolf (2008) circular block bootstrap, and the non-parametric Wilcoxon (1945) "
        "signed-rank test. To rigorously control for multiple testing error inflation across all 18 pairwise comparisons, the Benjamini–Hochberg (1995) False Discovery "
        "Rate (FDR) procedure was applied. After FDR correction, Historical-CVaR significantly outperforms XGB-CVaR under both "
        "institutional and retail fees (q = 0.000), and MVO significantly underperforms 1/N under retail fees (q = 0.009; institutional q = 0.056). "
        "Economically, both CVaR specifications outperform unconstrained MVO across all fee tiers (Tables 4.4–4.5b), while Table 4.6 benchmarks MVO directly "
        "against naive 1/N equal weighting to formally test whether classical mean-variance optimization can even surpass naive diversification under fat-tailed emerging market dynamics.",
        'body'
    )
    
    sig_df = pd.read_csv('output/tables/portfolio_significance_tests.csv')
    add_styled_paragraph(doc, "Table 4.6: Multi-Tier Pairwise Hypothesis Testing of Sharpe Ratio Equality across Fee Regimes", 'table_title')
    t6_headers = ["Fee Regime", "Strategy", "Benchmark", "Sharpe Diff", "Jobson-Korkie p-val", "Ledoit-Wolf Sharpe p-val", "Benjamini-Hochberg (FDR q-val)", "Wilcoxon p-val"]
    t6_rows = []
    for _, row in sig_df.iterrows():
        t6_rows.append([
            str(row['Fee Regime']),
            str(row['Strategy']),
            str(row['Benchmark']),
            f"{row['Sharpe Diff']:+.2f}",
            f"{row['Jobson-Korkie p-val']:.3f}",
            f"{row['Ledoit-Wolf Sharpe p-val']:.3f}",
            f"{row['Benjamini-Hochberg (FDR q-val)']:.3f}",
            f"{row['Wilcoxon p-val']:.3f}"
        ])
    add_table_to_docx(doc, t6_headers, t6_rows)
    add_styled_paragraph(doc, "Source: Author's computation (2026). Note: Sharpe Diff = Difference in annualized Sharpe ratio (Strategy minus Benchmark); Jobson-Korkie p-val = Asymptotic Z-test p-value under Gaussian assumptions (Jobson & Korkie, 1981; Memmel, 2003); Ledoit-Wolf Sharpe p-val = Circular block bootstrap p-value robust to fat tails and autocorrelation with 2,000 resamples (Ledoit & Wolf, 2008); Benjamini-Hochberg (FDR q-val) = False Discovery Rate adjusted q-value controlling the expected proportion of false positives across all 18 simultaneous pairwise comparisons (Benjamini & Hochberg, 1995); Wilcoxon p-val = Non-parametric Wilcoxon signed-rank test p-value (Wilcoxon, 1945).", 'caption')
    
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
        "Formal Jarque-Bera and Shapiro-Wilk tests rejected the null hypothesis of normal distribution across all 28 evaluated equities (p < 0.001). The return distributions exhibit predominantly positive skewness (cross-sectional mean = +0.54) combined with excess kurtosis across all 28 assets (ranging from 2.20 to 14.47 among assets unaffected by corporate actions), indicating heavy-tailed, leptokurtic distributions. Under these conditions, standard variance , which penalizes upside and downside deviations symmetrically, overstates the risk contribution of positive outliers while underestimating the severity of left-tail losses. Econometrically, this confirms that empirical NGX equity returns are characterized by fat tails "
        "and asymmetric risk profiles. These results strongly support the theoretical arguments and empirical evidence of Mozumder et al. (2024), Adegboyo & Sarwar (2025), Uzoaga et al. (2025a), and Alim et al. (2024), who emphasize that emerging frontier stock markets experience "
        "pronounced price jumps, policy shifts, and macroeconomic shocks that invalidate Gaussian assumptions. Conversely, these findings contrast with the theoretical premise of classical dispersion models (Bali et al., 2007; Samaniego Alcántar, 2023), which argue that standard variance can serve as an adequate proxy for portfolio risk when higher-order moments exhibit finite-sample instability. On the NGX, relying strictly on standard variance underestimates tail-risk exposure during market downturns, supporting the adoption of downside risk measures such as Conditional Value-at-Risk (CVaR).",
        'body'
    )
    
    # Paragraph 2: Objective 2
    add_styled_paragraph(
        doc,
        "Secondly, regarding the performance of non-linear Machine Learning models in forecasting weekly NGX equity returns under Expanding-Window Walk-Forward Validation, the empirical results in Section 4.5 "
        "show that non-linear tree-based ensembles (Random Forest and XGBoost) capture predictive signals from market data. While raw point forecasting metrics (RMSE) hover close to historical baselines due to weekly noise variance, "
        "Random Forest achieved an average out-of-sample directional accuracy of 38.1% across liquid NGX equities (with individual assets reaching up to 50.8%), compared to 37.9% for historical baselines and 37.8% for XGBoost. Feature importance analysis (Section 4.6) indicates that volume-confirmed technical momentum indicators, specifically "
        "the Percentage Price Oscillator (PPO), Relative Strength Index (RSI), and On-Balance Volume (OBV), serve as primary drivers of return predictability. This aligns with empirical asset pricing literature (Gu et al., 2020; Chao, 2024; Ojo & Okafor, 2024; Ajiga et al., 2024; Ferrari et al., 2024), "
        "demonstrating that machine learning algorithms capture non-linear market interactions and trend-persistence dynamics in emerging economies. However, this finding also engages with contrasting perspectives: it engages with the weak-form Efficient Market Hypothesis (Fama, 1970) by testing whether past technical price and volume patterns yield economic value, while contrasting with the findings of Moyoweshumba & Seitshiro (2025) on the Johannesburg Stock Exchange. Whereas Moyoweshumba and Seitshiro found that machine learning return forecasts delivered dramatic gains over traditional Markowitz allocation on the JSE, on the NGX machine learning return forecasts added no statistically significant edge over historical sample means (gross Sharpe difference +0.02, q = 0.591).",
        'body'
    )
    
    # Paragraph 3: Objective 3
    add_styled_paragraph(
        doc,
        "Thirdly, regarding the performance of integrated ML-CVaR portfolio strategies compared against classical Markowitz Mean-Variance Optimization and 1/N benchmarks, the backtest results in Section 4.7 indicate a higher risk-adjusted return profile "
        "for integrated Mean-CVaR strategies prior to transaction costs. Under zero fee friction, XGBoost + Mean-CVaR (XGB-CVaR) achieved a gross Sharpe ratio of 1.52 (42.00% annualized return, -22.09% max drawdown), compared to 0.91 for the passive NGX Index Buy-and-Hold benchmark "
        "and 0.76 for Markowitz MVO. Inferential hypothesis testing (Section 4.7.1) indicates that this Sharpe ratio outperformance is statistically significant at the unadjusted level under Ledoit-Wolf circular block bootstrap tests (p = 0.015), but is marginal after Benjamini–Hochberg False Discovery Rate correction for 18 simultaneous comparisons (q = 0.056). "
        "Crucially, the honestly significant finding that survives rigorous multiple testing correction is that the CVaR risk architecture decisively protects capital under transaction frictions: unconstrained MVO collapses against 1/N equal weighting under retail fees (FDR q = 0.009), while static low-turnover Historical-CVaR significantly outperforms high-turnover XGB-CVaR under institutional fees (Sharpe diff -0.25, FDR q = 0.000). Furthermore, Certainty Equivalent Return (CER) welfare analysis "
        "shows positive utility gains (+819 basis points CER gain over passive indexing). These results corroborate established portfolio selection theory (Markowitz, 1952; Rockafellar & Uryasev, 2000; Bodnar et al., 2022; Hsiao, 2025), showing that convex tail-risk constraints improve risk-adjusted outcomes regardless of whether forward-looking ML return forecasts or historical sample means are employed. Nevertheless, these findings provide a nuanced contrast to the empirical work of San (2025) and the classic estimation-error critique of naive diversification, which assert that simple 1/N equal weighting consistently outperforms or equals optimized portfolios out-of-sample due to parameter uncertainty. While 1/N achieves a robust gross Sharpe of 1.07 on the NGX (Table 4.5), disciplined CVaR tail-loss minimization achieves superior downside protection (-22.09% max drawdown versus -23.95% for 1/N), demonstrating that tail-risk optimization delivers distinct economic value.",
        'body'
    )
    
    # Paragraph 4: Objective 4
    add_styled_paragraph(
        doc,
        "Fourthly, regarding portfolio robustness under market stress and transaction cost frictions, the empirical evaluation in Section 4.7 highlights execution dynamics across market participant regimes. Under 1.50% retail fees and slippage, "
        "unconstrained Markowitz MVO experienced severe weight instability (99.28% average weekly turnover), resulting in a maximum drawdown of -86.38% and negative economic welfare (CER = -64.09%). This strongly supports Michaud's (1989) finding regarding the sensitivity of unconstrained MVO "
        "to estimation error in high-friction environments. Conversely, low-turnover Historical-CVaR (0.38% turnover) displayed resilience, retaining net Sharpe ratios of 1.48 (retail) and 1.49 (institutional). "
        "While active ML models generate gross risk-adjusted outperformance prior to friction over the index, comparable to Historical-CVaR, weekly rebalancing turnover (11.00%) incurs an annual fee drag (~3.6% to ~7.2%) that erodes gross returns after fees. This finding aligns with transaction cost literature (Job, 2022; Alotaibi et al., 2022; Kevin & Yugopuspito, 2025), "
        "indicating that structural tail-risk architecture (CVaR) plays a central role in frictional emerging markets. It also qualifies the assertions of high-frequency quantitative models that advocate unconstrained algorithmic rebalancing, demonstrating that without explicit turnover penalties or execution smoothing bands, transaction friction rapidly neutralizes statistical predictive edges on frontier exchanges.",
        'body'
    )
    
    # =========================================================================
    # CHAPTER 5: SUMMARY, CONCLUSION, AND RECOMMENDATIONS
    # =========================================================================
    add_styled_paragraph(doc, "CHAPTER FIVE", 'chapter_header')
    add_styled_paragraph(doc, "SUMMARY, CONCLUSION AND RECOMMENDATIONS", 'chapter_title_centered')
    
    add_styled_paragraph(doc, "5.1 Summary of Findings", 'section_title')
    add_styled_paragraph(
        doc,
        "1. Statistical Non-Normality and Tail-Risk Exposure: Formal statistical diagnostic tests (Jarque-Bera and Shapiro-Wilk) rejected Gaussian normality across all 28 evaluated NGX equities (p < 0.001). "
        "The empirical return distributions exhibited predominantly positive skewness (cross-sectional mean = +0.54) combined with excess kurtosis across all 28 assets (ranging from 2.20 to 14.47 among assets unaffected by corporate actions), indicating heavy-tailed, leptokurtic distributions that support the use of downside Conditional Value-at-Risk (CVaR) over standard variance.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "2. Machine Learning Return Forecasting Dynamics: Non-linear machine learning ensembles (Random Forest and XGBoost) evaluated under Expanding-Window Walk-Forward Validation captured time-varying market dynamics. "
        "Random Forest achieved the highest average out-of-sample directional accuracy of 38.1% across liquid NGX equities (with individual assets reaching up to 50.8%), driven primarily by volume-confirmed momentum features (Percentage Price Oscillator, Relative Strength Index, and On-Balance Volume).",
        'body'
    )
    add_styled_paragraph(
        doc,
        "3. Out-of-Sample Portfolio Optimization Performance: Integrating machine learning return forecasts into a convex Mean-CVaR optimization framework generated higher risk-adjusted returns under zero fee friction relative to the market index. "
        "XGBoost + Mean-CVaR achieved a gross Sharpe ratio of 1.52 (42.00% annualized return, -22.09% maximum drawdown) compared to 0.91 for the passive NGX Index Buy-Hold baseline. This gross outperformance over the index is statistically significant at the unadjusted level (Ledoit-Wolf circular block bootstrap p = 0.015), but marginal after Benjamini–Hochberg False Discovery Rate correction for 18 simultaneous comparisons (q = 0.056), while delivering Certainty Equivalent Return utility gains (+819 bps CER gain). "
        "Crucially, XGB-CVaR and Historical-CVaR achieved statistically indistinguishable gross Sharpe ratios (1.52 vs 1.50, difference +0.02, FDR q = 0.591), confirming that outperformance over the market index stems from the convex CVaR risk architecture rather than machine learning return forecasts. Under transaction friction, low-turnover Historical-CVaR significantly outperforms active XGB-CVaR under institutional fees (q = 0.000), and unconstrained MVO collapses against 1/N equal weighting under retail friction (q = 0.009).",
        'body'
    )
    add_styled_paragraph(
        doc,
        "4. Transaction Cost Dynamics and Turnover Friction: Evaluating portfolio performance under market stress and multi-tier transaction cost friction demonstrated that unconstrained Markowitz Mean-Variance Optimization experiences severe performance degradation (-86.38% drawdown, -64.09% CER utility) due to high turnover (99.28% weekly turnover). "
        "Under institutional (0.75%) and retail (1.50%) brokerage fees, active ML rebalancing turnover (11.00%) creates an annual fee drag (~3.6% to ~7.2%) that erodes gross returns after fees, while low-turnover Historical-CVaR (0.38% turnover) maintains stable post-fee performance (net Sharpe 1.48 to 1.49, pairwise Ledoit-Wolf p = 0.000, FDR q = 0.000 vs XGB-CVaR).",
        'body'
    )
    
    add_styled_paragraph(doc, "5.2 Conclusion", 'section_title')
    add_styled_paragraph(
        doc,
        "This study investigated equity return forecasting and tail-risk-aware portfolio optimization across 28 liquid equities on the Nigerian Exchange Group (NGX) spanning a 16-year period (2010-2025). "
        "The research evaluated non-normality diagnostics, Machine Learning return forecasting (Random Forest and XGBoost) under Expanding-Window Walk-Forward Validation, and convex Mean-CVaR asset allocation backtesting.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "The overall conclusion of this research is that while tail-risk-aware CVaR optimization delivers substantial risk-adjusted outperformance and downside protection on the NGX (+819 bps CER gain over passive indexing), machine learning return forecasts provide no statistically significant enhancement over simple historical sample means, and high-turnover rebalancing incurs severe transaction fee drag. "
        "Consequently, structural tail-risk management via Conditional Value-at-Risk (CVaR) appears to be the primary contributor to real-world investor economic surplus in the NGX context studied. "
        "This indicates that downside tail-risk architecture plays a far more critical role than model forecasting complexity in frictional emerging equity markets.",
        'body'
    )
    
    add_styled_paragraph(doc, "5.3 Policy and Practical Recommendations", 'section_title')
    
    add_styled_paragraph(doc, "5.3.1 Regulatory and Macroeconomic Policy Recommendations", 'section_title')
    add_styled_paragraph(
        doc,
        "1. PENCOM Investment Guidelines Update: The National Pension Commission (PENCOM) may consider incorporating downside tail-risk metrics, such as Conditional Value-at-Risk (CVaR at 95% confidence level), alongside traditional variance-based measures in its Investment Guidelines for Fund I, Fund II, and Fund III equity portfolios. Pension Fund Administrators (PFAs) could evaluate CVaR-constrained allocation models to protect pension assets during extreme macroeconomic shocks.",
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
        "1. Adoption of Low-Turnover Tail-Risk Frameworks: Pension Fund Administrators (PFAs) and institutional fund managers operating on the NGX should evaluate Mean-CVaR asset allocation as a complement or alternative to classical Markowitz Mean-Variance Optimization. To prevent fee erosion, institutional managers should enforce strict turnover caps, employ turnover-penalized objective functions, or adopt quarterly rebalancing protocols.",
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
        "1. Stress-Testing and Downside Risk Auditing: Risk officers and quantitative portfolio managers should consider regular stress testing using historical block bootstrap resampling and non-parametric CVaR estimation to evaluate portfolio tail loss limits.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "2. Turnover-Constrained Rebalancing and Fee Auditing: Quantitative portfolio managers on frontier exchanges must implement turnover constraints (such as rebalancing bands, penalty terms, or quarterly re-allocation schedules) to prevent aggressive portfolio turnover from eroding gross risk-adjusted performance across institutional and retail transaction fee tiers.",
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
    add_styled_paragraph(
        doc,
        "4. Sample Selection Bias: The requirement for complete 16-year price histories (2010\u20132025) may introduce survivorship and sample-selection bias, as only securities that remained "
        "continuously listed and traded throughout the full sample period were retained. Firms that delisted, were suspended, or entered the market after 2010 are not represented in the analysis. "
        "This limitation should be considered when generalizing findings to the broader NGX universe.",
        'body'
    )
    add_styled_paragraph(
        doc,
        "5. Price-Only Returns and Unadjusted Corporate Actions: This study used price-only (capital appreciation) returns rather than total returns inclusive of dividend distributions. "
        "Given that several NGX equities offer meaningful dividend yields, the reported returns may understate total investment performance across all strategies. "
        "Additionally, prices were not adjusted for corporate actions; these observations reflect mechanical price changes rather than economic returns and inflate the reported kurtosis for these three assets (MANSARD, TRANSCORP, and WEMABANK; see Section 4.2).",
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
        "(Random Forest and XGBoost with TimeSeriesSplit cross-validation tuning), convex Mean-CVaR linear programming portfolio optimization backtests, is "
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
    add_styled_paragraph(doc, "REFERENCES", 'chapter_header')
    
    references_list = [
        'Adegboyo, O. S., & Sarwar, K. (2025). Modelling and forecasting of Nigeria stock market volatility. Future Business Journal, 11(1), Article 124. https://doi.org/10.1186/s43093-025-00536-4',
        'Ajiga, D. I., Adeleye, R. A., Tubokirifuruar, T. S., Bello, B. G., Ndubuisi, N. L., Asuzu, O. F., & Owolabi, O. R. (2024). Machine learning for stock market forecasting: A review of models and accuracy. Finance & Accounting Research Journal, 6(2).',
        'Alfeus, M., Harvey, J., & Maphatsoe, P. (2024). Improving realised volatility forecast for emerging markets. Journal of Economics and Finance. Advance online publication. https://doi.org/10.1007/s12197-024-09701-x',
        'Alfzari, S., Al-Shboul, M., & Alshurideh, M. (2025). Predictive analytics in portfolio management: A fusion of AI and investment economics for optimal risk-return trade-offs. International Review of Management and Marketing, 15(2), 365–380. https://doi.org/10.32479/irmm.18594',
        'Alim, W., Khan, N. U., Zhang, V. W., Cai, H. H., Mikhaylov, A., & Yuan, Q. (2024). Influence of political stability on the stock market returns and volatility: GARCH and EGARCH approach. Financial Innovation. https://doi.org/10.1186/s40854-024-00658-8',
        'Alotaibi, T. S., Dalla Valle, L., & Craven, M. J. (2022). The worst case GARCH-copula CVaR approach for portfolio optimisation: Evidence from financial markets. Journal of Risk and Financial Management, 15(10), Article 482. https://doi.org/10.3390/jrfm15100482',
        'Arif, U., Sohail, M. T., & Majeed, M. I. (2020). Portfolio optimization with mean-variance & mean-CVaR: Evidence from Pakistan stock market. International Journal of Management Research & Emerging Sciences, 10(2), 215–226.',
        'Artzner, P., Delbaen, F., Eber, J.-M., & Heath, D. (1999). Coherent measures of risk. Mathematical Finance, 9(3), 203–228. https://doi.org/10.1111/1467-9965.00068',
        'Ashrafzadeh, M., Sadrani, M., & Zolfani, S. H. (2025). Clustering-based return prediction model for stock pre-selection in portfolio optimization. Results in Engineering, 27, Article 106263. https://doi.org/10.1016/j.rineng.2025.106263',
        'Bali, T. G., Gokcan, S., & Liang, B. (2007). Value at risk and the cross-section of hedge fund returns. Journal of Banking & Finance, 31(4), 1135–1166. https://doi.org/10.1016/j.jbankfin.2006.10.023',
        'Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A practical and powerful approach to multiple testing. Journal of the Royal Statistical Society: Series B (Methodological), 57(1), 289–300. https://doi.org/10.1111/j.2517-6161.1995.tb02031.x',
        'Bodnar, T., Lindholm, M., Niklasson, V., & Thorsén, E. (2022). Bayesian portfolio selection using VaR and CVaR. Applied Mathematics and Computation, 427, Article 127120.',
        'Breiman, L. (2001). Random forests. Machine Learning, 45(1), 5–32. https://doi.org/10.1023/A:1010933404324',
        'Chao, L. (2024). Application of machine learning in stock market return forecasting. International Journal of Scientific Research and Management (IJSRM), 12(7), 6827–6835. https://doi.org/10.18535/ijsrm/v12i07.em11',
        'Chaweewanchon, A., & Chaysiri, R. (2022). Markowitz mean-variance portfolio optimization with predictive stock selection using machine learning. International Journal of Financial Studies, 10(3), Article 64. https://doi.org/10.3390/ijfs10030064',
        'Chen, R. (2025). Stock price prediction and portfolio optimization based on mean variance model and random forest model. Advances in Economics, Business and Management Research, 333, 358–367.',
        'Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 785–794. https://doi.org/10.1145/2939672.2939785',
        'Cheng, Y. (2025). Monte Carlo-Based VaR Estimation and Backtesting Under Basel III. Risks, 13(8), Article 146. https://doi.org/10.3390/risks13080146',
        'Chung, V., Espinoza, J., & Quispe, R. (2025). Forecasting Financial Volatility Under Structural Breaks: A Comparative Study of GARCH Models and Deep Learning Techniques. Journal of Risk and Financial Management, 18(9), Article 494. https://doi.org/10.3390/jrfm18090494',
        'Dickey, D. A., & Fuller, W. A. (1979). Distribution of the estimators for autoregressive time series with a unit root. Journal of the American Statistical Association, 74(366), 427–431. https://doi.org/10.2307/2286348',
        'Diebold, F. X., & Mariano, R. S. (1995). Comparing predictive accuracy. Journal of Business & Economic Statistics, 13(3), 253–263. https://doi.org/10.1080/07350015.1995.10524599',
        'Espiga-Fernández, F., García-Sánchez, Á., & Ordieres-Meré, J. (2024). A Systematic Approach to Portfolio Optimization: A Comparative Study of Reinforcement Learning Agents, Market Signals, and Investment Horizons. Algorithms, 17(12), Article 570. https://doi.org/10.3390/a17120570',
        'Fama, E. F. (1970). Efficient capital markets: A review of theory and empirical work. The Journal of Finance, 25(2), 383–417. https://doi.org/10.1111/j.1540-6261.1970.tb00518.x',
        'Fan, Y. (2025). Enhancing investment strategies with LSTM-based stock prediction and mean-variance portfolio optimization. Advances in Economics, Management and Political Sciences, 182, 110–117. https://doi.org/10.54254/2754-1169/2024.23667',
        'Fapetu, O., Ojo, S. M., Balogun, A. A., & Asaolu, A. A. (2021). Capital market performance and macroeconomic dynamics in Nigeria. FUOYE Journal of Finance and Contemporary Issues, 1(1), 29–37.',
        'Fatouros, G., Makridis, G., Kotios, D., Soldatos, J., Filippakis, M., & Kyriazis, D. (2023). DeepVaR: A framework for portfolio risk assessment leveraging probabilistic deep neural networks. Digital Finance, 5(1), 29–56.',
        'Ferrari, D., Paterlini, S., Rigamonti, A., & Weissensteiner, A. (2024). Smoothed semicovariance estimation for portfolio selection. Annals of Operations Research. Advance online publication. https://doi.org/10.1007/s10479-024-06043-z',
        'Gu, S., Kelly, B., & Xiu, D. (2020). Empirical asset pricing via machine learning. The Review of Financial Studies, 33(5), 2223–2273. https://doi.org/10.1093/rfs/hhz113',
        'He, W. (2022). An empirical research based on Markowitz\'s portfolio theory. World Scientific Research Journal, 8(3), 221–227. https://doi.org/10.6911/WSRJ.202203_8(3).0028',
        'Hsiao, Y.-Y. (2025). A comprehensive survey of modern portfolio optimization: From traditional risk analysis to advanced analytics and machine learning approaches. Advances in Economics, Management and Political Sciences, 166, 189–194. https://doi.org/10.54254/2754-1169/2025.21140',
        'Huang, R., Kambouroudis, D., & McMillan, D. G. (2025). Is portfolio diversification still effective: Evidence spanning three crises from the perspective of U.S. investors. Journal of Asset Management, 26(2), 115–135. https://doi.org/10.1057/s41260-025-00398-z',
        'Jarque, C. M., & Bera, A. K. (1987). A test for normality of observations and regression residuals. International Statistical Review, 55(2), 163–172. https://doi.org/10.2307/1403192',
        'Job, O. D. (2022). An empirical evaluation of alternative asset allocation policies for emerging and frontier market investors in Africa. Journal of Financial Risk Management, 11(3), 481–521. https://doi.org/10.4236/jfrm.2022.113024',
        'Jobson, J. D., & Korkie, B. M. (1981). Performance hypothesis testing with the Sharpe and Treynor measures. The Journal of Finance, 36(4), 889–908.',
        'Kevin, J., & Yugopuspito, P. (2025). Hybrid LSTM and PPO networks for dynamic portfolio optimization. arXiv:2511.17963. https://arxiv.org/abs/2511.17963',
        'Leccadito, A., Staino, A., & Toscano, P. (2024). A novel robust method for estimating the covariance matrix of financial returns with applications to risk management. Financial Innovation, 10, Article 116.',
        'Ledoit, O., & Wolf, M. (2008). Robust performance hypothesis testing with the Sharpe ratio. Journal of Empirical Finance, 15(5), 850–859.',
        'Li, G. (2023). Portfolio optimization and risk analysis in financial markets. Proceedings of the 2nd International Conference on Financial Technology and Business Analysis, 61, 236–246. https://doi.org/10.54254/2754-1169/61/20231273',
        'Lorimer, D. A., van Schalkwyk, C. H., & Szczygielski, J. J. (2024). Portfolio optimisation using alternative risk measures. Finance Research Letters, 67, Article 105758. https://doi.org/10.1016/j.frl.2024.105758',
        'Lyu, X. (2024). Portfolio Optimization Strategies: New Approaches Based on Machine Learning Forecasting. Highlights in Business, Economics and Management, 40, 1077–1082.',
        'Mahadevaswamy, G. H., & Shyamala, G. (2022). Markowitz Model Is Right Choice to Investment. International Journal of Novel Research and Development, 7(7), 305–314.',
        'Manogna, R. L., & Kulkarni, N. (2025). Portfolio Optimization Model for Stock Price Prediction Using Machine Learning. Journal of Statistical Theory and Applications, 24, 1091–1108. https://doi.org/10.1007/s44199-025-00140-z',
        'Markowitz, H. (1952). Portfolio selection. The Journal of Finance, 7(1), 77–91. https://doi.org/10.1111/j.1540-6261.1952.tb01525.x',
        'Martínez-Barbero, X., Cervelló-Royo, R., & Ribal, J. (2024). Portfolio optimization with prediction-based return using Long Short-Term Memory neural networks: Testing on upward and downward European markets. Computational Economics, 65, 1479–1504. https://doi.org/10.1007/s10614-024-10604-6',
        'Mba, J. C., Ababio, K. A., & Agyei, S. K. (2022). Markowitz mean-variance portfolio selection and optimization under a behavioral spectacle: New empirical evidence. International Journal of Financial Studies, 10(2), Article 28. https://doi.org/10.3390/ijfs10020028',
        'Memmel, C. (2003). Performance hypothesis testing with the Sharpe ratio. Finance Letters, 1(1), 21–23.',
        'Michaud, R. O. (1989). The Markowitz optimization enigma: Is \'optimized\' optimal? Financial Analysts Journal, 45(1), 31–42. https://doi.org/10.2469/faj.v45.n1.31',
        'Moyoweshumba, E., & Seitshiro, M. (2025). Leveraging Markowitz, Random Forest, and XGBoost for optimal diversification of South African stock portfolios. Data Science in Finance and Economics, 5(2), 205–233. https://doi.org/10.3934/DSFE.2025010',
        'Mozumder, S., Hasan, M. K., & Kabir, M. H. (2024). An evaluation of the adequacy of Lévy and extreme value tail risk estimates. Financial Innovation, 10(1), Article 100. https://doi.org/10.1186/s40854-024-00614-6',
        'Naeem, M., Jassim, H. S., & Korsah, D. (2024). The application of machine learning techniques to predict stock market crises in Africa. Journal of Risk and Financial Management, 17(12), Article 554. https://doi.org/10.3390/jrfm17120554',
        'Nahari, F. (2025). Portfolio optimization in practice: A comparative analysis of the Markowitz and Index models. In M. M. Husin (Ed.), Proceedings of the 2025 International Conference on Financial Risk and Investment Management (ICFRIM 2025), Advances in Economics, Business and Management Research (Vol. 333, pp. 367–375). Atlantis Press.',
        'Nigerian Exchange Group. (2024). Market report and listed securities directory. NGX Group. https://ngxgroup.com',
        'Ojo, A. K., & Okafor, I. J. (2024). Forecasting Nigerian Equity Stock Returns Using Long Short-Term Memory Technique. Journal of Advances in Mathematics and Computer Science, 39(7), 45–54. https://doi.org/10.9734/jamcs/2024/v39i71911',
        'Okafor, C., & Robertson, A. (2023). Maximizing returns: Portfolio optimization in the Nigerian Stock Exchange. International Journal of Advances in Applied Mathematics and Computer Science, 10(2), 14–28. https://americaserial.com/journals/ijaamcs/article/518',
        'Rigamonti, A., & Lučivjanská, K. (2024). Mean-semivariance portfolio optimization using minimum average partial. Annals of Operations Research, 334, 185–203. https://doi.org/10.1007/s10479-022-04736-x',
        'Rockafellar, R. T., & Uryasev, S. (2000). Optimization of conditional value-at-risk. Journal of Risk, 2(3), 21–41. https://doi.org/10.21314/JOR.2000.038',
        'Rockafellar, R. T., & Uryasev, S. (2002). Conditional value-at-risk for general loss distributions. Journal of Banking & Finance, 26(7), 1443–1471. https://doi.org/10.1016/S0378-4266(02)00271-6',
        'Sahiner, M. (2022). Forecasting volatility in Asian financial markets: Evidence from recursive and rolling window methods. SN Business & Economics, 2, Article 157. https://doi.org/10.1007/s43546-022-00329-9',
        'Salo, A., Doumpos, M., Liesiö, J., & Zopounidis, C. (2024). Fifty years of portfolio optimization. European Journal of Operational Research, 318(1), 1–18. https://doi.org/10.1016/j.ejor.2023.12.031',
        'Samaniego Alcántar, A. (2023). Semi-variance optimization for the components of the Dow Jones Industrial Average index. Contaduría y Administración, 68(4), 1–17. http://dx.doi.org/10.22201/fca.24488410e.2023.3409',
        'San, J. (2025). Stock Forecasting and Portfolio Optimization Based on ARIMA-GARCH, Random Forest and Monte Carlo Models. Advances in Economics, Business and Management Research, 333, 582–591. https://doi.org/10.2991/978-94-6463-652-9_61',
        'Senescall, M., & Low, R. K. Y. (2024). Quantitative Portfolio Management: Review and Outlook. Mathematics, 12(18), Article 2897. https://doi.org/10.3390/math12182897',
        'Shapiro, S. S., & Wilk, M. B. (1965). An analysis of variance test for normality (complete samples). Biometrika, 52(3/4), 591–611. https://doi.org/10.2307/2333709',
        'Sharpe, W. F. (1966). Mutual fund performance. The Journal of Business, 39(1), 119–138. https://doi.org/10.1086/294846',
        'Ślusarczyk, D., & Ślepaczuk, R. (2025). Optimal Markowitz portfolio using returns forecasted with time series and machine learning models. Journal of Big Data, 12, Article 127. https://doi.org/10.1186/s40537-025-01164-z',
        'Sortino, F. A., & Price, L. N. (1994). Performance measurement in a downside risk framework. The Journal of Investing, 3(3), 59–64. https://doi.org/10.3905/joi.3.3.59',
        'Sulaiman, L. A., Adejayan, A. O., & Ilori, O. O. (2023). Capital Market Development and Economic Growth of West African Countries. Nigerian Journal of Banking and Financial Issues, 9(1), 117–125.',
        'Tjiwidjaja, H. (2025). Optimization of Investment Portfolio Returns Through an Integrated Risk Management Approach. STIE Ganesha Research Papers, 853–863.',
        'Uzoaga, G. A., Adenomon, M. O., Nweze, N. O., & Maijama, B. (2025a). Modelling and predicting stock prices of Nigerian Stock Exchange using some machine learning techniques and time series model. Science World Journal, 20(2), 510–515. https://dx.doi.org/10.4314/swj.v20i2.9',
        'Uzoaga, G. A., Adenomon, M. O., Nweze, N. O., & Maijamaa, B. (2025b). Predictive machine learning methods for stock returns among emerging economies in Africa. Science World Journal, 20(3), 941–947. https://dx.doi.org/10.4314/swj.v20i3.3',
        'Wahid, A. J., Riaman, & Sukono. (2025). A Systematic Literature Review on Mean-CVaR Based Financial Asset Portfolio Weight Allocation Using K-Means Clustering. CAUCHY – Jurnal Matematika Murni dan Aplikasi, 10(2), 1069–1091. https://doi.org/10.18860/cauchy.v10i2.36590',
        'Wang, T., Pan, Q., Wu, W., Gao, J., & Zhou, K. (2024). Dynamic Mean–Variance Portfolio Optimization with Value-at-Risk Constraint in Continuous Time. Mathematics, 12(14), Article 2268. https://doi.org/10.3390/math12142268',
        'Wilcoxon, F. (1945). Individual comparisons by ranking methods. Biometrics Bulletin, 1(6), 80–83. https://doi.org/10.2307/3001968',
        'Yadav, A., Madhavi, R., Bagaria, O., Ambulkar, A., & Sharma, S. (2024). Survey on financial portfolio management\'s role in investment decision-making strategies. Multidisciplinary Reviews, 6, Article e2023ss101. https://doi.org/10.31893/multirev.2023ss101',
        'Yu, S. (2024). Advancing stock market return forecasting with LSTM models and financial indicators. In Proceedings of the International Conference on Economic Management and Green Development, Advances in Economics, Management and Political Sciences (Vol. 122, pp. 137–144). https://doi.org/10.54254/2754-1169/2024.17734',
        'Zaimovic, A., Arnaut-Berilo, A., & Bešlija, R. (2024). International portfolio diversification benefits: An empirical investigation of the 28 European stock markets. The South East European Journal of Economics and Business, 19(1), 96–112. https://doi.org/10.2478/jeb-2024-0007',
        'Zapata Quimbayo, C., & León, B. (2025). Downside risk measures and ESG factors in optimal portfolio construction: Evidence from European equity markets. Economics - Innovative and Economics Research Journal, 13(4), 5–17. https://doi.org/10.2478/eoik-2025-0082',
        'Zhang, G. (2025). Using machine learning for stock return prediction. Advances in Economics, Management and Political Sciences, 185, 119–126. https://doi.org/10.54254/2754-1169/2025.LH23915',
        'Zhang, Y. (2024). Integrating forecasting and mean-variance portfolio optimization: A machine learning approach. Advances in Economics, Management and Political Sciences, 90, 157–168. https://doi.org/10.54254/2754-1169/90/20242002',
        'Zsurkis, G., Nicolau, J., & Rodrigues, P. M. M. (2024). First passage times in portfolio optimization: A novel nonparametric approach. European Journal of Operational Research, 312(3), 1074–1085. https://doi.org/10.1016/j.ejor.2023.07.044',
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
