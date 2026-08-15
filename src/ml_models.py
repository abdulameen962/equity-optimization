import os
import sys
sys.path.insert(0, '.')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from xgboost import XGBRegressor

from src.feature_engineering import generate_all_features

os.makedirs('output/tables', exist_ok=True)
os.makedirs('output/figures', exist_ok=True)

def tune_hyperparameters_time_series(master_feat, feature_cols, train_end_date='2020-12-31'):
    """
    Performs TimeSeriesSplit (5-fold) cross-validation on initial training data (2010-2020)
    to tune Random Forest and XGBoost hyperparameters chronologically without temporal leakage.
    """
    print("Performing TimeSeriesSplit (5-Fold) Hyperparameter Tuning on initial training set (2010-2020)...")
    
    # Pool training samples across assets up to train_end_date
    X_list, y_list = [], []
    for ticker, df in master_feat.items():
        train_df = df[df.index <= train_end_date]
        if len(train_df) > 0:
            X_list.append(train_df[feature_cols].values)
            y_list.append(train_df['Target_Return'].values)
            
    X_pool = np.vstack(X_list)
    y_pool = np.concatenate(y_list)
    
    # Scale pooled training data for hyperparameter search
    scaler_cv = MinMaxScaler()
    X_pool_scaled = scaler_cv.fit_transform(X_pool)
    
    # TimeSeriesSplit cross-validator (5 folds)
    tscv = TimeSeriesSplit(n_splits=5)
    
    # 1. Random Forest Grid Search
    rf_grid = {
        'n_estimators': [50, 100],
        'max_depth': [3, 5, 7]
    }
    rf_cv = GridSearchCV(
        estimator=RandomForestRegressor(random_state=42, n_jobs=-1),
        param_grid=rf_grid,
        cv=tscv,
        scoring='neg_mean_squared_error',
        n_jobs=-1
    )
    rf_cv.fit(X_pool_scaled, y_pool)
    best_rf_params = rf_cv.best_params_
    
    # 2. XGBoost Grid Search
    xgb_grid = {
        'n_estimators': [50, 100],
        'max_depth': [3, 4, 5],
        'learning_rate': [0.01, 0.03, 0.05]
    }
    xgb_cv = GridSearchCV(
        estimator=XGBRegressor(random_state=42, n_jobs=-1),
        param_grid=xgb_grid,
        cv=tscv,
        scoring='neg_mean_squared_error',
        n_jobs=-1
    )
    xgb_cv.fit(X_pool_scaled, y_pool)
    best_xgb_params = xgb_cv.best_params_
    
    print(f"Optimal Random Forest Hyperparameters (TimeSeriesSplit): {best_rf_params}")
    print(f"Optimal XGBoost Hyperparameters (TimeSeriesSplit): {best_xgb_params}")
    
    # Save hyperparameter tuning results
    hp_summary = [
        {'Model': 'Random Forest', **best_rf_params, 'Best CV Neg MSE': rf_cv.best_score_},
        {'Model': 'XGBoost', **best_xgb_params, 'Best CV Neg MSE': xgb_cv.best_score_}
    ]
    pd.DataFrame(hp_summary).to_csv('output/tables/best_hyperparameters.csv', index=False)
    
    return best_rf_params, best_xgb_params

def train_and_evaluate_ml_models_walk_forward(train_initial_end_date='2020-12-31', retrain_freq_weeks=13):
    """
    Executes Expanding Rolling Window Walk-Forward Validation for Random Forest and XGBoost.
    - Features scaled strictly within training window (zero test-set leakage).
    - Hyperparameters tuned chronologically via TimeSeriesSplit CV.
    - Initial train period: 2010-2020. Out-of-sample test period: 2021-2025.
    - Re-trains models every `retrain_freq_weeks` (quarterly walk-forward refit).
    """
    master_feat = generate_all_features()
    
    feature_cols = ['MACD', 'PPO', 'RSI', 'STOCH', 'Lag_1', 'Lag_2', 'Lag_3', 'Lag_4', 'SMA', 'ADX', 'SAR', 'ATR', 'OBV']
    
    # Tune hyperparameters via TimeSeriesSplit CV on 2010-2020 data
    best_rf_params, best_xgb_params = tune_hyperparameters_time_series(master_feat, feature_cols, train_initial_end_date)
    
    rf_predictions = {}
    xgb_predictions = {}
    actual_returns = {}
    baseline_predictions = {}
    
    performance_metrics = []
    
    rf_feature_importances = []
    xgb_feature_importances = []
    
    print(f"\nStarting Expanding Rolling Window Walk-Forward Validation (Re-train frequency: every {retrain_freq_weeks} weeks)...")
    
    for ticker, df in master_feat.items():
        test_mask = df.index > train_initial_end_date
        test_indices = np.where(test_mask)[0]
        
        y_test_all = df['Target_Return'].iloc[test_indices].values
        test_dates = df.index[test_indices]
        
        actual_returns[ticker] = pd.Series(y_test_all, index=test_dates)
        
        y_pred_rf = np.zeros(len(test_indices))
        y_pred_xgb = np.zeros(len(test_indices))
        y_pred_base = np.zeros(len(test_indices))
        
        rf_model = None
        xgb_model = None
        scaler = None
        
        for step_idx, global_idx in enumerate(test_indices):
            if step_idx % retrain_freq_weeks == 0 or rf_model is None:
                train_sub = df.iloc[:global_idx]
                X_tr_raw, y_tr = train_sub[feature_cols].values, train_sub['Target_Return'].values
                
                # Fit MinMaxScaler STRICTLY on expanding training window (No test leakage)
                scaler = MinMaxScaler()
                X_tr_scaled = scaler.fit_transform(X_tr_raw)
                
                # Fit Random Forest with tuned hyperparameters
                rf_model = RandomForestRegressor(**best_rf_params, random_state=42, n_jobs=-1)
                rf_model.fit(X_tr_scaled, y_tr)
                
                # Fit XGBoost with tuned hyperparameters
                xgb_model = XGBRegressor(**best_xgb_params, random_state=42, n_jobs=-1)
                xgb_model.fit(X_tr_scaled, y_tr)
                
                hist_mean = np.mean(y_tr)
                
                rf_feature_importances.append(rf_model.feature_importances_)
                xgb_feature_importances.append(xgb_model.feature_importances_)
                
            # Scale single test instance using scaler fit on training window ONLY
            X_curr_raw = df[feature_cols].iloc[global_idx:global_idx+1].values
            X_curr_scaled = scaler.transform(X_curr_raw)
            
            y_pred_rf[step_idx] = rf_model.predict(X_curr_scaled)[0]
            y_pred_xgb[step_idx] = xgb_model.predict(X_curr_scaled)[0]
            y_pred_base[step_idx] = hist_mean
            
        rf_predictions[ticker] = pd.Series(y_pred_rf, index=test_dates)
        xgb_predictions[ticker] = pd.Series(y_pred_xgb, index=test_dates)
        baseline_predictions[ticker] = pd.Series(y_pred_base, index=test_dates)
        
        # Compute Metrics
        def calc_da(y_true, y_pred):
            return np.mean(np.sign(y_true) == np.sign(y_pred)) * 100
        
        rmse_base = np.sqrt(mean_squared_error(y_test_all, y_pred_base))
        mae_base = mean_absolute_error(y_test_all, y_pred_base)
        da_base = calc_da(y_test_all, y_pred_base)
        
        rmse_rf = np.sqrt(mean_squared_error(y_test_all, y_pred_rf))
        mae_rf = mean_absolute_error(y_test_all, y_pred_rf)
        r2_rf = r2_score(y_test_all, y_pred_rf)
        da_rf = calc_da(y_test_all, y_pred_rf)
        
        rmse_xgb = np.sqrt(mean_squared_error(y_test_all, y_pred_xgb))
        mae_xgb = mean_absolute_error(y_test_all, y_pred_xgb)
        r2_xgb = r2_score(y_test_all, y_pred_xgb)
        da_xgb = calc_da(y_test_all, y_pred_xgb)
        
        performance_metrics.append({
            'Ticker': ticker,
            'Base RMSE': rmse_base,
            'Base MAE': mae_base,
            'Base DA (%)': da_base,
            'RF RMSE': rmse_rf,
            'RF MAE': mae_rf,
            'RF R2': r2_rf,
            'RF DA (%)': da_rf,
            'XGB RMSE': rmse_xgb,
            'XGB MAE': mae_xgb,
            'XGB R2': r2_xgb,
            'XGB DA (%)': da_xgb
        })
        
    perf_df = pd.DataFrame(performance_metrics)
    perf_df.to_csv('output/tables/ml_forecasting_performance.csv', index=False)
    
    # Save predicted return matrices for walk-forward test period (2021-2025)
    rf_pred_df = pd.DataFrame(rf_predictions)
    xgb_pred_df = pd.DataFrame(xgb_predictions)
    actual_ret_df = pd.DataFrame(actual_returns)
    base_pred_df = pd.DataFrame(baseline_predictions)
    
    rf_pred_df.to_csv('output/tables/rf_predicted_returns.csv')
    xgb_pred_df.to_csv('output/tables/xgb_predicted_returns.csv')
    actual_ret_df.to_csv('output/tables/actual_test_returns.csv')
    base_pred_df.to_csv('output/tables/baseline_predicted_returns.csv')
    
    # Average Feature Importance across all walk-forward iterations
    avg_rf_fi = np.mean(rf_feature_importances, axis=0)
    avg_xgb_fi = np.mean(xgb_feature_importances, axis=0)
    
    fi_df = pd.DataFrame({
        'Feature': feature_cols,
        'Random Forest Importance': avg_rf_fi,
        'XGBoost Importance': avg_xgb_fi,
        'Combined Average': (avg_rf_fi + avg_xgb_fi) / 2
    }).sort_values('Combined Average', ascending=False)
    
    fi_df.to_csv('output/tables/feature_importance.csv', index=False)
    
    # Plot Feature Importance Bar Chart
    plt.figure(figsize=(12, 7))
    x = np.arange(len(feature_cols))
    width = 0.35
    
    sorted_cols = fi_df['Feature'].values
    rf_vals = fi_df['Random Forest Importance'].values
    xgb_vals = fi_df['XGBoost Importance'].values
    
    plt.bar(x - width/2, rf_vals, width, label='Random Forest', color='#2b5c8f')
    plt.bar(x + width/2, xgb_vals, width, label='XGBoost', color='#d95f02')
    
    plt.xlabel('Technical Indicator Features ($X_t$)', fontweight='bold', labelpad=10)
    plt.ylabel('Mean Decrease Impurity (MDI) Importance', fontweight='bold')
    plt.title('Walk-Forward Feature Importance of 13 Technical Indicators across 28 NGX Stocks', fontweight='bold', pad=15)
    plt.xticks(x, sorted_cols, rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('output/figures/feature_importance_bar.png', dpi=300)
    plt.close()
    
    print("\n--- Walk-Forward ML Predictive Performance Summary (Averages across 28 Assets) ---")
    avg_row = {
        'RF RMSE': perf_df['RF RMSE'].mean(),
        'XGB RMSE': perf_df['XGB RMSE'].mean(),
        'RF MAE': perf_df['RF MAE'].mean(),
        'XGB MAE': perf_df['XGB MAE'].mean(),
        'RF DA (%)': perf_df['RF DA (%)'].mean(),
        'XGB DA (%)': perf_df['XGB DA (%)'].mean(),
        'Base DA (%)': perf_df['Base DA (%)'].mean()
    }
    for k, v in avg_row.items():
        print(f"{k:<15}: {v:.6f}" if 'DA' not in k else f"{k:<15}: {v:.2f}%")
        
    print("\nWalk-Forward Machine Learning Predictive Modeling Complete!")
    return perf_df, fi_df, rf_pred_df, xgb_pred_df, actual_ret_df

if __name__ == '__main__':
    train_and_evaluate_ml_models_walk_forward()

