from datasource import *
from core import (
    get_remote_cache_conn,
    set_remote_cache_data,
    get_all_remote_cache_data
)

def print_listings(listings: list = [], ctx={}, **kwargs):
    print('print_listings')
    print(listings)

def collect_exchange_info(ctx={}, **kwargs):
    tickers = {}

    supported_listings = get_listings()
    supported_exchange = ['US', 'KO', 'KQ', 'INDX', 'COMM']

    for exchange in supported_exchange:
        tickers[exchange] = get_eod_exchange_info(exchange)

    us_tickers = [d for d in tickers['US'] if d['Code'] in supported_listings]
    tickers['US'] = us_tickers

    total_tickerslist = []

    for exchange in supported_exchange:
        data = tickers[exchange]

        ##### STEP #####
        data_dict = {d['Code']: d for d in data}
        set_remote_cache_data(
            f'SIMPLI_{exchange}_TICKERS_DICT',
            data_dict
        )

        ##### STEP #####
        data_tickerlist = [d['Code'] for _, d in data_dict.items()]
        set_remote_cache_data(
            f'SIMPLI_{exchange}_TICKERS_LIST',
            data_tickerlist
        )

        ##### STEP #####
        data_tickernamelist = [[d['Code'], d['Name']] for _, d in data_dict.items()]
        set_remote_cache_data(
            f'SIMPLI_{exchange}_TICKERSNAME_LIST',
            data_tickernamelist
        )

        ##### STEP #####
        filter_type = ['Preferred Stock', 'Common Stock', 'Preferred Share', 'ETF', 'INDEX', 'Commodity']
        data_filtered_list = []
        for _, val in data_dict.items():
            if val['Type'] in filter_type:

                # 보통주, 우선주, ETF로 한글 명칭으로 바꿔주기
                if val['Type'] == 'Preferred Stock' or val['Type'] == 'Preferred Share':
                    stock_type = '우선주'
                elif val['Type'] == 'Common Stock':
                    stock_type = '보통주'
                elif val['Type'] == 'ETF':
                    stock_type = 'ETF'
                elif val['Type'] == 'INDEX':
                    stock_type = '지수'
                elif val['Type'] == 'Commodity':
                    stock_type = '원자재'

                data_filtered_list.append([
                    val['Code'],
                    val['Name'],
                    exchange,
                    val['Exchange'],
                    val['Currency'],
                    stock_type
                ])
        total_tickerslist = total_tickerslist + data_filtered_list
        set_remote_cache_data(
            f'SIMPLI_{exchange}_FILTERED_TICKERSNAME_LIST',
            total_tickerslist
        )

        ##### STEP #####
        sec_types = list(set(d['Type'] for _, d in data_dict.items()))
        set_remote_cache_data(
            f'SIMPLI_{exchange}_TICKERS_TYPES_LIST',
            sec_types
        )

    set_remote_cache_data(
        'SIMPLI_FILTERED_TICKERSNAMELIST',
        total_tickerslist
    )