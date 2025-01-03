def rsi(df, period):
    """
    Calculate the Relative Strength Index (RSI) for a DataFrame with closing price data.

    Parameters:
        df (pd.DataFrame): DataFrame containing OHLC (Open, High, Low, Close) data.
        period (int): Number of periods for RSI calculation (default: 14).

    Returns:
        pd.DataFrame: DataFrame with RSI values added as a new column.
    """
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    df['rsi'] = rsi
    return df
