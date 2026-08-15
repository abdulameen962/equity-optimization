import os
import sys
sys.path.insert(0, '.')

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from src.data_processing import load_and_preprocess_data, clean_stock_name

# Try importing ta library, else fall back to explicit numpy/pandas implementations
try:
    import ta
except ImportError:
    ta = None

os.makedirs('output/processed_features', exist_ok=True)

def compute_technical_indicators_pandas(df):
    """
    Fallback implementation of the 13 technical indicators using pandas & numpy.
    Input df columns: ['Price', 'Open', 'High', 'Low', 'Vol.']
    """
    close = df['Price'].copy()
    high = df['High'].copy()
    low = df['Low'].copy()
    volume = df['Vol.'].copy()
    
    features = pd.DataFrame(index=df.index)
    
    # 1. MACD (EMA 12 - EMA 26)
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    features['MACD'] = ema12 - ema26
    
    # 2. PPO (Percentage Price Oscillator)
    features['PPO'] = ((ema12 - ema26) / ema26) * 100
    
    # 3. RSI (14-week Relative Strength Index)
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / (loss + 1e-10)
    features['RSI'] = 100 - (100 / (1 + rs))
    
    # 4. STOCH (%K 14-week)
    low14 = low.rolling(window=14).min()
    high14 = high.rolling(window=14).max()
    features['STOCH'] = ((close - low14) / (high14 - low14 + 1e-10)) * 100
    
    # 5-8. Lagged Log Returns (Lag 1 to Lag 4)
    log_ret = np.log(close / close.shift(1))
    features['Lag_1'] = log_ret
    features['Lag_2'] = log_ret.shift(1)
    features['Lag_3'] = log_ret.shift(2)
    features['Lag_4'] = log_ret.shift(3)
    
    # 9. SMA (14-week Simple Moving Average)
    features['SMA'] = close.rolling(window=14).mean()
    
    # 10. ADX (14-week Approximation)
    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=14).mean()
    
    up_move = high - high.shift(1)
    down_move = low.shift(1) - low
    pos_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    neg_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)
    
    pos_di = 100 * (pd.Series(pos_dm, index=df.index).rolling(window=14).mean() / (atr + 1e-10))
    neg_di = 100 * (pd.Series(neg_dm, index=df.index).rolling(window=14).mean() / (atr + 1e-10))
    dx = 100 * ((pos_di - neg_di).abs() / (pos_di + neg_di + 1e-10))
    features['ADX'] = dx.rolling(window=14).mean()
    
    # 11. Parabolic SAR (Wilder's Iterative Algorithm)
    sar = pd.Series(index=df.index, dtype=float)
    af_start = 0.02
    af_step = 0.02
    af_max = 0.20
    
    if len(close) > 1:
        is_uptrend = close.iloc[1] >= close.iloc[0]
        af = af_start
        ep = high.iloc[0] if is_uptrend else low.iloc[0]
        sar_val = low.iloc[0] if is_uptrend else high.iloc[0]
        sar.iloc[0] = sar_val
        
        for i in range(1, len(close)):
            prev_sar = sar_val
            sar_val = prev_sar + af * (ep - prev_sar)
            
            if is_uptrend:
                if low.iloc[i] < sar_val:
                    is_uptrend = False
                    sar_val = ep
                    ep = low.iloc[i]
                    af = af_start
                else:
                    if high.iloc[i] > ep:
                        ep = high.iloc[i]
                        af = min(af + af_step, af_max)
                    if i > 1:
                        sar_val = min(sar_val, low.iloc[i-1], low.iloc[i-2])
                    else:
                        sar_val = min(sar_val, low.iloc[i-1])
            else:
                if high.iloc[i] > sar_val:
                    is_uptrend = True
                    sar_val = ep
                    ep = high.iloc[i]
                    af = af_start
                else:
                    if low.iloc[i] < ep:
                        ep = low.iloc[i]
                        af = min(af + af_step, af_max)
                    if i > 1:
                        sar_val = max(sar_val, high.iloc[i-1], high.iloc[i-2])
                    else:
                        sar_val = max(sar_val, high.iloc[i-1])
            sar.iloc[i] = sar_val
    else:
        sar = close.copy()
    features['SAR'] = sar
    
    # 12. ATR (14-week Average True Range)
    features['ATR'] = atr
    
    # 13. OBV (On-Balance Volume)
    obv_direction = np.sign(close.diff().fillna(0))
    features['OBV'] = (obv_direction * volume).cumsum()
    
    # Target Variable: 1-week ahead log return R_{t+1}
    features['Target_Return'] = log_ret.shift(-1)
    
    return features

def compute_technical_indicators_ta(df):
    """
    Uses the `ta` technical analysis library if installed.
    """
    close = df['Price'].copy()
    high = df['High'].copy()
    low = df['Low'].copy()
    volume = df['Vol.'].copy()
    
    features = pd.DataFrame(index=df.index)
    
    # 1. MACD
    macd_obj = ta.trend.MACD(close=close, window_slow=26, window_fast=12)
    features['MACD'] = macd_obj.macd()
    
    # 2. PPO
    features['PPO'] = ta.momentum.PercentagePriceOscillator(close=close, window_slow=26, window_fast=12).ppo()
    
    # 3. RSI
    features['RSI'] = ta.momentum.RSIIndicator(close=close, window=14).rsi()
    
    # 4. STOCH
    stoch_obj = ta.momentum.StochasticOscillator(high=high, low=low, close=close, window=14)
    features['STOCH'] = stoch_obj.stoch()
    
    # 5-8. Lagged Log Returns
    log_ret = np.log(close / close.shift(1))
    features['Lag_1'] = log_ret
    features['Lag_2'] = log_ret.shift(1)
    features['Lag_3'] = log_ret.shift(2)
    features['Lag_4'] = log_ret.shift(3)
    
    # 9. SMA
    features['SMA'] = ta.trend.SMAIndicator(close=close, window=14).sma_indicator()
    
    # 10. ADX
    features['ADX'] = ta.trend.ADXIndicator(high=high, low=low, close=close, window=14).adx()
    
    # 11. SAR
    features['SAR'] = ta.trend.PSARIndicator(high=high, low=low, close=close).psar()
    
    # 12. ATR
    features['ATR'] = ta.volatility.AverageTrueRange(high=high, low=low, close=close, window=14).average_true_range()
    
    # 13. OBV
    features['OBV'] = ta.volume.OnBalanceVolumeIndicator(close=close, volume=volume).on_balance_volume()
    
    # Target Variable: R_{t+1}
    features['Target_Return'] = log_ret.shift(-1)
    
    return features

def generate_all_features(data_dir='data/valid_from_2010', warmup_weeks=30):
    """
    Builds the 13 raw feature variables for all 28 assets, handles the 30-week warm-up period,
    and returns unscaled clean feature DataFrames.
    Scaling is performed strictly inside the walk-forward validation loop to prevent data leakage.
    """
    price_df, returns_df, raw_ohlcv = load_and_preprocess_data(data_dir)
    
    master_feature_dict = {}
    
    for ticker, df in raw_ohlcv.items():
        # Reindex single asset OHLCV to master weekly calendar
        master_dates = price_df.index
        df_reindexed = df.reindex(master_dates).ffill().bfill()
        
        if ta is not None:
            try:
                feat_df = compute_technical_indicators_ta(df_reindexed)
            except Exception:
                feat_df = compute_technical_indicators_pandas(df_reindexed)
        else:
            feat_df = compute_technical_indicators_pandas(df_reindexed)
            
        # Drop the first 30 warm-up weeks to eliminate initial NaNs from 26-week EMAs & rolling indicators
        # Also drop the very last row which lacks Target_Return R_{t+1}
        feat_df_clean = feat_df.iloc[warmup_weeks:-1].copy()
        
        # Verify zero NaNs remain
        feat_df_clean = feat_df_clean.dropna()
        
        master_feature_dict[ticker] = feat_df_clean
        
        # Save per-asset raw clean features to CSV
        feat_df_clean.to_csv(f'output/processed_features/{ticker}_raw_features.csv')
        
    print(f"Successfully generated raw feature matrices for {len(master_feature_dict)} assets.")
    print(f"Each asset has {len(next(iter(master_feature_dict.values())))} clean weekly feature rows after 30-week warm-up.")
    
    return master_feature_dict

if __name__ == '__main__':
    print("Executing Feature Engineering Pipeline (Raw Features)...")
    master_feat = generate_all_features()
    first_ticker = list(master_feat.keys())[0]
    print(f"\n--- Sample Raw Feature Set ({first_ticker}) ---")
    print(master_feat[first_ticker].head())
    print("\nFeature Engineering Pipeline Complete!")
