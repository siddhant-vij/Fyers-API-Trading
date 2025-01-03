def wma(ohlc_df, window, weights):
    """
    Calculate the weighted moving average (WMA) of a given OHLC data set.

    Parameters
    ----------
    ohlc_df : pd.DataFrame
        The OHLC data set to calculate the WMA of.
    window : int
        The number of periods to use for the WMA calculation.

    Returns
    -------
    pd.Series
        The WMA of the Close price of the data set.
    """
    return (ohlc_df['Close'] * weights).rolling(window).sum() / weights.sum()
