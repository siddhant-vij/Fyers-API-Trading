def atr(DF,n):
    # function to calculate True Range and Average True Range
    df = DF.copy()
    df['High-Low']=abs(df['High']-df['Low'])
    df['High-PrevClose']=abs(df['High']-df['Close'].shift(1))
    df['Low-PrevClose']=abs(df['Low']-df['Close'].shift(1))
    df['TR']=df[['High-Low','High-PrevClose','Low-PrevClose']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].ewm(com=n,min_periods=n).mean()
    df.dropna(inplace=True)
    return df
