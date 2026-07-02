#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 19:06:27 2026

@author: tianyang

This dynamic hedging engine simulates 
stock movement, European-style options and Greeks evolvement, order execution and P&L monitoring
enabled by Market, Options and Hedger, the three fundamental classes. 

Goals
simulate cost of continuously delta‑hedging a short option equals the Black‑Scholes price,

Convey final P&L converges to zero (minus transaction costs) when the stock follows the risk‑neutral process.

"""

import numpy as np
#import matplotlib.pyplot as plt
from scipy.stats import norm


    
class Market:   
    
    '''
    Goal
    Simulate stock price via Geometric Brownian Motion

    Note
    Log-transform GBM from exponential format to implement in vectorised additive manner
    '''
    
    def __init__(self, S0, r, sigma, T, N, seed=None):
        '''
        mu referenced in St simulation follows risk-neutral measurement
        '''
        self.S0 = S0
        self.T = T
        self.sigma = sigma
        self.mu = r
        self.N = N
        self.rng = np.random.default_rng(seed)#mean, sigma, size

    def BM_Bt(self):
        '''
        Underlying dBt term in Brownian Motion, Bt = sum_{i=0}^{n} Xi
        referenced in St diffusion,
        dWt^2 = dt per Quadratic Variation
        sigma=(T/N)^0.5 scaling factor for Var(Bt)=T and per Qudratic Variation
        '''
        
        dBt = self.rng.normal(0, (self.T/self.N)**0.5, self.N) #CORRECTION mean=0
        Bt = np.zeros(self.N+1)
        Bt[1:] = np.cumsum(dBt)
        
        return dBt, Bt
    
    def GBM_St(self,step):
        '''
        Y = lnX
        St = X = e^Y
        
        dXt = mu * Xt * dt + sigma * Xt * dBt      --- underlying dXt via ito's lemma, multiplicative Xt following GBM
        dY = (mu - .5*sigma**2) dt + sigma dBt     --- independent dY from Y_n-1
        '''
        
        dBt, Bt = self.BM_Bt()
        dt = self.T/self.N
        
        drift_Y = (self.mu - 0.5*self.sigma**2) * dt
        diffn_Y = self.sigma * dBt
        
        Y = np.zeros(self.N+1)
        Y[0] = np.log(self.S0)
        Y[1:] = np.log(self.S0) + np.cumsum(drift_Y+diffn_Y) # additive BM observed from dY that relies on initial dt and dBt
        
        return np.exp(Y)[step]
    
    def GBM_St_terminal(self):
        
        Z = self.rng.normal(0, 1)
        St = self.S0 * np.exp((self.mu - 0.5 * self.sigma**2) * self.T
                             + self.sigma * np.sqrt(self.T) * Z)
        return St


        
class Options:
    '''
    Goal
    Simulate current price of the option
    Illustrate current delta (and other Greeks)

    Notes
    Following risk-neutral measurement Q, Black-Scholes assumes drift-term of St is upon r
    Stock simulation in class Market shares risk-free rate r for St drift
    Ct = e^(-rt) (FN(d1)-KN(d2))
    '''
    
    def __init__(self, K, T, r, sigma, seed=None):
        
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.rng = np.random.default_rng(seed)
    
    def d1(self, St, t):
        
        nom = np.log(St/self.K) + (self.r+self.sigma**2/2)*(self.T-t)
    
        dem = self.sigma*(self.T-t)**0.5
        
        return nom/dem
        
    def eu_call_BS(self, St, t):
        
        d1 = self.d1(St,t)
        d2 = d1 - self.sigma*(self.T-t)**0.5
        
        Nd1 = norm.cdf(d1)
        Nd2 = norm.cdf(d2)
        
        C = np.exp(-self.r*(self.T-t)) * (St*Nd1 - self.K*Nd2)
        
        return C
    
    def Delta(self, t):
        
        d1 = self.d1(St, t)
        
        return norm.cdf(d1)
    
    
class Hedger:
    
    def __init__(self, market, option, N_steps):
        
        self.market = market
        self.option = option
        self.N = market.N
        self.dt = market.T/market.N
        self.stock = 0.0
        self.cash = 0.0
        self.short_call = True #option sell perspective
        
        #set up at t = 0
        S0 = market.GBM_St(0)
        self.cash = option.eu_call_BS(S0, 0)
        target_delta = option.Delta(0)
        self.cash -= S0 * target_delta
        self.stock = target_delta
        print(f'PRINT{self.cash}, {target_delta}')

    def rebalance():
        pass
    
S0 = 100
K = 90
r = 0
sigma = 1
T = 1
N = 252

market = Market(S0 = S0, r = r, sigma = sigma, T = T, N = N)
#t = np.linspace(0, T, N)
St = market.GBM_St(0)
options = Options(K=K, T=T, r=r, sigma=sigma)
options.eu_call_BS(100, t=0.0)
options.Delta(t=0)

hedger = Hedger(market, options, N)
        
        
        
        
        
        
        
        
        