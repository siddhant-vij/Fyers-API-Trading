def shooting_star(ohlc_df):
    """
    Identifies shooting star candlestick patterns in a DataFrame and adds a 'ShootingStar' column.

    Parameters
    ----------
    ohlc_df : pd.DataFrame
        A DataFrame containing the Open, High, Low, Close columns.

    Returns
    -------
    pd.DataFrame
        The original DataFrame with a new 'ShootingStar' column indicating the presence of a shooting star pattern.
    """
    df = ohlc_df.copy()
    shooting_star_values = []

    for _, row in df.iterrows():
        # Check for a bearish shooting star pattern
        if (row["Open"] - row["Close"] > 0) and (row["High"] - row["Open"] >= 2 * (row["Close"] - row["Low"])):
            shooting_star_values.append(True)
        # Check for a bullish shooting star pattern
        elif (row["Close"] - row["Open"] > 0) and (row["High"] - row["Close"] >= 2 * (row["Open"] - row["Low"])):
            shooting_star_values.append(True)
        else:
            shooting_star_values.append(False)

    df["ShootingStar"] = shooting_star_values
    return df
