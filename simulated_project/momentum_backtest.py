#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 14:03:47 2026

@author: tianyang
"""

import matplotlib.pyplot as plt
import numpy as np
from momentum_S5 import momentum

url = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv'
start='2023-01-01'
end='2026-07-30'

momentum = momentum(start, end, url)  
momentum_signal = momentum.generate_signal()
#long_short, with_signal = momentum.backtest_momentum()
strategy, with_signal = momentum.backtest_momentum()
strategy_vol_target = momentum.volatility_targeting()

metrics, cumulative = momentum.performance_evaluation(strategy_vol_target, VaR_threshold=.5)
sharpe = metrics['Sharpe Ratio'].values

# Visualisation
rolling_period = 6
rolling_sharpe = strategy_vol_target.rolling(rolling_period).mean() \
                /strategy_vol_target.rolling(rolling_period).std() * np.sqrt(12)

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
plt.title('W minus L Performance')
plt.show()
