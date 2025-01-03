def sma(ohlc_df, window):
    """
    Calculate the simple moving average (SMA) of a given OHLC data set.

    Parameters
    ----------
    ohlc_df : pd.DataFrame
        The OHLC data set to calculate the SMA of.
    window : int
        The number of periods to use for the SMA calculation.

    Returns
    -------
    pd.Series
        The SMA of the Close price of the data set.
    """
    return ohlc_df['Close'].rolling(window).mean()
