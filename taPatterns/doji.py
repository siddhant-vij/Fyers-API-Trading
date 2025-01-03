def doji(ohlc_df):
    """
    Returns a DataFrame with a 'Doji' column, a boolean indicating whether a given row is a Doji candle.

    Parameters
    ----------
    ohlc_df : pd.DataFrame
        A DataFrame containing the Open, High, Low, Close columns.

    Returns
    -------
    pd.DataFrame
        The original DataFrame with a new 'Doji' column.
    """
    df = ohlc_df.copy()
    doji_values = []
    for _, row in df.iterrows():
        if abs(row["Open"] - row["Close"]) <= 0.2 * (row['High'] - row['Low']):
            doji_values.append(True)
        else:
            doji_values.append(False)
    df["Doji"] = doji_values
    return df
