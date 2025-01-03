def bullish_marubozu(ohlc_df, buffer=0.25):
    """
    Identifies bullish marubozu candlestick patterns in a DataFrame and adds a 'BullishMarubozu' column.

    Parameters
    ----------
    ohlc_df : pd.DataFrame
        A DataFrame containing the Open, High, Low, Close columns.
    buffer : float, optional
        A threshold value to account for small price variations (default is 0.25).

    Returns
    -------
    pd.DataFrame
        The original DataFrame with a new 'BullishMarubozu' column indicating the presence of a bullish marubozu pattern.
    """
    df = ohlc_df.copy()
    bullish_marubozu_values = []

    for _, row in df.iterrows():
        # Check if the candle is bullish and the high and low are within the buffer
        if (row["Close"] > row["Open"] and 
            abs(row["High"] - row["Close"]) <= buffer and 
            abs(row["Low"] - row["Open"]) <= buffer):
            bullish_marubozu_values.append(True)
        else:
            bullish_marubozu_values.append(False)
    
    # Add the result as a new column in the DataFrame
    df["BullishMarubozu"] = bullish_marubozu_values
    return df

def bearish_marubozu(ohlc_df, buffer=0.25):
    """
    Identifies bearish marubozu candlestick patterns in a DataFrame and adds a 'BearishMarubozu' column.

    Parameters
    ----------
    ohlc_df : pd.DataFrame
        A DataFrame containing the Open, High, Low, Close columns.
    buffer : float, optional
        A threshold value to account for small price variations (default is 0.25).

    Returns
    -------
    pd.DataFrame
        The original DataFrame with a new 'BearishMarubozu' column indicating the presence of a bearish marubozu pattern.
    """
    df = ohlc_df.copy()
    bearish_marubozu_values = []
    
    for _, row in df.iterrows():
        # Check if the candle is bearish and the high and low are within the buffer
        if (row["Open"] > row["Close"] and 
            abs(row["High"] - row["Open"]) <= buffer and 
            abs(row["Low"] - row["Close"]) <= buffer):
            bearish_marubozu_values.append(True)
        else:
            bearish_marubozu_values.append(False)
    
    # Add the result as a new column in the DataFrame
    df["BearishMarubozu"] = bearish_marubozu_values
    return df
