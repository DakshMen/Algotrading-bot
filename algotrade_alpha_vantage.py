from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
import pandas as pd
import time

API_KEY = 'HEREJNKZX7BJ0XR6IVCA'

def fetch_alpha_vantage_data(symbol, interval='15min', outputsize='full'):
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    data, meta = ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
    data = data.sort_index()  # Ensure time series is in order
    return data


class MySmaTradingStrategy:
    def __init__(self, swindow, lwindow):
        self.__swindow = swindow
        self.__lwindow = lwindow

    def generate_signal(self, price_data):
        if len(price_data) < self.__lwindow:
            return "Hold"
        short_avg = price_data[-self.__swindow:].mean()
        long_avg = price_data[-self.__lwindow:].mean()
        if short_avg > long_avg:
            return "Buy"
        elif short_avg < long_avg:
            return "Sell"
        else:
            return "Hold"


class MyTrade:
    def __init__(self, strategy_name, signal, amount):
        self.strategy_name = strategy_name
        self.signal = signal
        self.amount = amount
        self.timestamp = datetime.now()

    def execute(self):
        print(f"Executed {self.signal} with strategy '{self.strategy_name}' \
              f"for amount {self.amount} at {self.timestamp}")

class MockTradingAPI:
    def __init__(self, balance):
        self.balance = balance

    def place_order(self, trade, price):
        if trade.signal == "Buy" and self.balance >= trade.amount * price:
            self.balance -= trade.amount * price
            print(f"Placed BUY at {price}, Remaining Balance: {self.balance}")
        elif trade.signal == "Sell":
            self.balance += trade.amount * price
            print(f"Placed SELL at {price}, New Balance: {self.balance}")
        else:
            print("Insufficient Balance or Invalid Signal")


if __name__ == "__main__":
    symbol = "AMZN"
    strategy = MySmaTradingStrategy(5, 20)

    print(f"Fetching {symbol} data from Alpha Vantage...")
    try:
        data = fetch_alpha_vantage_data(symbol)
        close_prices = data['4. close']
        signal = strategy.generate_signal(close_prices)
        print(f"Generated Signal: {signal}")

        trade = MyTrade("SMA Strategy", signal, amount=10)
        trade.execute()

        broker = MockTradingAPI(balance=100000)
        last_price = close_prices.iloc[-1]
        broker.place_order(trade, last_price)
    except Exception as e:
        print(f"Error fetching data: {e}")
