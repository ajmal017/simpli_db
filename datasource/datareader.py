"""
https://financedata.github.io/posts/finance-data-reader-users-guide.html
"""
import FinanceDataReader as fdr
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

df_nyse = fdr.StockListing('NYSE')
df_nasdaq = fdr.StockListing('NASDAQ')
df_amex = fdr.StockListing('AMEX')
df_sp500 = fdr.StockListing('SP500')

print(df_nasdaq)