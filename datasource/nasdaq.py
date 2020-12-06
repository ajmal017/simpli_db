from ftplib import FTP
import os

from tools.date import get_today_date

def make_nasdaq_listings(ctx={}, **kwargs):
    if not os.path.exists('./data'):
        os.makedirs('./data')

    today = get_today_date()

    nasdaq_listing_file = 'nasdaqlisted.txt'
    nyse_listing_file = 'otherlisted.txt'

    if not os.path.isfile(f'./data/{today}_{nasdaq_listing_file}'):
        ftp_url = 'ftp.nasdaqtrader.com'
        ftp = FTP(ftp_url)
        ftp.login()
        ftp.cwd('/SymbolDirectory')
        # print(ftp.dir())

        nasdaq_fw = open(f'./data/{today}_{nasdaq_listing_file}', 'wb')
        nyse_fw = open(f'./data/{today}_{nyse_listing_file}', 'wb')
        ftp.retrbinary(f'RETR {nasdaq_listing_file}', nasdaq_fw.write)
        ftp.retrbinary(f'RETR {nyse_listing_file}', nyse_fw.write)

    return True

def get_nasdaq_listings(ctx={}, **kwargs):
    if make_nasdaq_listings():
        today = get_today_date()

        nasdaq_listing_file = 'nasdaqlisted.txt'
        nyse_listing_file = 'otherlisted.txt'

        nasdaq_fw = open(f'./data/{today}_{nasdaq_listing_file}', 'rb')
        nyse_fw = open(f'./data/{today}_{nyse_listing_file}', 'rb')

        nasdaq_listings = nasdaq_fw.readlines()
        nyse_listings = nyse_fw.readlines()

        drop_types = ['warrant']
        filter_types = [
            'common stock',
            'preferred stock',
            'common shares',
            'ordinary shares',
            'depositary shares'
            'class a',
            'class b',
            'class c',
            'etf'
        ]
        
        filtered_code = []
        for data in [nasdaq_listings, nyse_listings]:
            for i in range(len(data) - 1):
                listing = data[i]
                listing_data = listing.decode('utf-8').split('|')
                code = listing_data[0]
                stock_type = listing_data[1].split('-')[-1].strip().lower()
                filter_in = any((t in stock_type for t in filter_types))
                filter_out = any((t in stock_type for t in drop_types))
                if filter_in and not filter_out:
                    filtered_code.append(code)

        # EOD/Simpli 형식에 맞추기 --> EOD는 $를 -P로 표현
        replace_vals = {
            '$': '-P'
        }
        for key, val in replace_vals.items():
            filtered_code = [code.replace(key, val) for code in filtered_code]

        return filtered_code


if __name__ == '__main__':
    get_nasdaq_listings()