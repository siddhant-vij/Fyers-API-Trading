def bollingerBand(DF,window=15, num_std_devs=2):
    # function to calculate Bollinger Bands
    df = DF.copy()
    df["MA"] = df['Close'].rolling(window).mean()
    df["BB_up"] = df["MA"] + df['Close'].rolling(window).std()*num_std_devs
    df["BB_dn"] = df["MA"] - df['Close'].rolling(window).std()*num_std_devs
    df["BB_width"] = df["BB_up"] - df["BB_dn"]
    df.dropna(inplace=True)
    return df
