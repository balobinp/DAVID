import david_currency_check as dcc

status, df = dcc.get_iis_shares(market='foreign', tickers=dcc.tickers_foreign)
print(df.sort_values(by='SECID'))

status, df = dcc.get_iis_shares(market='russian', tickers=dcc.tickers_russian)
print(df.sort_values(by='SECID'))