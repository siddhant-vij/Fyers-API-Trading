def trend(df):
    trend = None

    i = len(df) -1
    # Uptrend condition
    if df['Close'][i] > df['Open'][i] and df['Close'][i-1] > df['Open'][i-1] and df['Close'][i-2] > df['Open'][i-2] and\
            df['High'][i] > df['High'][i - 1] and df['High'][i - 1] > df['High'][i - 2] and \
            df['Low'][i] > df['Low'][i - 1] and df['Low'][i - 1] > df['Low'][i - 2]:
        trend = 'Uptrend'

    # Downtrend condition
    elif df['Close'][i] < df['Open'][i] and df['Close'][i-1] < df['Open'][i-1] and df['Close'][i-2] < df['Open'][i-2] and\
            df['High'][i] < df['High'][i - 1] and df['High'][i - 1] < df['High'][i - 2] and\
            df['Low'][i] < df['Low'][i - 1] and df['Low'][i - 1] < df['Low'][i - 2] :
        trend = 'Downtrend'

    else:
        trend = None

    return trend