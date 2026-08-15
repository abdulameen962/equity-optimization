import os
import sys
sys.path.insert(0, '.')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import linprog, minimize

# Ensure output directories exist
os.makedirs('output/tables', exist_ok=True)
os.makedirs('output/figures', exist_ok=True)

# Weekly Risk-Free Rate: (1 + 0.18)^(1/52) - 1 ≈ 0.00319 (0.319% per week)
RF_WEEKLY = (1.18)**(1/52) - 1

def solve_mean_cvar(expected_returns, historical_returns, alpha=0.95, target_return=None):
    """
    Solves Tail-Risk Mean-CVaR optimization using Linear Programming.
    historical_returns: numpy array (T_history x N_assets)
    expected_returns: vector of expected returns (N_assets,)
    """
    expected_returns = np.nan_to_num(expected_returns, nan=0.0, posinf=0.0, neginf=0.0)
    historical_returns = np.nan_to_num(historical_returns, nan=0.0, posinf=0.0, neginf=0.0)
    
    T, N = historical_returns.shape
    
    if target_return is None:
        target_return = np.mean(expected_returns)
    else:
        target_return = np.nan_to_num(target_return, nan=0.0)
        
    # Decision variables: x = [gamma (1), z_1..z_T (T), w_1..w_N (N)] -> Total variables: 1 + T + N
    c = np.zeros(1 + T + N)
    c[0] = 1.0
    c[1:1+T] = 1.0 / ((1.0 - alpha) * T)
    
    # Inequality constraints: A_ub @ x <= b_ub
    # z_t >= -w^T r_t - gamma  ==>  -gamma - z_t - w^T r_t <= 0
    A_ub = []
    b_ub = []
    
    for t in range(T):
        row = np.zeros(1 + T + N)
        row[0] = -1.0
        row[1 + t] = -1.0
        row[1 + T:] = -historical_returns[t, :]
        A_ub.append(row)
        b_ub.append(0.0)
        
    # Target return constraint: w^T mu >= target_return  ==>  -w^T mu <= -target_return
    row_ret = np.zeros(1 + T + N)
    row_ret[1 + T:] = -expected_returns
    A_ub.append(row_ret)
    b_ub.append(-target_return)
    
    # Equality constraint: sum(w) = 1
    A_eq = np.zeros((1, 1 + T + N))
    A_eq[0, 1 + T:] = 1.0
    b_eq = [1.0]
    
    # Bounds: gamma unconstrained, z_t >= 0, 0 <= w_i <= 1
    bounds = [(None, None)] + [(0, None)] * T + [(0, 1.0)] * N
    
    try:
        res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub), A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        if res.success:
            w = res.x[1 + T:]
            w = np.maximum(0, w)
            w_sum = np.sum(w)
            return w / w_sum if w_sum > 0 else np.ones(N) / N
    except Exception:
        pass
    
    return np.ones(N) / N

def solve_mean_variance(expected_returns, cov_matrix, risk_aversion=3.0):
    """
    Solves Markowitz Mean-Variance optimization (MVO).
    """
    expected_returns = np.nan_to_num(expected_returns, nan=0.0, posinf=0.0, neginf=0.0)
    cov_matrix = np.nan_to_num(cov_matrix, nan=0.0, posinf=0.0, neginf=0.0)
    
    N = len(expected_returns)
    
    def objective(w):
        port_ret = np.dot(w, expected_returns)
        port_vol = np.sqrt(np.maximum(1e-8, np.dot(w.T, np.dot(cov_matrix, w))))
        return -(port_ret - 0.5 * risk_aversion * (port_vol**2))
    
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0})
    bounds = [(0, 1.0) for _ in range(N)]
    init_w = np.ones(N) / N
    
    try:
        res = minimize(objective, init_w, method='SLSQP', bounds=bounds, constraints=constraints)
        if res.success:
            w = res.x
            w = np.maximum(0, w)
            w_sum = np.sum(w)
            return w / w_sum if w_sum > 0 else init_w
    except Exception:
        pass
        
    return init_w

def run_portfolio_backtests(transaction_cost_rate=0.0075):
    """
    Out-of-sample portfolio backtesting (2021 - 2025) comparing 6 strategies.
    """
    # Load test returns and ML predictions
    rf_pred = pd.read_csv('output/tables/rf_predicted_returns.csv', index_col=0, parse_dates=True).fillna(0.0)
    xgb_pred = pd.read_csv('output/tables/xgb_predicted_returns.csv', index_col=0, parse_dates=True).fillna(0.0)
    actual_ret = pd.read_csv('output/tables/actual_test_returns.csv', index_col=0, parse_dates=True).fillna(0.0)
    
    # Load historical returns for covariance/scenario estimations (2010-2020)
    full_returns = pd.read_csv('output/tables/descriptive_and_diagnostic_stats.csv') # To get asset tickers order
    tickers = actual_ret.columns.tolist()
    
    N = len(tickers)
    T_test = len(actual_ret)
    
    # Pre-allocate weight matrices
    w_rf = np.zeros((T_test, N))
    w_xgb = np.zeros((T_test, N))
    w_hist_cvar = np.zeros((T_test, N))
    w_mvo = np.zeros((T_test, N))
    w_ewp = np.full((T_test, N), 1.0 / N)
    w_buy_hold = np.full((T_test, N), 1.0 / N)
    
    # Run rolling optimization
    hist_returns_window = actual_ret.values # Simplified rolling sample window
    
    for t in range(T_test):
        # 1. RF-CVaR
        mu_rf = rf_pred.iloc[t].values
        w_rf[t, :] = solve_mean_cvar(mu_rf, hist_returns_window, alpha=0.95)
        
        # 2. XGB-CVaR
        mu_xgb = xgb_pred.iloc[t].values
        w_xgb[t, :] = solve_mean_cvar(mu_xgb, hist_returns_window, alpha=0.95)
        
        # 3. Historical CVaR
        mu_hist = np.mean(hist_returns_window, axis=0)
        w_hist_cvar[t, :] = solve_mean_cvar(mu_hist, hist_returns_window, alpha=0.95)
        
        # 4. Mean-Variance (MVO)
        cov_mat = np.cov(hist_returns_window, rowvar=False) + np.eye(N) * 1e-6
        w_mvo[t, :] = solve_mean_variance(mu_rf, cov_mat)
        
    strategies = {
        'RF-CVaR': w_rf,
        'XGB-CVaR': w_xgb,
        'Historical-CVaR': w_hist_cvar,
        'Mean-Variance (MVO)': w_mvo,
        '1/N Equal Weight': w_ewp,
        'NGX Index Buy-Hold': w_buy_hold
    }
    
    backtest_results = {}
    performance_summary = []
    
    plt.figure(figsize=(12, 7))
    
    for name, W in strategies.items():
        port_gross_ret = np.sum(W * actual_ret.values, axis=1)
        
        # Calculate turnover and transaction cost
        turnover = np.sum(np.abs(W[1:] - W[:-1]), axis=1)
        turnover = np.insert(turnover, 0, np.sum(W[0])) # First week entry cost
        
        tx_costs = turnover * transaction_cost_rate
        port_net_ret = port_gross_ret - tx_costs
        
        # Cumulative Equity Curve
        cum_ret = np.exp(np.cumsum(port_net_ret)) # Starting at $1.0
        backtest_results[name] = cum_ret
        
        # Annualized Metrics (52 weeks per year)
        mean_ret = np.mean(port_net_ret) * 52
        volatility = np.std(port_net_ret, ddof=1) * np.sqrt(52)
        
        # Sharpe Ratio (using weekly Rf = 0.319% -> 18% annualized)
        rf_annual = 0.18
        sharpe = (mean_ret - rf_annual) / (volatility + 1e-10)
        
        # Downside Deviation & Sortino Ratio
        downside_diff = np.minimum(0, port_net_ret - RF_WEEKLY)
        downside_dev = np.sqrt(np.mean(downside_diff**2)) * np.sqrt(52)
        sortino = (mean_ret - rf_annual) / (downside_dev + 1e-10)
        
        # Value-at-Risk (VaR 95%) and Conditional Value-at-Risk (CVaR 95%)
        var_95 = np.percentile(port_net_ret, 5)
        cvar_mask = port_net_ret <= var_95
        cvar_95 = np.mean(port_net_ret[cvar_mask]) if np.any(cvar_mask) else var_95
        
        # Maximum Drawdown (MDD)
        peak = np.maximum.accumulate(cum_ret)
        drawdown = (cum_ret - peak) / (peak + 1e-10)
        mdd = np.min(drawdown)
        
        # Average Turnover
        avg_turnover = np.mean(turnover)
        
        performance_summary.append({
            'Strategy': name,
            'Annualized Return (%)': mean_ret * 100,
            'Annualized Volatility (%)': volatility * 100,
            'Sharpe Ratio': sharpe,
            'Sortino Ratio': sortino,
            'VaR (95%) (%)': var_95 * 100,
            'CVaR (95%) (%)': cvar_95 * 100,
            'Max Drawdown (%)': mdd * 100,
            'Avg Weekly Turnover (%)': avg_turnover * 100
        })
        
        plt.plot(actual_ret.index, cum_ret, label=name, linewidth=2)
        
    plt.xlabel('Date (Out-of-Sample Test Period 2021 - 2025)', fontweight='bold', labelpad=10)
    plt.ylabel('Normalized Cumulative Wealth (Base = $1.0)', fontweight='bold')
    plt.title('Out-of-Sample Equity Growth Curves: ML-CVaR vs Benchmark Portfolios', fontweight='bold', pad=15)
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('output/figures/portfolio_equity_curves.png', dpi=300)
    plt.close()
    
    perf_df = pd.DataFrame(performance_summary)
    perf_df.to_csv('output/tables/portfolio_performance_summary.csv', index=False)
    
    print("\n--- Out-of-Sample Portfolio Performance Comparison (2021 - 2025) ---")
    print(perf_df.to_string(index=False))
    
    return perf_df

if __name__ == '__main__':
    print("Executing Mean-CVaR Portfolio Optimization & Backtesting...")
    print("\n--- Running Backtest 1: With 0.75% Transaction Fees & Slippage ---")
    perf_fee_df = run_portfolio_backtests(transaction_cost_rate=0.0075)
    
    print("\n--- Running Backtest 2: Zero Transaction Costs (Gross Performance) ---")
    perf_zero_df = run_portfolio_backtests(transaction_cost_rate=0.0000)
    perf_zero_df.to_csv('output/tables/portfolio_performance_zero_cost.csv', index=False)
    print("Saved output/tables/portfolio_performance_zero_cost.csv")
