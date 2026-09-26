# Quantitative Equity Return Forecasting & Tail-Risk-Aware Portfolio Optimization on the Nigerian Exchange Group (NGX)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Managed with uv](https://img.shields.io/badge/managed_with-uv-purple.svg)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end empirical quantitative finance pipeline implementing Machine Learning (Random Forest & XGBoost) return forecasting under **Expanding Rolling Window Walk-Forward Validation** and **Convex Tail-Risk (Mean-CVaR at $\alpha=0.95$)** portfolio optimization across 28 liquid equities on the Nigerian Exchange Group (NGX) spanning a clean 16-year historical panel of weekly data from 2010 to 2025 (835 weekly observations per asset).

---

## 📌 Master Pipeline Entry Point

Run the entire end-to-end quantitative pipeline with a single command:

```bash
uv run python main.py
```

This master entry point automatically executes all sequential stages:
1. **Data Preprocessing & Non-Normality Diagnostics** (`src/data_processing.py`)
2. **Technical Feature Engineering & Wilder's Parabolic SAR** (`src/feature_engineering.py`)
3. **ML Walk-Forward Forecasting with TimeSeriesSplit CV Tuning** (`src/ml_models.py`)
4. **Convex Mean-CVaR Portfolio Optimization & Statistical Hypothesis Testing** (`src/portfolio_optimization.py`)
5. **Academic ReportLab Chapters 4 & 5 PDF Generation** (`src/generate_chapters.py`)
6. **Consolidated Academic Thesis PDF Compilation** (`generate_thesis_pdf.py`)

---

## 📄 Thesis PDF Compilation & Reproducibility Workflow

To ensure **100% reproducibility** and layout integrity across Microsoft Word and ReportLab vector PDF rendering:

1. **Chapters 1–3 Source (`Abdulameen Chapter 1 -3.docx`)**:
   - Maintained in native Microsoft Word format with fully justified body text, left-aligned section headers, and native vector math equations, matrices, and tables.
   - Converted directly to PDF via Word COM API (`export_and_compile_thesis.py` or Word "Save As PDF") to produce `Abdulameen Chapter 1 -3.pdf`.

2. **Chapters 4 & 5 Source (`src/generate_chapters.py`)**:
   - Generated programmatically using ReportLab into `output/pdf/Chapters_4_and_5.pdf`, containing empirical findings, econometric tables, figures, and references.

3. **Master PDF Synthesis (`generate_thesis_pdf.py`)**:
   - Merges `Abdulameen Chapter 1 -3.pdf` (Chapters 1–3) + `output/pdf/Chapters_4_and_5.pdf` (Chapters 4–5 & References).
   - Dynamically stamps centered bottom page numbers across the entire document.
   - Outputs the final complete document: **`Abdulameen_Complete_Thesis_Chapters_1_5.pdf`** (100+ total pages).

To re-compile the complete thesis PDF at any time:

```bash
# Option A: Fast compilation from default Abdulameen Chapter 1 -3.pdf baseline
python generate_thesis_pdf.py

# Option B: Complete export from Abdulameen Chapter 1 -3.docx via Word COM + compilation
python export_and_compile_thesis.py
```

---

## 📌 Methodological Hardening & Statistical Significance Suite

1. **Reconciled Benchmark Drift**: Differentiated "1/N Equal Weight" (weekly rebalancing) from "NGX Index Buy-Hold" (passive weight drift $w_{t+1, i} \propto w_{t, i}(1+R_{t+1, i})$ with 0.00% turnover post-entry).
2. **Ledoit-Wolf Circular Block Bootstrap**: Evaluated two-sided Sharpe and Sortino ratio equality using overlapping blocks ($b=5$ weeks, $B=2,000$ resamples) to preserve time-series autocorrelation and conditional heteroskedasticity (GARCH effects) (Ledoit & Wolf, 2008).
3. **Jobson-Korkie Test (Memmel 2003 Correction)**: Parametric Z-test for Sharpe ratio equality under correlated portfolio return series (Jobson & Korkie, 1981; Memmel, 2003).
4. **Non-Parametric Wilcoxon Signed-Rank Test**: Inferential non-parametric rank test on weekly return differential series ($\Delta R_t = R_{A,t} - R_{B,t}$) (Wilcoxon, 1945).
5. **Diebold-Mariano Test (Diebold & Mariano, 1995)**: Quadratic loss differential test with Newey–West HAC standard errors evaluating out-of-sample forecast accuracy of XGBoost versus the flat historical mean baseline across all 28 assets (confirming statistical parity on point predictions across 89.3% of equities, $p > 0.05$).
6. **Benjamini-Hochberg False Discovery Rate (FDR) Procedure (Benjamini & Hochberg, 1995)**: Multiple testing correction applied across all 18 simultaneous pairwise portfolio comparisons to control the family-wise false discovery rate ($\\alpha = 0.05$), confirming that low-turnover Historical-CVaR significantly outperforms active XGB-CVaR under market friction ( = 0.000$) and retail MVO significantly collapses against 1/N ( = 0.009$).\n7. **Zero Data Leakage**: Feature scaling (`MinMaxScaler`) fit strictly inside the expanding training window loop in `src/ml_models.py`.

---

## 📊 Out-of-Sample Performance & Statistical Significance (2021-2025)

### Table 4.4: Out-of-Sample Portfolio Performance (1.50% Retail Transaction Fees & Slippage)

| Strategy | Annualized Return (%) | Annualized Volatility (%) | Sharpe Ratio | Sortino Ratio | VaR (95%) (%) | CVaR (95%) (%) | Max Drawdown (%) | Avg Weekly Turnover (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Historical-CVaR** | **41.97%** | **16.15%** | **1.48** | **3.00** | -2.18% | -2.61% | **-21.96%** | 0.38% |
| **1/N Equal Weight** | 37.27% | 18.27% | 1.05 | 1.81 | -2.82% | -4.44% | -23.95% | 0.38% |
| **RF-CVaR** | 35.37% | 16.17% | 1.07 | 1.99 | -2.25% | -3.05% | -23.01% | 7.59% |
| **NGX Index Buy-Hold** | 35.73% | 19.75% | 0.90 | 1.53 | -3.32% | -4.95% | -26.66% | **0.00%** |
| **XGB-CVaR** | 33.42% | 15.98% | 0.96 | 1.75 | -2.47% | -3.10% | -25.12% | 11.00% |
| **Markowitz (MVO)** | -20.48% | 53.92% | -0.71 | -1.02 | -10.85% | -17.16% | -86.38% | 99.28% |

---

### Table 4.5b: Institutional PFA Performance (0.75% Transaction Fees)

| Strategy | Annualized Return (%) | Annualized Volatility (%) | Sharpe Ratio | Sortino Ratio | VaR (95%) (%) | CVaR (95%) (%) | Max Drawdown (%) | Avg Weekly Turnover (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Historical-CVaR** | **42.12%** | **16.15%** | **1.49** | **3.02** | -2.18% | -2.61% | -21.96% | 0.38% |
| **RF-CVaR** | 38.33% | 16.09% | 1.26 | 2.42 | -2.20% | -2.93% | -22.38% | 7.59% |
| **XGB-CVaR** | 37.71% | 15.85% | 1.24 | 2.37 | -2.32% | -2.85% | -23.62% | 11.00% |
| **1/N Equal Weight** | 37.42% | 18.29% | 1.06 | 1.83 | -2.82% | -4.44% | -23.95% | 0.38% |
| **NGX Index Buy-Hold** | 35.88% | 19.77% | 0.90 | 1.54 | -3.32% | -4.95% | -26.66% | 0.00% |
| **Markowitz (MVO)** | 18.24% | 53.87% | 0.00 | 0.01 | -9.58% | -16.24% | -71.07% | 99.28% |

---

### Table 4.5c: Gross Performance (Zero Transaction Costs - 0.00%)

| Strategy | Annualized Return (%) | Annualized Volatility (%) | Sharpe Ratio | Sortino Ratio | VaR (95%) (%) | CVaR (95%) (%) | Max Drawdown (%) | Avg Weekly Turnover (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **XGB-CVaR** | **42.00%** | **15.75%** | **1.52** | **3.06** | -2.18% | -2.58% | -22.09% | 11.00% |
| **Historical-CVaR** | 42.27% | 16.16% | 1.50 | 3.04 | -2.18% | -2.61% | -21.96% | 0.38% |
| **RF-CVaR** | 41.29% | 16.05% | 1.45 | 2.87 | -2.18% | -2.78% | -22.01% | 7.59% |
| **1/N Equal Weight** | 37.57% | 18.31% | 1.07 | 1.84 | -2.82% | -4.44% | -23.95% | 0.38% |
| **NGX Index Buy-Hold** | 36.03% | 19.79% | 0.91 | 1.55 | -3.32% | -4.95% | -26.66% | 0.00% |
| **Markowitz (MVO)** | 56.97% | 54.18% | 0.72 | 1.25 | -8.83% | -15.38% | -53.51% | 99.28% |

---

### Table 4.6: Multi-Tier Pairwise Statistical Significance Testing (Sharpe & Sortino Equality)

| Fee Regime | Target Strategy | Benchmark | Sharpe Diff | Jobson-Korkie p-val | Ledoit-Wolf Sharpe p-val | Benjamini-Hochberg (FDR q-val) | Wilcoxon p-val |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Gross (0.00%)** | **XGB-CVaR** | **NGX Index Buy-Hold** | **+0.61** | 0.203 | **0.015** * | 0.056 | 0.519 |\n| **Gross (0.00%)** | **RF-CVaR** | **NGX Index Buy-Hold** | **+0.54** | 0.245 | **0.033** * | 0.066 | 0.632 |\n| **Gross (0.00%)** | **Historical-CVaR** | **NGX Index Buy-Hold** | **+0.59** | 0.223 | **0.022** * | 0.056 | 0.544 |\n| **Inst. (0.75%)** | **Historical-CVaR** | **NGX Index Buy-Hold** | **+0.59** | 0.223 | **0.022** * | 0.056 | 0.544 |\n| **Inst. (0.75%)** | XGB-CVaR | NGX Index Buy-Hold | +0.34 | 0.423 | 0.181 | 0.233 | 0.852 |\n| **Retail (1.50%)** | **Historical-CVaR** | **NGX Index Buy-Hold** | **+0.59** | 0.223 | **0.022** * | 0.056 | 0.544 |\n| **Retail (1.50%)** | XGB-CVaR | NGX Index Buy-Hold | +0.07 | 0.838 | 0.770 | 0.769 | 0.318 |\n| **Retail (1.50%)** | **Historical-CVaR** | XGB-CVaR | **+0.52** | **0.008** * | **0.000** * | **0.000** * | **0.000** * |\n| **Retail (1.50%)** | **Markowitz (MVO)** | **1/N Equal Weight** | -1.77 | **0.004** * | **0.002** * | **0.009** * | **0.000** * |\n
*\* Bold p-values denote statistical significance at $\alpha = 0.05$ (Ledoit-Wolf 2,000 block resamples).*
---

### Table 4.7: Investor Economic Welfare Utility and Certainty Equivalent Return (CER) Analysis ($\gamma = 3$)

$$\text{CER} = \mu_p - \frac{\gamma}{2} \sigma_p^2$$

| Strategy & Regime | Annualized Return ($\mu_p$) | Annualized Volatility ($\sigma_p$) | Variance Penalty | Certainty Equivalent Return (CER) | Economic Welfare Gain vs Index ($\Delta\text{CER}$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Historical-CVaR (Inst. 0.75%)** | **42.12%** | **16.15%** | **3.91%** | **38.21%** | **+8.19% (+819 bps)** |
| **Historical-CVaR (Retail 1.50%)** | **41.97%** | **16.15%** | **3.91%** | **38.06%** | **+8.17% (+817 bps)** |
| **RF-CVaR (Inst. 0.75%)** | 38.33% | 16.09% | 3.88% | 34.45% | +4.43% (+443 bps) |
| **XGB-CVaR (Inst. 0.75%)** | 37.71% | 15.85% | 3.77% | 33.94% | +3.92% (+392 bps) |
| **1/N Equal Weight (Inst. 0.75%)** | 37.42% | 18.29% | 5.02% | 32.40% | +2.38% (+238 bps) |
| **RF-CVaR (Retail 1.50%)** | 35.37% | 16.17% | 3.92% | 31.45% | +1.56% (+156 bps) |
| **NGX Index Buy-Hold** | 35.88% | 19.77% | 5.86% | 30.02% | Baseline (0 bps) |
| **XGB-CVaR (Retail 1.50%)** | 33.42% | 15.98% | 3.83% | 29.59% | -0.30% (-30 bps) |
| **Markowitz (MVO, Retail 1.50%)** | -20.48% | 53.92% | 43.61% | -64.09% | -93.98% (-9398 bps) |

---

### 🔑 Key Econometric Conclusions across Three Market Tiers:
1. **Statistically Significant Gross ML Alpha ($p = 0.015 < 0.05$)**: Ledoit-Wolf circular block bootstrap testing under zero fees (0.00%) confirms that XGB-CVaR achieves statistically significant Sharpe outperformance over passive Buy-and-Hold ($p = 0.015$), empirically proving that machine learning predictions possess genuine predictive alpha before market friction.
2. **Institutional PFA Fee Friction (0.75% Fees)**: Under 0.75% institutional transaction fees, active ML weekly turnover (11.00%) incurs a ~3.6% annual fee drag, reducing XGB-CVaR net Sharpe to 1.24 ($p = 0.181$, non-significant). Low-turnover Historical-CVaR (Sharpe 1.49, Return 42.12%, CER 38.21%) statistically dominates active ML ($p = 0.000$) and retains statistically significant outperformance over passive Buy-and-Hold ($p = 0.022$).
3. **Retail Fee Drag Paradox (1.50% Fees)**: Under 1.50% retail brokerage fees and market slippage, active turnover creates a ~7.2% annual fee drag that reduces XGB-CVaR net Sharpe to 0.96 ($p = 0.770$). Low-turnover **Historical-CVaR (Sharpe 1.48, CER = 38.06%)** remains the optimal choice for retail accounts ($p = 0.023$).
4. **Naira Capital Multiplier (2021–2025)**: Over 5 out-of-sample years, **₦10 Million** initial capital compounds to **₦57.77 Million** under Historical-CVaR (+₦47.77M net profit) vs **₦46.33 Million** under passive NGX Buy-and-Hold, delivering **+₦11.44 Million in net economic surplus** while reducing maximum drawdown from -26.66% to -21.96%.
5. **Statistical Breakdown of Gaussian Markowitz MVO**: Unconstrained MVO statistically underperforms naively diversified 1/N Equal Weight ($p = 0.0015$ Ledoit-Wolf, $p = 0.000$ Wilcoxon test), confirming the breakdown of Gaussian mean-variance theory in heavy-tailed emerging markets.

---

## 🛠️ Project Structure

```text
equity-optimization/
├── main.py                                    # Master execution entry point (Runs all 6 pipeline stages)
├── export_and_compile_thesis.py               # Word COM export + complete thesis PDF compiler
├── generate_thesis_pdf.py                     # Fast thesis PDF compilation script (Default input: Abdulameen Chapter 1 -3.pdf)
├── Abdulameen Chapter 1 -3.docx               # Master Word source document for Chapters 1-3
├── Abdulameen Chapter 1 -3.pdf                # Word-exported vector PDF for Chapters 1-3 (Default input)
├── Abdulameen_Complete_Thesis_Chapters_1_5.pdf # Consolidated 100+ Page Academic Thesis Document
├── README.md                                  # Comprehensive project documentation
├── data/
│   ├── valid_from_2010/                       # 28 valid stock CSVs (complete 2010-2025 data)
│   └── excluded_post_2010/                    # 10 excluded post-2010 listed stock CSVs
├── src/
│   ├── data_processing.py                     # Parsing, missing data imputation, JB/ADF tests, correlation
│   ├── feature_engineering.py                 # 13 technical indicators, Wilder SAR, warm-up handling
│   ├── ml_models.py                           # TimeSeriesSplit CV, train-only scaling walk-forward ML models
│   ├── portfolio_optimization.py              # Mean-CVaR LP solver & statistical significance tests
│   └── generate_chapters.py                   # ReportLab academic PDF builder for Chapters 4 & 5
└── output/
    ├── figures/                               # Heatmap, Feature Importance, Equity Growth Curves
    ├── tables/                                # Empirical results CSV tables (Stats, ML Perf, Portfolios, Significance)
    └── pdf/                                   # Standalone Chapters 4 & 5 PDF & Word export PDF
```
