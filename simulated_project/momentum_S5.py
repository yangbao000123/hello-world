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
- daily rebalancing, quintile portfolios, long-short returns
- volatility targeting
- covariance shrinkage on weights and Markowitz mean-variance optimizer

Performance metrics
Sharpe ratio, max drawdown, annualised return, turnover
VaR, Expected Shortfall
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
import matplotlib.pyplot as plt
# Gather constituents and calcuate return
'''
S&P 500 constituent-daily price from yahoo finance; 
Survivorship bias
    - collection of constituents as of 07/31/2026 where it contains survived constituents only
    - neglection of historical index rebalance 
Compute daily returns and resampled to monthly cadence return
'''

class momentum:
    
    def __init__(self, start, end, s5_url):
        
        self.start = start
        self.end = end
        self.s5_url = s5_url
        self.price_data = self.get_constituent_price()
        self.return_data = self.price_to_return()
        
        
    def get_constituent_price(self):
        
        '''
        3 Failed downloads:
        ['BRK.B']: possibly delisted; no timezone found
        ['BF.B', 'BAX']: possibly delisted; no price data found  (1d 2022-01-01 -> 2026-07-30)
        '''
        sp500 = pd.read_csv(self.s5_url)
        tickers = sp500['Symbol'].tolist()
        print(tickers)
        data = yh.download(tickers, start=self.start, end=self.end) #only has 'Close' price
        return data
    
    
    def preliminary_check(self):
        
        price_data = self.price_data
        price_data['Close'].isna().sum()
    
    
    def price_to_return(self):
        
        '''
        Return frequency in monthly cadence
        '''
        price_data = self.price_data

        price_monthly = price_data['Close'].resample('ME').last()
        return_monthly = price_monthly.pct_change()

        return return_monthly
    
    
    def generate_signal(self):
        
        '''
        Momentum signal for month t: growth from t-12 to t-1
        
        by nature of month-end return, 
        it means for portfolio simulation, position is entered at next-month beginning timestamp; 
        next-month return is to be earned/logged for performance that corresponds with current-month position entered, 
        assuming an enter-and-hold for monthly balance
        '''
        return_monthly = self.return_data.iloc[1:,:]
        total_return_idx = (1 + return_monthly).cumprod() # why momentum factor from cumulative return 
        momentum_signal = (total_return_idx.shift(1) / total_return_idx.shift(12)) - 1
        
        return momentum_signal
    
    
    def generate_signal_alt1(self):
        
        '''
        Alternative apporach to produce momentum signal
        '''
        price = self.price_data['Close'].resample('ME').last()
        momentum_signal = price.shift(1).diff(11)/price.shift(12)
        
        return momentum_signal
    
    
    def generate_signal_alt2(self):
        
        momentum_signal = (1+self.return_data).rolling(window=11).apply(np.prod, raw=True) - 1
        momentum_signal = momentum_signal.shift(1) # at t, the signal is of window t-1 to t-11
        
        return momentum_signal
    
    
    def backtest_momentum(self):    
        
        '''
        Vectorized backtest engine
        
        daily rebalancing, quintile portfolios, long-short returns.
        each month, rank tickers by momentum signal to find winner and loser, compute monthly W-L return
        
        Pandas syntax
        df.reset_index().melet(): columns aggregated to single df column after groupby
        df.groupby(index)[column].transform(lambda func)
            - transform adds qcut result to a column with the same index in flattened
            - new column to host ticker's momentum signal score
            - benefit over df.groupby(index)[column].apply(lambda func())
                - applied = flattened.groupby('Date')['signal'].apply(lambda x: pd.qcut(x, 2, labels=False, duplicates='drop'))
                - reduction of index handling after producing quantiles
        '''
        momentum_signal = self.generate_signal()
        flattened = momentum_signal.reset_index().melt(
            id_vars='Date', 
            var_name='ticker',          
            value_name='signal'         
            )
        
        return_align = self.return_data.shift(-1)
        flattened['return_aligned'] = return_align.reset_index().melt(id_vars='Date', var_name='ticker', value_name='return_aligned')['return_aligned']
        
        flattened['decile'] = flattened.groupby('Date')['signal'].transform( 
                                                        lambda x:pd.qcut(x,
                                                                         10, #10 quantiles
                                                                         labels=False, 
                                                                         duplicates='drop') )
        
        top = flattened[flattened['decile']==9].groupby('Date')['return_aligned'].mean()
        bottom = flattened[flattened['decile']==0].groupby('Date')['return_aligned'].mean()
        
        long_short = top-bottom
        
        return long_short, flattened
    
    
    def volatility_targeting(self):    
        
        strategy, with_signal = self.backtest_momentum()
        # volatility targeting by adjusting execution trade size
        vol_target = 0.2
        vol_trailng = strategy.rolling(6).std().shift(1)*(12**0.5)
        vol_scalar = vol_target/vol_trailng
        return_vol_target = strategy*vol_scalar
        
        return return_vol_target
    
    
    def performance_evaluation(self, VaR_threshold=0.5):
        
        '''
        Sharpe ratio, max drawdown, annualised return, turnover
        VaR and Expected Shortfall
        Plot cumulative returns, drawdown chart, rolling Sharpe
        '''
        strategy, with_signal = self.backtest_momentum()

        cumulative = (1+strategy).cumprod() # if log return, cumsum then exp?
        sharpe = strategy.mean()/strategy.std() * np.sqrt(12)
        mdd =  (cumulative/cumulative.cummax()-1).min()
        VaR = strategy.quantile(VaR_threshold)
        shortfall = strategy[strategy<=VaR].mean()
        metrics = pd.DataFrame(data=[[sharpe, mdd, VaR, shortfall]], 
                               columns=['Sharpe Ratio', 'Maximum Drawdown', 'VaR', 'Shortfall'])
        
        return metrics, cumulative
    
    
if __name__ == '__main__':
    
    url = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv'
    start='2023-01-01'
    end='2026-07-30'

    #momentum = momentum(start, end, url)  
    #momentum_signal = momentum.generate_signal()
    #long_short, with_signal = momentum.backtest_momentum()
    #metrics, cumulative = momentum.performance_evaluation()
    