# Quantitative Equity Return Forecasting & Tail-Risk-Aware Portfolio Optimization on the Nigerian Exchange Group (NGX)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Managed with uv](https://img.shields.io/badge/managed_with-uv-purple.svg)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end empirical quantitative finance pipeline implementing Machine Learning (Random Forest & XGBoost) return forecasting under **Expanding Rolling Window Walk-Forward Validation** and **Convex Tail-Risk (Mean-CVaR at $\alpha=0.95$)** portfolio optimization across 28 liquid equities on the Nigerian Exchange Group (NGX) spanning 15 years of weekly data (2010–2025).

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
4. **Convex Mean-CVaR Portfolio Optimization & Backtesting** (`src/portfolio_optimization.py`)
5. **Academic ReportLab Chapters 4 & 5 PDF Generation** (`src/generate_chapters.py`)
6. **Consolidated 66-Page Thesis PDF Compilation** (`generate_thesis_pdf.py`)

---

## 📌 Methodological Hardening & Purity Standards

1. **Zero Data Leakage**: Feature scaling (`MinMaxScaler`) is fit strictly inside the expanding training window loop in `src/ml_models.py`, preventing future test bounds (2021–2025) from leaking into feature normalization.
2. **Wilder's Parabolic SAR Iterative Algorithm**: Implemented Welles Wilder's true iterative SAR algorithm incorporating acceleration factors ($AF \in [0.02, 0.20]$) and trend flip logic instead of EMA approximations.
3. **Chronological Hyperparameter Tuning**: Evaluated 5-fold `TimeSeriesSplit` cross-validation on initial 2010–2020 training data to tune tree depth and ensemble size without temporal shuffling.
4. **ReportLab Math Markup**: All mathematical expressions in generated PDF chapters use native ReportLab HTML formatting (`CVaR<sub>0.95</sub>`), eliminating raw LaTeX syntax bugs.

---

## 🏛️ Asset Universe Breakdown (NGX Pension Index)

A total of **38 NGX Pension Index constituent equities** were audited. To maintain sample balance across a 15-year historical horizon (835 weekly observations from 2010 to 2025) without introducing survivorship bias, look-ahead bias, or synthetic data imputation:
- **28 Equities Included**: Complete 15-year weekly trading dataset from January 2010 through December 2025 (*CONOIL, CUSTODIAN, DANGCEM, DANGSUGAR, ETI, FCMB, FIDELITYBK, FIDSON, FBNH, GTCO, GUINNESS, JBERGER, WAPCO, MANSARD, NAHCO, NASCON, NESTLE, NB, OKOMUOIL, PRESCO, STANBIC, STERLINGNG, TRANSCORP, UACN, UBA, UNILEVER, WEMABANK, ZENITHBANK*).
- **10 Equities Excluded**: Equities listed post-2010 (*Access Holdings, Airtel Africa, Aradel Holdings, BUA Foods, Geregu Power, MTN Nigeria, Seplat Energy, Transcorp Hotels, Transcorp Power, United Capital*) were excluded due to short historical windows (< 15 years).

---

## 📊 Out-of-Sample Portfolio Performance Sensitivity (2021–2025)

### Table 4.4: Performance with 0.75% Retail Transaction Fees

| Strategy | Annualized Return (%) | Annualized Volatility (%) | Sharpe Ratio | Sortino Ratio | VaR (95%) (%) | CVaR (95%) (%) | Max Drawdown (%) | Avg Weekly Turnover (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **RF-CVaR** | **38.33%** | **16.09%** | **1.26** | **2.42** | **-2.20%** | **-2.93%** | **-22.38%** | **7.59%** |
| **XGB-CVaR** | **37.71%** | **15.85%** | **1.24** | **2.37** | **-2.32%** | **-2.85%** | **-23.62%** | **11.00%** |
| **Historical-CVaR** | 42.12% | 16.15% | 1.49 | 3.02 | -2.18% | -2.61% | -21.96% | 0.38% |
| **Markowitz (MVO)** | 18.24% | 53.87% | 0.00 | 0.01 | -9.58% | -16.24% | -71.07% | 99.28% |
| **1/N Equal Weight** | 37.42% | 18.29% | 1.06 | 1.83 | -2.82% | -4.44% | -23.95% | 0.38% |
| **NGX Index Buy-Hold**| 37.42% | 18.29% | 1.06 | 1.83 | -2.82% | -4.44% | -23.95% | 0.38% |

---

### Table 4.5: Gross Performance (Zero Transaction Costs)

| Strategy | Annualized Return (%) | Annualized Volatility (%) | Sharpe Ratio | Sortino Ratio | VaR (95%) (%) | CVaR (95%) (%) | Max Drawdown (%) | Avg Weekly Turnover (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **XGB-CVaR** | **42.00%** | **15.75%** | **1.52** | **3.06** | **-2.18%** | **-2.58%** | **-22.09%** | **11.00%** |
| **RF-CVaR** | **41.29%** | **16.05%** | **1.45** | **2.87** | **-2.18%** | **-2.78%** | **-22.01%** | **7.59%** |
| **Historical-CVaR** | 42.27% | 16.16% | 1.50 | 3.04 | -2.18% | -2.61% | -21.96% | 0.38% |
| **Markowitz (MVO)** | 56.97% | 54.18% | 0.72 | 1.25 | -8.83% | -15.38% | -53.51% | 99.28% |
| **1/N Equal Weight** | 37.57% | 18.31% | 1.07 | 1.84 | -2.82% | -4.44% | -23.95% | 0.38% |
| **NGX Index Buy-Hold**| 37.57% | 18.31% | 1.07 | 1.84 | -2.82% | -4.44% | -23.95% | 0.38% |

*Notes: Risk-Free Rate = 0.319% weekly (18.00% annualized CBN 91-day T-Bill rate).*

---

## 🛠️ Project Structure

```text
equity-optimization/
├── main.py                                    # Master execution entry point (Runs all 6 pipeline stages)
├── Abdulameen Chapter 1 -3.pdf                # Original Chapters 1-3 PDF (Preserved untouched)
├── Abdulameen_Complete_Thesis_Chapters_1_5.pdf # Consolidated 66-Page Academic Thesis Document
├── categorize_data.py                         # Data categorization script (2010 cutoff)
├── generate_thesis_pdf.py                     # Final PDF synthesis and merger script
├── README.md                                  # Comprehensive project documentation
├── data/
│   ├── valid_from_2010/                       # 28 valid stock CSVs (complete 2010-2025 data)
│   └── excluded_post_2010/                    # 10 excluded post-2010 listed stock CSVs
├── src/
│   ├── data_processing.py                     # Parsing, missing data imputation, JB/ADF tests, correlation
│   ├── feature_engineering.py                 # 13 technical indicators, Wilder SAR, warm-up handling
│   ├── ml_models.py                           # TimeSeriesSplit CV, train-only scaling walk-forward ML models
│   ├── portfolio_optimization.py              # Mean-CVaR LP solver & sensitivity backtester (Retail & Gross)
│   └── generate_chapters.py                   # ReportLab academic PDF builder for Chapters 4 & 5
└── output/
    ├── figures/                               # Heatmap, Feature Importance, Equity Growth Curves
    ├── tables/                                # Empirical results CSV tables (Stats, ML Perf, Portfolios)
    └── pdf/                                   # Standalone Chapters 4 & 5 PDF output
```

