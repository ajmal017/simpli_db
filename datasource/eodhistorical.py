import os
import pandas as pd
from enum import Enum
from core.dependencies import request_url
from tools.structure import get_json_data_structure

from dotenv import load_dotenv

load_dotenv()

RESPONSIBILITY = os.getenv('RESPONSIBILITY')
API_KEY = os.getenv(f'API_{RESPONSIBILITY}')


class ExchangeType(str, Enum):
    us = 'US'
    ko = 'KO'
    kq = 'KQ'
    indx = 'INDX'
    comm = 'COMM'


def get_eod_exchange_info(exchange: ExchangeType, ctx={}, **kwargs):
    exchange_url = f'https://eodhistoricaldata.com/api/exchange-symbol-list/{exchange}?fmt=json&api_token={API_KEY}'
    res = request_url(exchange_url)
    return res.json()

def get_eod_market_holidays(exchange: ExchangeType, ctx={}, **kwargs) -> pd.DataFrame:
    url = f'https://eodhistoricaldata.com/api/exchange-details/{exchange}?api_token={API_KEY}&from=1970-01-01'
    res = request_url(url)
    holidays_df = pd.DataFrame.from_dict(res.json()['ExchangeHolidays'], orient='index')
    return holidays_df

def get_eod_price_data(ticker: str, exchange: ExchangeType, ctx={}, **kwargs) -> pd.DataFrame:
    url = f'https://eodhistoricaldata.com/api/eod/{ticker}.{exchange}?fmt=json&api_token={API_KEY}'
    res = request_url(url)
    price_df = pd.DataFrame(res.json())
    return price_df

def get_eod_fundamental_data(ticker: str, exchange: ExchangeType, ctx={}, **kwargs):
    url = f'https://eodhistoricaldata.com/api/fundamentals/{ticker}.{exchange}?fmt=json&api_token={API_KEY}'
    res = request_url(url)
    # Balance_Sheet, Cash_Flow, Income_Statement
    # quarterly, yearly
    structure = get_json_data_structure(res.json()['Financials']['Balance_Sheet']['quarterly'])
    for key, val in structure.items():
        print(key)
        print(val)
        print(len(val[1]))
        print('\n')

def get_eod_dividend_data(ticker: str, exchange: ExchangeType, ctx={}, **kwargs):
    url = f'https://eodhistoricaldata.com/api/div/{ticker}.{exchange}?fmt=json&api_token={API_KEY}'
    res = request_url(url)
    print(res.json())