def pivotpoints_today(prev_ohlc_data):
    """
    Calculate the current day's pivot point and support/resistance levels from the previous day's OHLC data.

    Parameters:
        prev_ohlc_data (DataFrame): A DataFrame containing the Open, High, Low, and Close prices for the previous day.

    Returns:
        tuple: A tuple containing the pivot point, three resistance levels (r1, r2, r3), and three support levels (s1, s2, s3).
    """
    high = round(prev_ohlc_data["High"].iloc[-1],2)
    low = round(prev_ohlc_data["Low"].iloc[-1],2)
    close = round(prev_ohlc_data["Close"].iloc[-1],2)
    pivot = round((high + low + close)/3,2)
    r1 = round((2*pivot - low),2)
    r2 = round((pivot + (high - low)),2)
    r3 = round((high + 2*(pivot - low)),2)
    s1 = round((2*pivot - high),2)
    s2 = round((pivot - (high - low)),2)
    s3 = round((low - 2*(high - pivot)),2)
    return (pivot,r1,r2,r3,s1,s2,s3)
