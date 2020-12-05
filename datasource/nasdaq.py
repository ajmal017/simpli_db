from ftplib import FTP
import os

from tools.date import get_today_date

def get_listings_from_nasdaq(ctx={}, **kwargs):
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

        nasdaq_fw = open(f'./data/{today}_{nasdaq_listing_file}', 'wb')
        nyse_fw = open(f'./data/{today}_{nyse_listing_file}', 'wb')
        ftp.retrbinary(f'RETR {nasdaq_listing_file}', nasdaq_fw.write)
        ftp.retrbinary(f'RETR {nyse_listing_file}', nyse_fw.write)

    return True

def parse_listing_file(ctx={}, **kwargs):
    pass


if __name__ == '__main__':
    get_listings_from_nasdaq()