def hammer(ohlc_df):
    """
    Identifies hammer candlestick patterns in a DataFrame and adds a 'Hammer' column.

    Parameters
    ----------
    ohlc_df : pd.DataFrame
        A DataFrame containing the Open, High, Low, Close columns.

    Returns
    -------
    pd.DataFrame
        The original DataFrame with a new 'Hammer' column indicating the presence of a hammer pattern.
    """
    df = ohlc_df.copy()
    hammer_values = []
    for _, row in df.iterrows():
        # Check for a bearish hammer pattern
        if (row["Open"] - row["Close"] > 0) and (row["Open"] - row["Low"] >= 2 * (row["High"] - row["Close"])):
            hammer_values.append(True)
        # Check for a bullish hammer pattern
        elif (row["Close"] - row["Open"] > 0) and (row["Close"] - row["Low"] >= 2 * (row["High"] - row["Open"])):
            hammer_values.append(True)
        else:
            hammer_values.append(False)
    df["Hammer"] = hammer_values
    return df
