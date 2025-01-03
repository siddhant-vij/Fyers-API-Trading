def ema(ohlc_df, window):
    """
    Calculate the exponential moving average (EMA) of a given OHLC data set.

    Parameters
    ----------
    ohlc_df : pd.DataFrame
        The OHLC data set to calculate the EMA of.
    window : int
        The number of periods to use for the EMA calculation.

    Returns
    -------
    pd.Series
        The EMA of the Close price of the data set.
    """
    return ohlc_df['Close'].ewm(span=window, adjust=False).mean()

