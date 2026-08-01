#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 22:17:14 2026

@author: tianyang

S&P 500 constituent-daily price from yahoo finance
Clean for survivorship bias (note limitations)

Compute daily log returns. 
Build the momentum signal: 12-month return, skip most recent month.

Vectorized backtest engine
daily rebalancing, quintile portfolios, long-short returns.

Performance metrics
Sharpe ratio, max drawdown, annualised return, turnover
Plot cumulative returns, drawdown chart, rolling Sharpe.

Reference
Frazzini, Andrea and Moskowitz, Tobias J. and Moskowitz, Tobias J. and Asness, Cliff S. and Israel, Ronen, 
Fact, Fiction and Momentum Investing (May 9, 2014). 
Journal of Portfolio Management, Fall 2014 (40th Anniversary Issue), 
Available at SSRN: https://ssrn.com/abstract=2435323 or http://dx.doi.org/10.2139/ssrn.2435323
"""

import requests
import numpy as np
import pandas as pd
import yfinance as yh 
#%%S&P 500 constituent-daily price from yahoo finance; survivorship bias (note limitations)

url = 'https://en.m.wikipedia.org/wiki/List_of_S%26P_500_companies'
headers = {'User-Agent': 'Mozilla/5.0'}

html = requests.get(url, headers=headers).text
tables = pd.read_html(html)
sp500_table = tables[0]
tickers = sp500_table['Symbol'].tolist()

data = yh.download(tickers, start='2023-01-01', end='2026-07-30') #only has 'Close' price
close = data['Adj Close']
'''3 Failed downloads:
['BRK.B']: possibly delisted; no timezone found
['BF.B', 'BAX']: possibly delisted; no price data found  (1d 2022-01-01 -> 2026-07-30)'''

data['Close'].isna().sum()

#%% Compute daily log returns, monthly cadence return; momentum signal based off of monthly return

price_monthly = data['Close'].resample('ME').last()
return_monthl = price_monthly.pct_change()

# cumulative return index (starting at 1)
total_return_idx = (1 + return_monthl).cumprod()
# Momentum signal for month t: growth from t-12 to t-1
momentum_signal = (total_return_idx.shift(1) / total_return_idx.shift(12)) - 1

#2.
price = data['Close'].resample('ME').last()
momen = price.shift(1).diff(11)/price.shift(12)
#3.
momentum_sgnl = (1+return_monthl).rolling(window=11).apply(np.prod, raw=True) - 1
momentum_sgnl = momentum_sgnl.shift(1) # at t, the signal is of window t-1 to t-11

#%%Vectorized backtest engine
#daily rebalancing, quintile portfolios, long-short returns.

#Performance metrics
#Sharpe ratio, max drawdown, annualised return, turnover
#Plot cumulative returns, drawdown chart, rolling Sharpe.




