import pandas as pd
from core.dependencies import get_all_urls_async

async def get_data(tickers: list, ctx={}, **kwargs) -> (pd.DataFrame, pd.DataFrame):
    urls = [f'http://api.simpli.kr/price/{ticker}/?token=blendedrequesttoken' for ticker in tickers]
    res = await get_all_urls_async(*urls)
    return res

def concat(df1: pd.DataFrame, df2: pd.DataFrame, ctx={}, **kwargs) -> int:
    print('start concat')
    print('done concat')
    return 1