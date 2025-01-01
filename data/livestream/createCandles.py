import os
import threading
from queue import Queue
from datetime import datetime
from csv import DictWriter
from fyers_apiv3.FyersWebsocket import data_ws

client_id = open(f"{os.getcwd()}/auth/secrets/fyers_appid.txt", 'r').read()
access_token = open(f"{os.getcwd()}/auth/secrets/fyers_token.txt", 'r').read()

tick_queue = Queue()

minute_data = {}
minute_data_lock = threading.Lock()

last_processed_minute = None

def generate_csv(csv_name, field_names, row_dict):
    folder_path = f"{os.getcwd()}/data/livestream/db"
    csv_file = f"{folder_path}/{csv_name}.csv"

    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)

    write_header = not os.path.isfile(csv_file)

    with open(csv_file, "a", newline="") as obj:
        writer = DictWriter(obj, fieldnames=field_names)
        if write_header:
            print(f"{csv_name} Candle created: data/livestream/db/{csv_name}.csv")
            writer.writeheader()
        writer.writerow(row_dict)

def finalize_candle_for_minute(minute_to_finalize):
    global minute_data

    with minute_data_lock:
        symbol_dict = minute_data.get(minute_to_finalize, {})

        for symbol, price_list in symbol_dict.items():
            if not price_list:
                continue
            o = price_list[0]
            h = max(price_list)
            l = min(price_list)
            c = price_list[-1]

            candle_row = {
                'minute': str(minute_to_finalize),
                'open': o,
                'high': h,
                'low': l,
                'close': c
            }

            csv_name = symbol.replace(":", "_")
            field_names = ['minute', 'open', 'high', 'low', 'close']
            generate_csv(csv_name, field_names, candle_row)

        if minute_to_finalize in minute_data:
            del minute_data[minute_to_finalize]

def onmessage(message):
    if 'exch_feed_time' in message:
        ms = message.get('exch_feed_time', 0)
        curr_time = datetime.fromtimestamp(ms)
        symbol = message.get('symbol')
        ltp = message.get('ltp')
        if symbol and (ltp is not None):
            tick_queue.put((symbol, float(ltp), curr_time))

def onerror(message):
    print("Error:", message)

def onclose(message):
    print("Connection closed:", message)

def candle_main_loop():
    global last_processed_minute
    while True:
        symbol, price, curr_time = tick_queue.get()

        exchange_minute = curr_time.replace(second=0, microsecond=0)

        if last_processed_minute is None:
            last_processed_minute = exchange_minute

        if exchange_minute > last_processed_minute:
            finalize_thread = threading.Thread(
                target=finalize_candle_for_minute,
                args=(last_processed_minute,)
            )
            finalize_thread.start()

            last_processed_minute = exchange_minute

        with minute_data_lock:
            if exchange_minute not in minute_data:
                minute_data[exchange_minute] = {}
            if symbol not in minute_data[exchange_minute]:
                minute_data[exchange_minute][symbol] = []
            minute_data[exchange_minute][symbol].append(price)

def onopen():
    data_type = "SymbolUpdate"
    symbols = ["NSE:SBIN-EQ"]
    fyers.subscribe(symbols=symbols, data_type=data_type)
    fyers.keep_running()


fyers = data_ws.FyersDataSocket(
    access_token=f"{client_id}:{access_token}",
    log_path=f"{os.getcwd()}/data/livestream/logs",
    litemode=False,
    write_to_file=False,
    reconnect=True,
    on_connect=onopen,
    on_close=onclose,
    on_error=onerror,
    on_message=onmessage
)


def main():
    candle_thread = threading.Thread(target=candle_main_loop, daemon=True)
    candle_thread.start()    

    fyers.connect()

    candle_thread.join()

if __name__ == "__main__":
    main()
