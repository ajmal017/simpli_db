"""
https://github.com/ranaroussi/yfinance
"""
import yfinance as yf

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def get_yahoo_info_data(ticker: str):
    handler = yf.Ticker(ticker)
    return handler.info

def get_yahoo_price_data(ticker: str):
    handler = yf.Ticker(ticker)
    return handler.history(period='max')

if __name__ == '__main__':
    print(get_yahoo_info_data('AAPL'))