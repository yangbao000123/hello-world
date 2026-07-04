#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 20:49:53 2026

@author: tianyang
"""

import numpy as np
import matplotlib.pyplot as plt
from the_engine import Market, Options, Hedger
    
    
S0 = 100; K = 90; r = 0; sigma = 1; T = 1; N = 252

pnl_list = []

for _ in range(1000):
    market = Market(S0 = S0, r = r, sigma = sigma, T = T, N = N)
    options = Options(K=K, T=T, r=r, sigma=sigma)
    hedger = Hedger(market, options)
    hedger.rebalance()
    pnl = hedger.final_trade()

    pnl_list.append(pnl)
    
print(f'Mean P&L is {np.mean(pnl_list):.3f}')
print(f'Standard deviation P&L is {np.std(pnl_list):.3f}')
