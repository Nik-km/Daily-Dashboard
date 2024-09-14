#%% Preliminaries ---------------------------------------------------------------------------------
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yahooFinance
from fredapi import Fred

from dash import Dash, dcc, html
from vizro import Vizro
import vizro.models as vm
import vizro.plotly.express as px

# Set path to working directory of this script file
path_file = os.path.dirname(os.path.abspath(__file__))
os.chdir(path_file)

# Set start date to be 5 years from today
date_current = datetime.today()
date_start = datetime(date_current.year - 5, date_current.month, date_current.day).strftime('%Y-%m-%d')


#%% Import Data -----------------------------------------------------------------------------------

#>> Equities
ticker_stocks = {
    # U.S. Market
    '^GSPC' : 'S&P 500 Index',      # alternative: ^SPX
    '^RUT' : 'Russell 2000',
    '^IXIC' : 'NASDAQ Composite',
    '^DJI' : 'Dow Jones Industrial Average (Dow 30)',
    # Sectoral Indexes
    'XLE' : 'Energy Select Sector SPDR Fund',   # NYSEArca
    '^VIX' : 'CBOE Volatility Index',       # Cboe Indices
    'QQQ' : 'Invesco QQQ Trust',            # NasdaqGM
}

df_equity = yahooFinance.download(list(ticker_stocks.keys()), interval='1wk', start=date_start, keepna=True, rounding=True)
df_equity = df_equity[['Close', 'Volume']]

#>> Currencies
ticker_cur = {
    'CAD=X' : 'USD/CAD',
}

df_cur = yahooFinance.download(list(ticker_cur.keys()), interval='1d', start=date_start, keepna=True, rounding=True)
df_cur = df_cur[['Close', 'Volume']]

#>> Commodities
ticker_com = {
    'CL=F' : 'Crude Oil',                   # NY Mercantile
    'BZ=F' : 'Brent Crude Oil',             # NY Mercantile
    'GC=F' : 'Gold',                        # COMEX
    'ES=F' : 'E-Mini S&P 500',              
    '' : '',
}

df_equity = yahooFinance.download(list(ticker_com.keys()), interval='1wk', start=date_start, keepna=True, rounding=True)
df_equity = df_equity[['Close', 'Volume']]


ticker_futures = {
    '2YY=F' : '2Y Yield Futures',   # CBOT
    'ZN=F' : '10Y T-Note Futures',  # CBOT
    'DX-Y.NYB' : 'US Dollar Index', # ICE Futures
}






#>> Import FRED data series
API_key = open(path_file + "/FRED_api_key_file.txt", "r").read()
fred = Fred(api_key=API_key)

def get_FRED_data(tickers):
    df = pd.DataFrame()
    for k,v in tickers.items():
        series = fred.get_series(k, observation_start=start_date, frequency='m', aggregation_method='eop')
        series.name = v
        df = df.join(series, how='outer')
    return(df)

tickers_daily = {
    'DCOILWTICO' : 'WTI_crude_oil', # Dollars per Barrel
    'DFEDTARU' : 'fed_target_upper', # Federal Funds Target Range - Upper Limit
}

tickers_weekly = {
    'WCOILWTICO' : 'WTI Crude Oil Prices',      # Dollars per Barrel
}



tickers_fred = {
    # Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity
    'DGS2':'2Y Treasury Yield',
    'DGS5':'5Y Treasury Yield',
    'DGS10':'10Y Treasury Yield',
    'DGS30':'30Y Treasury Yield',
    '':'',
    '':'',
    '':'',
    'T10Y2Y':'10Y Treasury Spread',     # 10Y Treasury Constant Maturity - 2Y Treasury Constant Maturity    
    'EXPINF10YR':'expected_cpi',
}
tickers_macro = {
    'GDPC1':'real_gdp',

}

df_FRED = get_FRED_data(tickers_fred)
df_FRED.head()





#%% Notes -----------------------------------------------------------------------------------------
# https://fred.stlouisfed.org/tags/series?t=10-year%3Btreasury

# E-mini S&P 500 Futures - traded on CME; allow traders to gain exposure to the S&P 500 index


# Rates tickers from YahooFinance
# ticker_rates = {
#     '^IRX' : '13W Treasury Bill',   # Cboe Indices
#     '^FVX' : '5Y Treasury Yield',   # Cboe Indices
#     '^TNX' : '10Y Treasury Yield',  # Cboe Indices
#     '^TYX' : '30Y Treasury Yield',  # Cboe Indices
# }



# Load stock returns (Date, Ticker, and Return columns)
# df_SP = yahooFinance.Ticker("^SPX").history(start='1990-01-01', interval='1mo', actions=True)
#df_SP = yahooFinance.Ticker("^GSPC").history(start='1990-01-01', interval='1mo', actions=True)

# Compute monthly log returns
# df_SP["Returns"] = np.log(df_SP["Close"]/df_SP["Close"].shift(1)) * 100
# df_SP = df_SP[["Close", "Volume", "Returns"]]
# print(df_SP.head())

# Extract the date of the first observation
# start_date = datetime.strftime(df_SP.index[0], '%m/%d/%Y'); start_date

# data = yahooFinance.download(ticker_stocks, interval = '1mo', start = '1990-01-01', end = '2024-06-01')



# df_equity.columns
# df_equity.drop(['column_name'], axis=1, inplace=True)
# df_equity = df_equity.droplevel(0, axis=1)  # remove multi-index columns


