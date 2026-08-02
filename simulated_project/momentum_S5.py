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
'''by nature of month-end return, 
it means for portfolio simulation, position is entered at next-month beginning timestamp; 
next-month return is to be earned/logged for performance that corresponds with current-month position entered, 
assuming an enter-and-hold for monthly balance
'''

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


#%% Vectorized backtest engine
# daily rebalancing, quintile portfolios, long-short returns.
# each month, rank tickers by momentum signal to find winner and loser, compute monthly W-L return

flattened = momentum_sgnl.reset_index().melt(
    id_vars='Date', 
    var_name='ticker',   #columns aggregated to single column for groupby later
    value_name='signal'  #new column to host ticker's momentum signal score
    )
return_align = return_monthl.shift(-1)
flattened['return_aligned'] = return_align.reset_index().melt(id_vars='Date', var_name='ticker', value_name='return_aligned')['return_aligned']

flattened['decile'] = flattened.groupby('Date')['signal'].transform( # transform adds qcut result to a column with the same index in flattened
    lambda x:pd.qcut(x,10, labels=False, 
                           duplicates='drop') )

top = flattened[flattened['decile']==9].groupby('Date')['return_aligned'].mean()
bottom = flattened[flattened['decile']==0].groupby('Date')['return_aligned'].mean()

long_short = top-bottom

#Performance metrics
#Sharpe ratio, max drawdown, annualised return, turnover
#Plot cumulative returns, drawdown chart, rolling Sharpe.

sharpe = long_short.mean()/long_short.std() * np.sqrt(12)
cumulative = (1+long_short).cumprod() # if log return, cumsum then exp?
max_dd = (cumulative/cumulative.cummax()-1).min()
 


