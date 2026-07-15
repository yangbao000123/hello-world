#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 19:18:37 2026

@author: tianyang

Heston Model, stochastic volatility
a. St and vt, 13 July
b. Monte-Carlo multi-path European call pricer, 14 July
c. Implied volatility and plots
"""


import numpy as np


class Heston_Volatility:
    
    '''
    UNDER Q-probability measurement
    dSt = mu*St*dt + vt**0.5*St*dWt^S
    dvt = k(theta-vt)dt + sigmav*vt**0.5*dWt^v
   vt+i = vti + kappa(theta - vti)*deltat + sigmav (vti)**0.5 *dWtv; max(vt,0)
   St+i = Sti + rSti*deltat + vti**0.5 Sti dWtS
   
    Parameters
     kappa: rate at which volatility mean-reverts to its long-term average
     theta: long-run average variance of asset
    sigmav: volatility of variance process
       rho: correlation coefficient between the asset price shocks and volatility shocks
        v0: initial variance of asset
    '''
    

    def __init__(self, T, N, rho, kappa, theta, sigma_v, v0, r, S0):
        
        self.T = T
        self.N = N
        self.rho = rho
        self.kappa = kappa
        self.theta = theta
        self.sigma_v = sigma_v
        self.v0 = v0
        self.r = r
        self.S0 = S0
        
        self.dt = self.T/self.N
        self.rng = np.random.default_rng()
    
    def St_heston_simu(self, n_paths):
        '''
        Vectorise large-number path simulations for St
        Maintain time-wise loop for St and Vt
        '''
        
        S = np.full(n_paths, self.S0, dtype=float)
        v = np.full(n_paths, self.v0, dtype=float)
        
        Z1 = self.rng.normal(0, 1, size = (n_paths, self.N))
        Z2 = self.rng.normal(0, 1, size = (n_paths, self.N))
    
        dWtS = self.dt**0.5*Z1                                          #array of N~(0,1)
        dWtv = self.dt**0.5 * (self.rho*Z1+(1-self.rho**2)**0.5*Z2)     #delta volatility, correlated with delta S
        
        for t in range(self.N):
            
            v_left = v                                                  #v at one-previous step, update once St is calculated
            v = np.maximum(v + self.kappa*(self.theta - v)*self.dt + self.sigma_v*np.maximum(v,0)**0.5*dWtv[:, t], 0)
            
            S = S + self.r*S*self.dt + v_left**0.5*S*dWtS[:,t]          #simualte S using v_t-1 to maintain correlation
            
        return S #n_paths simulation, each with N (time)steps
    
    def European_Call_MC_simu(self, K, n_paths):
        
        S_n_paths = self.St_heston_simu(n_paths)
        payoff_np = np.maximum(S_n_paths - K, 0)
        Call_MC = np.exp(-self.r*self.T)*np.mean(payoff_np)
        
        return Call_MC
    
    def St_heston(self):
        
        St = np.zeros(N+1); St[0] = self.S0
        Vt = np.zeros(N+1); Vt[0] = self.v0
        
        for i in range(self.N):
            Z1 = self.rng.normal(0, 1)              #N~(0,1)
            Z2 = self.rng.normal(0, 1)              #CORRECTION from N~(0, deltat**0.5); 
                                                    #error causes dWt~N(0, dt**2) with significantly smaller stdev
            dWtS = (self.dt)**0.5*Z1                #N~(0,deltat**0.5)
            dWtv = (self.dt)**0.5*(self.rho*Z1+(1-self.rho**2)**0.5*Z2)
            Vt[i+1] = np.maximum(Vt[i] + self.kappa * (self.theta - Vt[i]) * self.dt + self.sigma_v * np.maximum(Vt[i]**0.5,0) * dWtv,0)
            St[i+1] = St[i] + self.r * St[i] * self.dt + Vt[i]**0.5 * St[i] * dWtS
        
        return St
    
    def European_Call_MC(self, K, n_paths):
        
        St_MC = np.zeros(n_paths)
        payoff = np.zeros(n_paths)
        
        for n in range(n_paths):
            St = self.St_heston()[-1]
            call_payoff = np.maximum(St - K,0)
            
            St_MC[n] = St
            payoff[n] = call_payoff

            #rint(St, call_payoff)
        call_MC = np.exp(-self.r*self.T) * np.mean(payoff)
        
        return call_MC
    
T = 1; N = 252; rho = -0.7; kappa = 0.1; theta = 0.12
sigmav = 0.5; v0 = .3; r = 0.1; S0=100

heston = Heston_Volatility(T=T, N=N, rho=rho, kappa=kappa, theta=theta, 
                           sigma_v = sigmav, v0 = v0, r = r, S0 = S0)
St_single = heston.St_heston()
european_C = heston.European_Call_MC(90, 1000)
eu_MC = heston.European_Call_MC_simu(90, 10000)
print(np.mean(heston.St_heston_simu(1000)))
print(european_C)
print(eu_MC)
#print(f"Risk-neutral expectation for St is {S0 * np.exp(r*T):.3f}")


#%% Heston SDE simulation
#Monte Carlo European Call Pricer



n_p = 10000
ST = np.zeros(n_p)
for each in range(n_p):             
       
    St = np.zeros(N+1); 
    Vt = np.zeros(N+1)
    St[0] = S0; Vt[0] = v0
    
    for i in range(N):
        Z1 = rng.normal(0, 1)       #N~(0,1)
        Z2 = rng.normal(0, 1)       #CORRECTION from N~(0, dt**0.5); 
                                    #error causes dWt~N(0, dt**2) with significantly smaller stdev
        dWtS = (dt)**0.5*Z1         #N~(0,deltat**0.5)
        dWtv = (dt)**0.5*(rho*Z1+(1-rho**2)**0.5*Z2)
        Vt[i+1] = np.maximum(Vt[i] + kappa * (theta - Vt[i]) * dt + sigmav * Vt[i]**0.5 * dWtv,0)
        St[i+1] = St[i] + r * St[i] * dt + Vt[i]**0.5 * St[i] * dWtS
    ST[each] = St[-1]
print("Mean S_T:", np.mean(ST)) 
print(f"Risk-neutral expectation for St is {S0 * np.exp(r*T):.3f}")

#%%
#vt+i = vti + kappa(theta - vti)*deltat + sigmav (vti)**0.5 *dWtv; max(vt,0)
#St+i = Sti + rSti*deltat + vti**0.5 Sti dWtS

Z1 = np.random.normal(mu_dWtS, 1, N)
Z2 = np.random.normal(mu_dWtS, 1, N)

dWtS = (dt)**0.5*Z1
dWtv = (dt)**0.5*(rho*Z1+(1-rho**2)**0.5*Z2)

St = np.zeros(N+1); Vt = np.zeros(N+1)
St[0] = S0; Vt[0] = v0

for i in range(N):
    
    #volatility has floor 0, as being standard deviation**2
    Vt[i+1] = max(Vt[i] + kappa * (theta - Vt[i]) * dt + sigmav * Vt[i]**0.5 * dWtv[i], 0)
    St[i+1] = St[i] + r * St[i] * dt + Vt[i]**0.5 * St[i] * dWtS[i]

print(St[-1])













#NOTES and First Attempt
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

corr = 0.9
vdWtS = sigma_dWts**2       #INCORRECT, dWt standard deviation == deltat**0.5
vdWtv = 0.6                 #INCORRECT, dWt standard deviation == deltat**0.5
#covrn = vdWtS*vdWtv*corr
covMx = [[vdWtS**2, vdWtS*vdWtv*corr],[vdWtS*vdWtv*corr, vdWtv**2]]    #INCORRECT, design correlation matrix with rho
L_chk = np.linalg.cholesky(covMx)

#random shocks to dWtS and dWtv are not introduced and dWtS dimension is off
dWtS = np.random.normal(loc=mu_dWtS, scale=sigma_dWts, size=(len(covMx),N)) 
dWtv = L_chk@dWtS
S0 = 100; mu_St = 0; sigma_St = 1.0; 
#terminal St is not appropraite; 
#intermediate St is needed to incorporate Heston SDE, with volatility at each step

#vt+i = vti + kappa(theta - vti)*deltat + sigmav (vti)**0.5 *dWtv; max(vt,0)
#St+i = Sti + rSti*deltat + vti**0.5 Sti dWtS

St= 100 * np.exp(mu_St - 0.5 * sigma_St**2) * T + sigma_St*(T**0.5)*dWtS[0]








