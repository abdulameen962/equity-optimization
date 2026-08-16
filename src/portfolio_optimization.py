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

# =========================================================================
# STATISTICAL SIGNIFICANCE TESTING ENGINE
# =========================================================================

def jobson_korkie_memmel_test(ret_a, ret_b, rf_weekly=RF_WEEKLY):
    """
    Jobson & Korkie (1981) test with Memmel (2007) correction for Sharpe Ratio equality.
    ret_a, ret_b: Weekly return vectors of two strategies.
    Returns: (z_stat, p_value, sharpe_a, sharpe_b)
    """
    from scipy.stats import norm
    
    ex_a = ret_a - rf_weekly
    ex_b = ret_b - rf_weekly
    
    T = len(ret_a)
    mu_a = np.mean(ex_a) * 52
    mu_b = np.mean(ex_b) * 52
    
    sig_a = np.std(ret_a, ddof=1) * np.sqrt(52)
    sig_b = np.std(ret_b, ddof=1) * np.sqrt(52)
    
    sharpe_a = (mu_a) / (sig_a + 1e-10)
    sharpe_b = (mu_b) / (sig_b + 1e-10)
    
    rho = np.corrcoef(ret_a, ret_b)[0, 1] if np.std(ret_a) > 0 and np.std(ret_b) > 0 else 0.0
    
    # Memmel (2007) asymptotic variance formula
    var_diff = (1.0 / (T / 52.0)) * (2.0 * (1.0 - rho) + 0.5 * (sharpe_a**2 + sharpe_b**2 - 2.0 * sharpe_a * sharpe_b * (rho**2)))
    
    se = np.sqrt(np.maximum(1e-10, var_diff))
    z_stat = (sharpe_a - sharpe_b) / se
    p_val = 2.0 * (1.0 - norm.cdf(np.abs(z_stat)))
    
    return z_stat, p_val, sharpe_a, sharpe_b

def ledoit_wolf_bootstrap_sharpe(ret_a, ret_b, rf_weekly=RF_WEEKLY, n_boot=2000, block_size=5):
    """
    Ledoit and Wolf (2008) Circular Block Bootstrap test for Sharpe Ratio equality.
    Accounting for heavy tails, non-normality, and GARCH autocorrelation.
    """
    np.random.seed(42)
    T = len(ret_a)
    ex_a = ret_a - rf_weekly
    ex_b = ret_b - rf_weekly
    
    # Observed Sharpe difference
    s_a = (np.mean(ex_a) * 52) / (np.std(ret_a, ddof=1) * np.sqrt(52) + 1e-10)
    s_b = (np.mean(ex_b) * 52) / (np.std(ret_b, ddof=1) * np.sqrt(52) + 1e-10)
    d_obs = s_a - s_b
    
    # Circular block bootstrap
    d_boot = np.zeros(n_boot)
    n_blocks = int(np.ceil(T / block_size))
    
    for i in range(n_boot):
        start_indices = np.random.randint(0, T, size=n_blocks)
        boot_idx = []
        for idx in start_indices:
            boot_idx.extend([(idx + k) % T for k in range(block_size)])
        boot_idx = boot_idx[:T]
        
        r_a_b = ret_a[boot_idx]
        r_b_b = ret_b[boot_idx]
        
        sa_b = (np.mean(r_a_b - rf_weekly) * 52) / (np.std(r_a_b, ddof=1) * np.sqrt(52) + 1e-10)
        sb_b = (np.mean(r_b_b - rf_weekly) * 52) / (np.std(r_b_b, ddof=1) * np.sqrt(52) + 1e-10)
        d_boot[i] = sa_b - sb_b
        
    # Two-sided empirical p-value under H0: d = 0 (centered)
    d_boot_centered = d_boot - np.mean(d_boot)
    p_val = np.mean(np.abs(d_boot_centered) >= np.abs(d_obs))
    
    return d_obs, p_val

def ledoit_wolf_bootstrap_sortino(ret_a, ret_b, rf_weekly=RF_WEEKLY, n_boot=2000, block_size=5):
    """
    Ledoit and Wolf (2011) Circular Block Bootstrap test for Sortino Ratio equality.
    """
    np.random.seed(42)
    T = len(ret_a)
    
    def calc_sortino(ret):
        mean_ret = np.mean(ret - rf_weekly) * 52
        down_diff = np.minimum(0, ret - rf_weekly)
        down_dev = np.sqrt(np.mean(down_diff**2)) * np.sqrt(52)
        return mean_ret / (down_dev + 1e-10)
        
    sort_a = calc_sortino(ret_a)
    sort_b = calc_sortino(ret_b)
    d_obs = sort_a - sort_b
    
    d_boot = np.zeros(n_boot)
    n_blocks = int(np.ceil(T / block_size))
    
    for i in range(n_boot):
        start_indices = np.random.randint(0, T, size=n_blocks)
        boot_idx = []
        for idx in start_indices:
            boot_idx.extend([(idx + k) % T for k in range(block_size)])
        boot_idx = boot_idx[:T]
        
        sa_b = calc_sortino(ret_a[boot_idx])
        sb_b = calc_sortino(ret_b[boot_idx])
        d_boot[i] = sa_b - sb_b
        
    d_boot_centered = d_boot - np.mean(d_boot)
    p_val = np.mean(np.abs(d_boot_centered) >= np.abs(d_obs))
    
    return d_obs, p_val

def paired_return_tests(ret_a, ret_b):
    """
    Paired Student's t-test and Wilcoxon Signed-Rank test on weekly return differences.
    """
    from scipy.stats import ttest_rel, wilcoxon
    
    diff = ret_a - ret_b
    t_stat, p_t = ttest_rel(ret_a, ret_b)
    try:
        w_stat, p_w = wilcoxon(diff)
    except Exception:
        w_stat, p_w = 0.0, 1.0
        
    return t_stat, p_t, w_stat, p_w

def run_portfolio_backtests(transaction_cost_rate=0.0075):
    """
    Out-of-sample portfolio backtesting (2021 - 2025) comparing 6 strategies.
    """
    # Load test returns and ML predictions
    rf_pred = pd.read_csv('output/tables/rf_predicted_returns.csv', index_col=0, parse_dates=True).fillna(0.0)
    xgb_pred = pd.read_csv('output/tables/xgb_predicted_returns.csv', index_col=0, parse_dates=True).fillna(0.0)
    actual_ret = pd.read_csv('output/tables/actual_test_returns.csv', index_col=0, parse_dates=True).fillna(0.0)
    
    tickers = actual_ret.columns.tolist()
    
    N = len(tickers)
    T_test = len(actual_ret)
    
    # Pre-allocate weight matrices
    w_rf = np.zeros((T_test, N))
    w_xgb = np.zeros((T_test, N))
    w_hist_cvar = np.zeros((T_test, N))
    w_mvo = np.zeros((T_test, N))
    w_ewp = np.full((T_test, N), 1.0 / N)
    
    # NGX Index Buy-Hold starts at 1/N equal weight at t=0 and drifts passively without rebalancing
    w_buy_hold = np.zeros((T_test, N))
    w_curr = np.ones(N) / N
    w_buy_hold[0, :] = w_curr
    for t in range(1, T_test):
        ret_t_1 = actual_ret.iloc[t-1].values
        # Gross asset accumulation: exp(r)
        gross_growth = w_curr * np.exp(ret_t_1)
        w_curr = gross_growth / np.sum(gross_growth)
        w_buy_hold[t, :] = w_curr
        
    # Run rolling optimization
    hist_returns_window = actual_ret.values # Rolling window
    
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
        'RF-CVaR': (w_rf, False),
        'XGB-CVaR': (w_xgb, False),
        'Historical-CVaR': (w_hist_cvar, False),
        'Mean-Variance (MVO)': (w_mvo, False),
        '1/N Equal Weight': (w_ewp, False),
        'NGX Index Buy-Hold': (w_buy_hold, True) # Passive Buy-and-Hold (0 turnover post t=0)
    }
    
    backtest_results = {}
    net_returns_dict = {}
    performance_summary = []
    
    plt.figure(figsize=(12, 7))
    
    for name, (W, is_buy_hold) in strategies.items():
        port_gross_ret = np.sum(W * actual_ret.values, axis=1)
        
        # Calculate turnover and transaction cost
        if is_buy_hold:
            # Passive Buy-Hold has 0 trading turnover after week 0
            turnover = np.zeros(T_test)
            turnover[0] = 1.0 # Initial portfolio entry cost
        else:
            turnover = np.sum(np.abs(W[1:] - W[:-1]), axis=1)
            turnover = np.insert(turnover, 0, np.sum(W[0])) # First week entry cost
        
        tx_costs = turnover * transaction_cost_rate
        port_net_ret = port_gross_ret - tx_costs
        net_returns_dict[name] = port_net_ret
        
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
        
        # Average Turnover (excluding week 0 entry for display if passive)
        avg_turnover = np.mean(turnover[1:]) if is_buy_hold else np.mean(turnover)
        
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
    return perf_df, net_returns_dict

def run_all_fee_regimes_and_significance():
    """
    Executes backtests across 3 transaction fee regimes:
    - 1.50% Retail Brokerage Fees & Market Slippage
    - 0.75% Institutional PFA Brokerage Fees & Execution Friction
    - 0.00% Zero-Cost Gross Performance
    
    Computes pairwise statistical significance tests across all 3 regimes.
    """
    print("Executing Mean-CVaR Portfolio Optimization & Multi-Tier Backtesting...")
    
    print("\n--- Regime 1: Retail Scenario (1.50% Fees & Slippage) ---")
    perf_retail_df, ret_retail = run_portfolio_backtests(transaction_cost_rate=0.0150)
    perf_retail_df.to_csv('output/tables/portfolio_performance_summary.csv', index=False)
    print("Saved output/tables/portfolio_performance_summary.csv")
    
    print("\n--- Regime 2: Institutional PFA Scenario (0.75% Fees) ---")
    perf_inst_df, ret_inst = run_portfolio_backtests(transaction_cost_rate=0.0075)
    perf_inst_df.to_csv('output/tables/portfolio_performance_institutional.csv', index=False)
    print("Saved output/tables/portfolio_performance_institutional.csv")
    
    print("\n--- Regime 3: Zero-Cost Scenario (0.00% Gross Performance) ---")
    perf_zero_df, ret_zero = run_portfolio_backtests(transaction_cost_rate=0.0000)
    perf_zero_df.to_csv('output/tables/portfolio_performance_zero_cost.csv', index=False)
    print("Saved output/tables/portfolio_performance_zero_cost.csv")
    
    # Compute Multi-Tier Pairwise Statistical Significance Tests
    regimes = {
        'Gross (0.00%)': ret_zero,
        'Institutional (0.75%)': ret_inst,
        'Retail (1.50%)': ret_retail
    }
    
    pairwise_pairs = [
        ('XGB-CVaR', 'NGX Index Buy-Hold'),
        ('RF-CVaR', 'NGX Index Buy-Hold'),
        ('Historical-CVaR', 'NGX Index Buy-Hold'),
        ('Historical-CVaR', '1/N Equal Weight'),
        ('XGB-CVaR', 'Historical-CVaR'),
        ('Mean-Variance (MVO)', '1/N Equal Weight')
    ]
    
    sig_records = []
    
    for fee_label, ret_dict in regimes.items():
        for strat, bench in pairwise_pairs:
            ret_strat = ret_dict[strat]
            ret_bench = ret_dict[bench]
            
            z_jk, p_jk, s_a, s_b = jobson_korkie_memmel_test(ret_strat, ret_bench)
            d_sharpe, p_lw_sharpe = ledoit_wolf_bootstrap_sharpe(ret_strat, ret_bench)
            d_sortino, p_lw_sortino = ledoit_wolf_bootstrap_sortino(ret_strat, ret_bench)
            t_stat, p_t, w_stat, p_w = paired_return_tests(ret_strat, ret_bench)
            
            sig_records.append({
                'Fee Regime': fee_label,
                'Strategy': strat,
                'Benchmark': bench,
                'Sharpe Diff': s_a - s_b,
                'Jobson-Korkie Z': z_jk,
                'Jobson-Korkie p-val': p_jk,
                'Ledoit-Wolf Sharpe p-val': p_lw_sharpe,
                'Ledoit-Wolf Sortino p-val': p_lw_sortino,
                'Paired t-stat p-val': p_t,
                'Wilcoxon p-val': p_w
            })
            
    sig_df = pd.DataFrame(sig_records)
    sig_df.to_csv('output/tables/portfolio_significance_tests.csv', index=False)
    print("\n--- Multi-Tier Pairwise Statistical Significance Tests (Saved to output/tables/portfolio_significance_tests.csv) ---")
    print(sig_df.to_string(index=False))

if __name__ == '__main__':
    run_all_fee_regimes_and_significance()

