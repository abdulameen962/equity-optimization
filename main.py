"""
Master Entry Point for Quantitative Equity Return Forecasting & 
Tail-Risk-Aware Portfolio Optimization on the Nigerian Exchange Group (NGX).

Executes the full end-to-end quantitative pipeline:
1. Data Preprocessing & Non-Normality Diagnostics
2. Technical Feature Engineering (with true Wilder Parabolic SAR)
3. ML Forecasting (TimeSeriesSplit CV tuning & train-only scaling walk-forward)
4. Mean-CVaR Portfolio Optimization & Sensitivity Backtesting
5. Academic Thesis PDF Chapters 4 & 5 Generation
6. Consolidated Thesis Document Compilation (Chapters 1-5 PDF)
"""

import sys
import os
import time

def run_pipeline():
    start_time = time.time()
    print("==================================================================")
    print("      QUANTITATIVE EQUITY OPTIMIZATION PIPELINE (NGX 2010-2025)    ")
    print("==================================================================\n")
    
    # 1. Data Preprocessing
    print("--- [STEP 1/6] Running Data Preprocessing & Diagnostics ---")
    from src.data_processing import process_all_data
    process_all_data()
    print("[OK] Step 1 Complete: Data cleaned, JB/SW/ADF tests & correlation computed.\n")
    
    # 2. Feature Engineering
    print("--- [STEP 2/6] Running Feature Engineering (Wilder's Parabolic SAR) ---")
    from src.feature_engineering import generate_all_features
    generate_all_features()
    print("[OK] Step 2 Complete: 13 technical indicators built & 30-week warm-up dropped.\n")
    
    # 3. Machine Learning Forecasting
    print("--- [STEP 3/6] Running ML Forecasting (TimeSeriesSplit CV & Walk-Forward) ---")
    from src.ml_models import train_and_evaluate_ml_models_walk_forward
    train_and_evaluate_ml_models_walk_forward()
    print("[OK] Step 3 Complete: RF & XGBoost models trained with zero test leakage.\n")
    
    # 4. Portfolio Optimization & Backtesting
    print("--- [STEP 4/6] Running Mean-CVaR Portfolio Backtesting (Retail & Gross) ---")
    from src.portfolio_optimization import run_portfolio_backtests
    run_portfolio_backtests()
    print("[OK] Step 4 Complete: Portfolio optimization backtests executed across fee regimes.\n")
    
    # 5. Academic Chapters 4 & 5 Generation
    print("--- [STEP 5/6] Generating Academic Chapters 4 & 5 PDF ---")
    from src.generate_chapters import generate_chapters_pdf
    generate_chapters_pdf()
    print("[OK] Step 5 Complete: Standalone Chapters 4 & 5 PDF generated.\n")
    
    # 6. Consolidated PDF Merger
    print("--- [STEP 6/6] Merging Chapters 1-3 with Chapters 4 & 5 ---")
    from generate_thesis_pdf import compile_complete_thesis_pdf
    compile_complete_thesis_pdf()
    print("[OK] Step 6 Complete: Consolidated Thesis PDF generated successfully.\n")
    
    elapsed = time.time() - start_time
    print("==================================================================")
    print(f" SUCCESS: Complete Pipeline Execution Finished in {elapsed/60:.2f} minutes!")
    print(" Final Thesis Output: Abdulameen_Complete_Thesis_Chapters_1_5.pdf")
    print("==================================================================")

if __name__ == '__main__':
    run_pipeline()
