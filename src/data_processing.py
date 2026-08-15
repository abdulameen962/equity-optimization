import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
try:
    import seaborn as sns
except ImportError:
    sns = None
from scipy import stats
from statsmodels.tsa.stattools import adfuller

# Ensure output directories exist
os.makedirs('output/tables', exist_ok=True)
os.makedirs('output/figures', exist_ok=True)

def parse_volume(vol_str):
    """Clean Investing.com Volume string (e.g. '741.34M', '17.98K', '2.16B', '-') to float."""
    if pd.isna(vol_str) or vol_str == '-' or str(vol_str).strip() == '':
        return 0.0
    vol_str = str(vol_str).strip().upper()
    multiplier = 1.0
    if vol_str.endswith('K'):
        multiplier = 1e3
        vol_str = vol_str[:-1]
    elif vol_str.endswith('M'):
        multiplier = 1e6
        vol_str = vol_str[:-1]
    elif vol_str.endswith('B'):
        multiplier = 1e9
        vol_str = vol_str[:-1]
    
    # Remove any commas
    vol_str = vol_str.replace(',', '')
    try:
        return float(vol_str) * multiplier
    except ValueError:
        return 0.0

def parse_price(price_str):
    """Clean price string (e.g. '2,270.00') to float."""
    if pd.isna(price_str) or price_str == '-' or str(price_str).strip() == '':
        return np.nan
    p_str = str(price_str).replace(',', '').strip()
    try:
        return float(p_str)
    except ValueError:
        return np.nan

def clean_stock_name(filename):
    """Extract clean stock ticker/short name from CSV filename."""
    name = filename.replace(' Stock Price History.csv', '')
    name_map = {
        'Access Holdings': 'ACCESS',
        'Conoil': 'CONOIL',
        'Custodian Allied': 'CUSTODIAN',
        'Dangote Cement': 'DANGCEM',
        'Dangote Sugar': 'DANGSUGAR',
        'ETI': 'ETI',
        'Fcmb': 'FCMB',
        'Fidelitybk': 'FIDELITYBK',
        'Fidson': 'FIDSON',
        'First HoldCo': 'FBNH',
        'Guaranty Trust Holding': 'GTCO',
        'Guinness Nigeria': 'GUINNESS',
        'Julius Berger': 'JBERGER',
        'Lafarge Africa': 'WAPCO',
        'Mansard Ins': 'MANSARD',
        'Nahco': 'NAHCO',
        'Nascon': 'NASCON',
        'Nestle Nigeria': 'NESTLE',
        'Nigerian Breweries': 'NB',
        'Okomu Oil Palm': 'OKOMUOIL',
        'Presco': 'PRESCO',
        'STANBIC IBTC Bank': 'STANBIC',
        'Sterling Bank': 'STERLINGNG',
        'Transcorp': 'TRANSCORP',
        'UAC Of Nigeria': 'UACN',
        'UBA': 'UBA',
        'Unilever Nigeria': 'UNILEVER',
        'Wema Bank': 'WEMABANK',
        'Zenith Bank': 'ZENITHBANK'
    }
    return name_map.get(name, name.upper())

def load_and_preprocess_data(data_dir='data/valid_from_2010'):
    """
    Loads all 28 valid CSV files, parses numbers, aligns onto a master weekly calendar (2010-2025),
    applies forward-fill/backward-fill, and calculates log returns.
    """
    files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    raw_prices = {}
    raw_ohlcv = {}
    
    for f in sorted(files):
        filepath = os.path.join(data_dir, f)
        ticker = clean_stock_name(f)
        
        df = pd.read_csv(filepath)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date']).sort_values('Date').reset_index(drop=True)
        
        df['Price'] = df['Price'].apply(parse_price)
        df['Open'] = df['Open'].apply(parse_price)
        df['High'] = df['High'].apply(parse_price)
        df['Low'] = df['Low'].apply(parse_price)
        df['Vol.'] = df['Vol.'].apply(parse_volume)
        
        # Set date index
        df = df.set_index('Date')
        
        raw_prices[ticker] = df['Price']
        raw_ohlcv[ticker] = df[['Price', 'Open', 'High', 'Low', 'Vol.']]
        
    # Combine closing prices into a single DataFrame
    price_df = pd.DataFrame(raw_prices)
    
    # Create master weekly calendar from 2010-01-03 to 2025-12-28 (Sunday weekly frequency matching Investing.com)
    master_dates = pd.date_range(start='2010-01-03', end='2025-12-28', freq='W-SUN')
    
    # Reindex onto master calendar
    price_df = price_df.reindex(master_dates)
    
    # Apply forward fill (non-trading weeks) then backward fill (initial NaNs before listing)
    price_df = price_df.ffill().bfill()
    
    # Compute weekly logarithmic returns: R_{i,t} = ln(P_{i,t} / P_{i,t-1})
    returns_df = np.log(price_df / price_df.shift(1)).dropna()
    
    return price_df, returns_df, raw_ohlcv

def compute_descriptive_and_diagnostic_stats(returns_df):
    """
    Computes Descriptive Statistics (Mean, Std, Min, Max, Skewness, Kurtosis)
    and Statistical Non-Normality Diagnostics (Jarque-Bera, Shapiro-Wilk, ADF test).
    """
    stats_list = []
    
    for col in returns_df.columns:
        r = returns_df[col].values
        
        mean_val = np.mean(r)
        std_val = np.std(r, ddof=1)
        min_val = np.min(r)
        max_val = np.max(r)
        skew_val = stats.skew(r)
        kurt_val = stats.kurtosis(r) # Excess kurtosis
        
        # Jarque-Bera Test
        jb_stat, jb_p = stats.jarque_bera(r)
        
        # Shapiro-Wilk Test
        sw_stat, sw_p = stats.shapiro(r)
        
        # Augmented Dickey-Fuller Test for stationarity
        adf_res = adfuller(r, autolag='AIC')
        adf_stat, adf_p = adf_res[0], adf_res[1]
        
        stats_list.append({
            'Ticker': col,
            'Mean (%)': mean_val * 100,
            'Std Dev (%)': std_val * 100,
            'Min (%)': min_val * 100,
            'Max (%)': max_val * 100,
            'Skewness': skew_val,
            'Kurtosis': kurt_val,
            'JB Stat': jb_stat,
            'JB p-value': jb_p,
            'SW Stat': sw_stat,
            'SW p-value': sw_p,
            'ADF Stat': adf_stat,
            'ADF p-value': adf_p,
            'Stationary': 'Yes' if adf_p < 0.05 else 'No'
        })
        
    stats_df = pd.DataFrame(stats_list)
    stats_df.to_csv('output/tables/descriptive_and_diagnostic_stats.csv', index=False)
    print("Saved output/tables/descriptive_and_diagnostic_stats.csv")
    return stats_df

def plot_correlation_matrix(returns_df):
    """Generates and saves a 28x28 correlation matrix heatmap."""
    corr = returns_df.corr()
    corr.to_csv('output/tables/return_correlation_matrix.csv')
    
    plt.figure(figsize=(16, 14))
    if sns is not None:
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', vmin=-0.2, vmax=1.0,
                    linewidths=0.5, cbar_kws={'label': 'Pearson Correlation'})
    else:
        plt.imshow(corr, cmap='coolwarm', vmin=-0.2, vmax=1.0)
        plt.colorbar(label='Pearson Correlation')
        plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
        plt.yticks(range(len(corr.columns)), corr.columns)
        
    plt.title('NGX 28 Equity Return Correlation Matrix (2010 - 2025)', fontsize=16, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig('output/figures/correlation_heatmap.png', dpi=300)
    plt.close()
    print("Saved output/figures/correlation_heatmap.png")

def process_all_data():
    print("Executing Data Cleaning & Non-Normality Diagnostics...")
    price_df, returns_df, raw_ohlcv = load_and_preprocess_data()
    print(f"Master Price Matrix Shape: {price_df.shape} (Weeks x Assets)")
    print(f"Master Returns Matrix Shape: {returns_df.shape} (Weeks x Assets)")
    
    stats_df = compute_descriptive_and_diagnostic_stats(returns_df)
    plot_correlation_matrix(returns_df)
    print("Data Processing & Non-Normality Diagnostics Complete!")
    return price_df, returns_df, stats_df

if __name__ == '__main__':
    process_all_data()
