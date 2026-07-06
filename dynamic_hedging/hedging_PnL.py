#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 20:49:53 2026

@author: tianyang
"""

import numpy as np
import matplotlib.pyplot as plt
from the_engine import Market, Options, Hedger
    

#P&L impact under transaction cost and hedging thresholds
'''
a. Transaction cost is applied at initial state, rebalancing and final state
With non-zero transaction cost, PnL simulations remain negative. 

b. For delta that is below hedging threshold, the hedging trade is not executed
In experiment, the threholds looked at are [0, 0.005, 0.01, 0.02, 0.05]; 
from this rough estimation, the higher the threshold, 
the smaller magnitude of negative PnL yet the more volatile the PnL simulations appear to be.
With introduction of hedging threshold, the hedging is not as closely aligned, 
so it introduces more uncertainty into the option-stock replication due to unhedged exposure.

'''

    
S0 = 100; K = 90; r = 0; sigma = 1; T = 1; transaction_cost = .001; threshold = 0.01

def PnL_rebalance_TC(N_rebalance, N_simulation):
        
    pnl_list = []
    N = N_rebalance; 
    
    #In 252 business days, simulate hedger P&L for 1000 times and verify their mean 
    for _ in range(N_simulation):
        market = Market(S0 = S0, r = r, sigma = sigma, T = T, N = N)
        options = Options(K=K, T=T, r=r, sigma=sigma)
        hedger = Hedger(market, options, transaction_cost=transaction_cost, threshold=threshold)
        hedger.rebalance()
        pnl = hedger.final_trade()
    
        pnl_list.append(pnl)
        
    print(f'Mean P&L is {np.mean(pnl_list):.3f}')
    print(f'Standard deviation P&L is {np.std(pnl_list):.3f}')
    
    #plt.scatter(range(1000), pnl_list, s=.7)
    plt.hist(pnl_list, bins=50, density=True, alpha=0.7)
    plt.axvline(np.mean(pnl_list), color='pink', linestyle='--', label=f'Mean = {np.mean(pnl_list):.3f}')
    plt.xlabel('Simulated PnL')
    plt.ylabel('Probability Density of PnL')
    plt.title('P&L Distribution')
    plt.legend()
    plt.show()

PnL_rebalance_TC(252, 1000)


def PnL_rebalance_Threshold(N_rebalance, N_simulation, thresholds):
     
     mean_list = []
     stdv_list = []  
     for threshold in thresholds:
         
        pnl_list = []
        
        N = N_rebalance; 
        
        for _ in range(N_simulation):
            market = Market(S0 = S0, r = r, sigma = sigma, T = T, N = N)
            options = Options(K=K, T=T, r=r, sigma=sigma)
            hedger = Hedger(market, options, transaction_cost=transaction_cost, threshold=threshold)
            hedger.rebalance()
            pnl = hedger.final_trade()
        
            pnl_list.append(pnl)
            
        mean_list.append(np.mean(pnl_list))
        stdv_list.append(np.std(pnl_list))
     
     fig, ax1 = plt.subplots()

     ax1.set_xlabel('Threshold')
     ax1.set_ylabel('Pnl Mean', color='palevioletred')
     ax1.plot(thresholds, mean_list, color='palevioletred')
     ax1.tick_params(axis='y', labelcolor='palevioletred')
     
     ax2 = ax1.twinx()
     ax2.set_ylabel('PnL Standard Deviation', color='slategray')
     ax2.plot(thresholds, stdv_list, color='slategray')
     ax2.tick_params(axis='y', labelcolor='slategray')
     
     fig.tight_layout()
        
PnL_rebalance_Threshold(252, 1000, [0, 0.005, 0.01, 0.02, 0.05])
