def bullish_engulfing(ohlc_df):
    """
    Identifies bullish engulfing candlestick patterns in a DataFrame and adds a 'BullishEngulfing' column.

    Parameters
    ----------
    ohlc_df : pd.DataFrame
        A DataFrame containing the Open, High, Low, Close columns.

    Returns
    -------
    pd.DataFrame
        The original DataFrame with a new 'BullishEngulfing' column indicating the presence of a bullish engulfing pattern.
    """
    df = ohlc_df.copy()
    bullish_engulfing_values = [False]
    for i in range(1, len(df)):
        previous_row = df.iloc[i - 1]
        current_row = df.iloc[i]
        # Check the conditions for a bullish engulfing pattern
        if (previous_row["Open"] > previous_row["Close"]) and \
                (current_row["Open"] < current_row["Close"]) and \
                (current_row["Open"] <= previous_row["Close"]) and \
                (current_row["Close"] >= previous_row["Open"]):
            bullish_engulfing_values.append(True)
        else:
            bullish_engulfing_values.append(False)
    df["BullishEngulfing"] = bullish_engulfing_values
    return df

def bearish_engulfing(ohlc_df):
    """
    Identifies bearish engulfing candlestick patterns in a DataFrame and adds a 'BearishEngulfing' column.

    Parameters
    ----------
    ohlc_df : pd.DataFrame
        A DataFrame containing the Open, High, Low, Close columns.

    Returns
    -------
    pd.DataFrame
        The original DataFrame with a new 'BearishEngulfing' column indicating the presence of a bearish engulfing pattern.
    """
    df = ohlc_df.copy()
    bearish_engulfing_values = [False]
    for i in range(1, len(df)):
        previous_row = df.iloc[i - 1]
        current_row = df.iloc[i]
        # Check the conditions for a bearish engulfing pattern
        if (previous_row["Open"] < previous_row["Close"]) and \
                (current_row["Open"] > current_row["Close"]) and \
                (current_row["Open"] >= previous_row["Close"]) and \
                (current_row["Close"] <= previous_row["Open"]):
            bearish_engulfing_values.append(True)
        else:
            bearish_engulfing_values.append(False)
    df["BearishEngulfing"] = bearish_engulfing_values
    return df
