# Quantitative Equity Return Forecasting & Tail-Risk-Aware Portfolio Optimization on the Nigerian Exchange Group (NGX)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Managed with uv](https://img.shields.io/badge/managed_with-uv-purple.svg)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end empirical quantitative finance pipeline implementing Machine Learning (Random Forest & XGBoost) return forecasting under **Expanding Rolling Window Walk-Forward Validation** and **Convex Tail-Risk (Mean-CVaR at $\alpha=0.95$)** portfolio optimization across 28 liquid equities on the Nigerian Exchange Group (NGX) spanning 15 years of weekly data (2010-2025).

---

## 📌 Master Pipeline Entry Point

Run the entire end-to-end quantitative pipeline with a single command:

```bash
uv run python main.py
```

This master entry point automatically executes all 6 sequential stages:
1. **Data Preprocessing & Non-Normality Diagnostics** (`src/data_processing.py`)
2. **Technical Feature Engineering & Wilder's Parabolic SAR** (`src/feature_engineering.py`)
3. **ML Walk-Forward Forecasting with TimeSeriesSplit CV Tuning** (`src/ml_models.py`)
4. **Convex Mean-CVaR Portfolio Optimization & Statistical Hypothesis Testing** (`src/portfolio_optimization.py`)
5. **Academic ReportLab Chapters 4 & 5 PDF Generation** (`src/generate_chapters.py`)
6. **Consolidated 69-Page Thesis PDF Compilation** (`generate_thesis_pdf.py`)

---

## 📌 Methodological Hardening & Statistical Significance Suite

1. **Reconciled Benchmark Drift**: Differentiated "1/N Equal Weight" (weekly rebalancing) from "NGX Index Buy-Hold" (passive weight drift $w_{t+1, i} \propto w_{t, i}(1+R_{t+1, i})$ with 0.00% turnover post-entry).
2. **Ledoit-Wolf Circular Block Bootstrap**: Evaluated two-sided Sharpe and Sortino ratio equality using overlapping blocks ($b=5$ weeks, $B=2,000$ resamples) to preserve time-series autocorrelation and conditional heteroskedasticity (GARCH effects).
3. **Jobson-Korkie Test (Memmel 2007 Correction)**: Parametric Z-test for Sharpe ratio equality under correlated portfolio return series.
4. **Non-Parametric Wilcoxon & Paired t-Tests**: Inferential test on weekly return differential series ($\Delta R_t = R_{A,t} - R_{B,t}$).
5. **Diebold-Mariano Test**: Loss differential test evaluating out-of-sample forecast RMSE accuracy against the historical mean baseline.
6. **Zero Data Leakage**: Feature scaling (`MinMaxScaler`) fit strictly inside the expanding training window loop in `src/ml_models.py`.

---

## 📊 Out-of-Sample Performance & Statistical Significance (2021-2025)

### Table 4.4: Out-of-Sample Portfolio Performance (0.75% Retail Transaction Fees)

| Strategy | Annualized Return (%) | Annualized Volatility (%) | Sharpe Ratio | Sortino Ratio | VaR (95%) (%) | CVaR (95%) (%) | Max Drawdown (%) | Avg Weekly Turnover (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Historical-CVaR** | **42.12%** | **16.15%** | **1.49** | **3.02** | -2.18% | -2.61% | **-21.96%** | 0.38% |
| **RF-CVaR** | 38.33% | 16.09% | 1.26 | 2.42 | -2.20% | -2.93% | -22.38% | 7.59% |
| **XGB-CVaR** | 37.71% | 15.85% | 1.24 | 2.37 | -2.32% | -2.85% | -23.62% | 11.00% |
| **1/N Equal Weight** | 37.42% | 18.29% | 1.06 | 1.83 | -2.82% | -4.44% | -23.95% | 0.38% |
| **NGX Index Buy-Hold** | 35.88% | 19.77% | 0.90 | 1.54 | -3.32% | -4.95% | -26.66% | **0.00%** |
| **Markowitz (MVO)** | 18.24% | 53.87% | 0.00 | 0.01 | -9.58% | -16.24% | -71.07% | 99.28% |

---

### Table 4.5: Gross Performance (Zero Transaction Costs)

| Strategy | Annualized Return (%) | Annualized Volatility (%) | Sharpe Ratio | Sortino Ratio | VaR (95%) (%) | CVaR (95%) (%) | Max Drawdown (%) | Avg Weekly Turnover (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **XGB-CVaR** | **42.00%** | **15.75%** | **1.52** | **3.06** | -2.18% | -2.58% | -22.09% | 11.00% |
| **RF-CVaR** | 41.29% | 16.05% | 1.45 | 2.87 | -2.18% | -2.78% | -22.01% | 7.59% |
| **Historical-CVaR** | 42.27% | 16.16% | 1.50 | 3.04 | -2.18% | -2.61% | -21.96% | 0.38% |
| **Markowitz (MVO)** | 56.97% | 54.18% | 0.72 | 1.25 | -8.83% | -15.38% | -53.51% | 99.28% |
| **1/N Equal Weight** | 37.57% | 18.31% | 1.07 | 1.84 | -2.82% | -4.44% | -23.95% | 0.38% |
| **NGX Index Buy-Hold** | 35.88% | 19.77% | 0.90 | 1.54 | -3.32% | -4.95% | -26.66% | 0.00% |

---

### Table 4.6: Pairwise Statistical Significance Testing (Sharpe & Sortino Equality)

| Target Strategy | Benchmark | Sharpe Diff | Jobson-Korkie p-val | Ledoit-Wolf Sharpe p-val | Ledoit-Wolf Sortino p-val | Wilcoxon p-val |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Historical-CVaR** | **NGX Index Buy-Hold** | **+0.605** | 0.223 | **0.022** * | **0.033** * | 0.544 |
| **Historical-CVaR** | **1/N Equal Weight** | **+0.442** | 0.356 | **0.085** | **0.066** | 0.344 |
| **RF-CVaR** | NGX Index Buy-Hold | +0.375 | 0.399 | 0.165 | 0.165 | 0.949 |
| **XGB-CVaR** | NGX Index Buy-Hold | +0.357 | 0.423 | 0.181 | 0.183 | 0.852 |
| **Markowitz (MVO)** | **1/N Equal Weight** | -1.109 | **0.048** * | **0.025** * | **0.056** | **0.008** * |

*\* Bold values denote statistical significance at $\alpha = 0.05$.*

---

### Table 4.7: Investor Economic Welfare Utility and Certainty Equivalent Return (CER) Analysis ($\gamma = 3$)

$$\text{CER} = \mu_p - \frac{\gamma}{2} \sigma_p^2$$

| Strategy | Annualized Return ($\mu_p$) | Annualized Volatility ($\sigma_p$) | Variance Penalty | Certainty Equivalent Return (CER) | Economic Welfare Gain vs Index ($\Delta\text{CER}$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Historical-CVaR (Net)** | **42.12%** | **16.15%** | **3.91%** | **38.21%** | **+8.19% (+819 bps)** |
| **RF-CVaR (Net)** | 38.33% | 16.09% | 3.88% | 34.45% | +4.43% (+443 bps) |
| **XGB-CVaR (Net)** | 37.71% | 15.85% | 3.77% | 33.94% | +3.92% (+392 bps) |
| **1/N Equal Weight** | 37.42% | 18.29% | 5.02% | 32.40% | +2.38% (+238 bps) |
| **NGX Index Buy-Hold** | 35.88% | 19.77% | 5.86% | 30.02% | Baseline (0 bps) |
| **Markowitz (MVO)** | 18.24% | 53.87% | 43.53% | -25.29% | -55.31% (-5531 bps) |

### 🔑 Key Econometric Conclusions:
1. **Historical-CVaR Statistically Outperforms Passive Buy-and-Hold**: Ledoit-Wolf circular block bootstrap confirms statistically significant Sharpe outperformance ($p = 0.022 < 0.05$) and Sortino outperformance ($p = 0.033 < 0.05$).
2. **Economic Welfare Gains ($\Delta CER = +819 \text{ bps}$)**: Transitioning from passive NGX Index Buy-and-Hold to Historical-CVaR yields an annual certainty-equivalent welfare gain of **+8.19% (819 bps)**. An investor would be willing to pay up to 8.19% annually in management fees before becoming economically indifferent to active tail-risk management.
3. **Naira Wealth Multiplier**: An initial investment of **₦10 Million** grows to **₦57.77 Million** under Historical-CVaR vs **₦46.33 Million** under passive NGX Buy-and-Hold, delivering **+₦11.44 Million in net economic surplus per ₦10M invested** while reducing maximum drawdown from -26.66% to -21.96%.
4. **Statistical Failure of Gaussian Markowitz MVO**: Unconstrained Mean-Variance Optimization statistically underperforms naively diversified 1/N Equal Weight ($p = 0.025$ Ledoit-Wolf Sharpe, $p = 0.008$ Wilcoxon test), resulting in a catastrophic welfare loss ($\text{CER} = -25.29\%$).

---

## 🛠️ Project Structure

```text
equity-optimization/
├── main.py                                    # Master execution entry point (Runs all 6 pipeline stages)
├── Abdulameen Chapter 1 -3.pdf                # Original Chapters 1-3 PDF (Preserved untouched)
├── Abdulameen_Complete_Thesis_Chapters_1_5.pdf # Consolidated 69-Page Academic Thesis Document
├── generate_thesis_pdf.py                     # Final PDF synthesis and merger script
├── README.md                                  # Comprehensive project documentation
├── data/
│   ├── valid_from_2010/                       # 28 valid stock CSVs (complete 2010-2025 data)
│   └── excluded_post_2010/                    # 10 excluded post-2010 listed stock CSVs
├── src/
│   ├── data_processing.py                     # Parsing, missing data imputation, JB/ADF tests, correlation
│   ├── feature_engineering.py                 # 13 technical indicators, Wilder SAR, warm-up handling
│   ├── ml_models.py                           # TimeSeriesSplit CV, train-only scaling walk-forward ML models
│   ├── portfolio_optimization.py              # Mean-CVaR LP solver & statistical significance tests
│   ├── generate_section_3_3_6.py              # Standalone Section 3.3.6 PDF page builder
│   └── generate_chapters.py                   # ReportLab academic PDF builder for Chapters 4 & 5
└── output/
    ├── figures/                               # Heatmap, Feature Importance, Equity Growth Curves
    ├── tables/                                # Empirical results CSV tables (Stats, ML Perf, Portfolios, Significance)
    └── pdf/                                   # Standalone Chapters 4 & 5 PDF & Section 3.3.6 PDF
```
