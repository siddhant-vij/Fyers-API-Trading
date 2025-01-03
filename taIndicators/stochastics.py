def stochastics(data, lookback_period=14):
  """
  Calculate the Stochastic Oscillator for a given DataFrame.

  Parameters:
  data (pd.DataFrame): DataFrame containing 'High', 'Low', and 'Close' price columns.
  lookback_period (int): Lookback period for the Stochastic Oscillator calculation.

  Returns:
  pd.DataFrame: DataFrame with additional 'K' and 'D' columns representing the Stochastic Oscillator values.
  """
  K = []
  D = []

  for i in range(len(data)):
    if i >= lookback_period:
      highest_high = 0
      lowest_low = float('inf')
      for j in range(lookback_period):
        highest_high = max(highest_high, data.loc[i-j, "High"])
        lowest_low = min(lowest_low, data.loc[i-j, "Low"])

      k_value = (data.loc[i, "Close"] - lowest_low) * 100 / (highest_high - lowest_low)
      K.append(k_value)

      if i >= lookback_period + 3:
        d_value = (K[i] + K[i-1] + K[i-2]) / 3
        D.append(d_value)
      else:
        D.append(0)
    else:
      K.append(0)
      D.append(0)

  data['K'] = K
  data['D'] = D
  return data