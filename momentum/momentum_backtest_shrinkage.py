#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 14:03:47 2026

@author: tianyang
"""

import matplotlib.pyplot as plt
import numpy as np
from momentum_S5 import momentum
from sklearn.covariance import LedoitWolf

def visualise_performance(strategy, cumulative, sharpe, feature, rolling_window=6):
    
    rolling_sharpe = strategy.rolling(rolling_window).mean() \
                    /strategy.rolling(rolling_window).std() * np.sqrt(12)
    
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Timestamp')
    ax1.set_ylabel('Cumulative Return', color='lightpink')
    ax1.plot(rolling_sharpe.index, cumulative, color='lightpink', linewidth=1.2)
    ax1.tick_params(axis='y', labelcolor='lightpink')
    ax1.tick_params(axis='x', rotation=45)
    ax1.legend(['Cumulative Return'], loc='upper left')
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('Rolling Sharpe', color='lightseagreen')
    ax2.axhline(sharpe, color='lightseagreen', linestyle='--', alpha=0.5)
    ax2.plot(rolling_sharpe.index, rolling_sharpe, color='lightseagreen', linewidth=1.2)
    ax2.tick_params(axis='y', labelcolor='lightseagreen')
    ax2.tick_params(axis='x', rotation=45)
    ax2.legend(['Rolling Sharpe'], loc='upper right')
    
    
    fig.tight_layout()
    plt.title(f'W minus L Performance, {feature}')
    plt.show()

url = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv'
start='2023-01-01'
end='2026-07-30'

momentum = momentum(start, end, url)  
momentum_signal = momentum.generate_signal()
#long_short, with_signal = momentum.backtest_momentum()
strategy_plain, with_signal = momentum.backtest_momentum()
metrics_plain, cumulative_plain = momentum.performance_evaluation(strategy_plain, VaR_threshold=.5)
sharpe_plain = metrics_plain['Sharpe Ratio'].values


strategy_vol_target = momentum.volatility_targeting()
metrics_vol, cumulative_vol = momentum.performance_evaluation(strategy_vol_target, VaR_threshold=.5)
sharpe_vol = metrics_vol['Sharpe Ratio'].values

# Visualisation

visualise_performance(strategy_vol_target, cumulative_vol, sharpe_vol, 'with volatility targeting')
visualise_performance(strategy_plain, cumulative_plain, sharpe_plain, 'in plain')

#%%
# Ledoit Wolf shrinkage, June 2026
June2026 = momentum.return_data.loc['2026-06-30',:]
daily_return = momentum.price_data['Close'].pct_change().replace(np.nan, 0)
ticker_top = with_signal[(with_signal['Date'] == '2026-06-30') & (with_signal['decile'] == 9)]['ticker']
return_top = daily_return.loc['2025-07-01':'2026-06-30', ticker_top].dropna(how='all')

lw = LedoitWolf()
lw.fit(return_top)
shrinkage = lw.covariance_

cov_inve = np.linalg.inv(shrinkage)
ones= np.ones(len(cov_inve))
weights = cov_inve @ ones / (ones @ cov_inve @ ones)

var_equal = (1/len(weights))**2 * np.sum(shrinkage)
var_mv = weights @ shrinkage @ weights
print(var_equal, var_mv)