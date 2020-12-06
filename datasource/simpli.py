from core.dependencies import request_url
from datasource.nasdaq import get_nasdaq_listings

def get_simpli_info(ctx={}, **kwargs):
    info_url = 'http://api.simpli.kr/info/?token=blendedrequesttoken'
    res = request_url(info_url)
    data = res.json()['data']
    return data

def get_simpli_listings(ctx={}, **kwargs):
    data = get_simpli_info()

    filter_exchange = ['NYSE', 'NASDAQ', 'NYSE MKT', 'NYSE ARCA']
    filter_type = ['Preferred Stock', 'Common Stock', 'Preferred Share', 'ETF', 'INDEX']
    
    filtered_code = []
    for _, info in data.items():
        exchange_filter = info['Exchange'] in filter_exchange
        type_filter = info['Type'] in filter_type
        if exchange_filter and type_filter:
            filtered_code.append(info)

    return [info['Code'] for info in filtered_code]

def get_listings(ctx={}, **kwargs) -> list:
    simpli_listings = set(get_simpli_listings())
    nasdaq_listings = set(get_nasdaq_listings())

    listings = simpli_listings.intersection(nasdaq_listings)
    listings = sorted(list(listings))

    return listings

               
if __name__ == '__main__':
    get_simpli_listings()