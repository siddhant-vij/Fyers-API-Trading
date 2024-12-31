import os
import datetime as dt
import pandas as pd
from fyers_apiv3 import fyersModel
import pytz

client_id = open(f"{os.getcwd()}/auth/secrets/fyers_appid.txt", 'r').read()
access_token = open(f"{os.getcwd()}/auth/secrets/fyers_token.txt", 'r').read()

fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, is_async=False, log_path=f"{os.getcwd()}/data/historical/logs")

def fetchOHLCV(ticker, start_date, end_date, interval="1"):
    from_date = dt.datetime.strptime(start_date, '%Y-%m-%d')
    to_date = dt.datetime.strptime(end_date, '%Y-%m-%d')

    candles_list = []

    while True:
        from_date_string = from_date.strftime("%Y-%m-%d")
        to_date_string = to_date.strftime("%Y-%m-%d")

        if from_date.date() >= (to_date.date() - dt.timedelta(100)):
            data = {
                "symbol": ticker,
                "resolution": interval,
                "date_format": "1",
                "range_from": from_date_string,
                "range_to": to_date_string,
                "cont_flag": "1"
            }
            resp = fyers.history(data=data).get("candles", [])            
            candles_list.extend(resp)            
            break
        else:
            chunk_end = from_date + dt.timedelta(100)
            chunk_end_string = chunk_end.strftime("%Y-%m-%d")
            data = {
                "symbol": ticker,
                "resolution": interval,
                "date_format": "1",
                "range_from": from_date_string,
                "range_to": chunk_end_string,
                "cont_flag": "1"
            }
            resp = fyers.history(data=data).get("candles", [])
            candles_list.extend(resp)
            from_date = chunk_end + dt.timedelta(1)

    columns = ["Timestamp", "Open", "High", "Low", "Close", "Volume"]
    df = pd.DataFrame(candles_list, columns=columns)

    df["Timestamp2"] = pd.to_datetime(df["Timestamp"], unit="s").dt.tz_localize(pytz.utc)
    ist = pytz.timezone("Asia/Kolkata")
    df["Timestamp2"] = df["Timestamp2"].dt.tz_convert(ist)

    df.drop(columns=['Timestamp'], inplace=True)
    df.set_index('Timestamp2', inplace=True)
    df.index.name = "Timestamp"

    return df


def resampleOHLCV(df, interval):
    df_interval = df.resample(interval).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    })
    df_interval.dropna(inplace=True)
    return df_interval


if __name__ == "__main__":
    ticker = "NSE:SBIN-EQ"
    start_date = "2022-01-01"
    end_date = "2023-01-01"

    # Fetching 1m candles from API... 
    df_result = fetchOHLCV(ticker, start_date, end_date)

    # Save the data to a CSV file/Integrate a database here... 
    filename = f"{ticker.replace(':','_')}_1m_{start_date}_{end_date}.csv"
    df_result.to_csv(f"{os.getcwd()}/data/historical/db/{filename}")
    print(f"Data fetched and saved to data/historical/db/{filename}")

    # Resample 1m candles to bigger interval candles - read 1m from DB...
    # 1m -> 15 minutes
    df_15min = resampleOHLCV(df_result, "15min")
    filename = f"{ticker.replace(':','_')}_15m_{start_date}_{end_date}.csv"
    df_15min.to_csv(f"{os.getcwd()}/data/historical/db/{filename}")
    print(f"Data fetched and saved to data/historical/db/{filename}")

    # 1m -> 1 hour (from 9am)
    df_1h_9 = resampleOHLCV(df_result, "h")
    filename = f"{ticker.replace(':','_')}_1h_9_{start_date}_{end_date}.csv"
    df_1h_9.to_csv(f"{os.getcwd()}/data/historical/db/{filename}")
    print(f"Data fetched and saved to data/historical/db/{filename}")
    
    # 1m -> 1 hour (from 9:15am)
    df_1h = df_result[df_result.index.time <= pd.Timestamp('15:30').time()]
    df_1h.index = df_1h.index - pd.Timedelta(minutes=15)
    df_1h_9_15 = resampleOHLCV(df_1h, "h")
    df_1h_9_15.dropna(inplace=True)
    df_1h_9_15.index = df_1h_9_15.index + pd.Timedelta(minutes=15)
    filename = f"{ticker.replace(':','_')}_1h_9_15_{start_date}_{end_date}.csv"
    df_1h_9_15.to_csv(f"{os.getcwd()}/data/historical/db/{filename}")
    print(f"Data fetched and saved to data/historical/db/{filename}")

    # 1m -> 1 day
    df_1day = resampleOHLCV(df_result, "D")
    filename = f"{ticker.replace(':','_')}_1d_{start_date}_{end_date}.csv"
    df_1day.to_csv(f"{os.getcwd()}/data/historical/db/{filename}")
    print(f"Data fetched and saved to data/historical/db/{filename}")
