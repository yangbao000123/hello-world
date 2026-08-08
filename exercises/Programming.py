#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 13:37:15 2026

@author: tianyang

paired programming exercise
"""
'''
17July

Wednesday (1‑2 h): DP focus. Start with the basic three DP problems. Once comfortable, add one new DP problem per week.

Friday (1‑2 h): General algorithms & data structures. Rotate through arrays, hashing, strings, recursion. Use a structured list (e.g., “Top 50 Quant Coding Questions” if available, or the coding questions in the Green Book).

Saturday (part of your deep‑work block): Apply coding to your projects or work on a larger simulation problem (which you’re already great at). This also counts as “coding practice” and reinforces your strength.

+programming paired from prob/stats exercises
'''

#%% TASKS, week 3rd Aug

# sliding window: deque solution ^^^###^^^
# meeting room booking: check same room availability 
# kth hamming number versus Prime Factorization via Trial Division

#%% reversal +++ Carry variable
a=[9,9,9,9,9,9,9]
b=[9,9,9,9]

l1 = a[::-1]
l2 = b[::-1]

a_s =[str(i) for i in l1]; a_str = ''.join(a_s)
b_s =[str(i) for i in l2]; b_str = ''.join(b_s)

res_str = str(int(a_str)+int(b_str))

res_rev = list(res_str[::-1])
res_rev = [int(i) for i in res_rev]

#%% reverse entire string, then individual word

s = "  hello   world  "
rev = [i for i in s.split(' ') if i != ''][::-1]
str_r = ''
each_space = ''
for each in rev:
    each_space = each+' '
    #print(each_space)
    str_r += each_space
    #print(each)
    #final = " ".join(each)
str_r = str_r[:-1]


#%% exponential calc via iterative squaring 
def power(base, exponent):
    
    powered = 1 # x^0
    while exponent > 0: #CORRECTION exponent to be 0, 1 not enough
        if exponent%2==1:
            powered *= base
        base = base**2    #CORRECTION from base = base^2
        exponent //= 2
        print(base, exponent, powered)
    return powered
    
print(power(2, 10))

'''
powered = 1
expo = 10, powered = 1, base = 4, expo = 5, 
expo = 5, powered = 1*4, base = 4**2, expo = 2 

square the base
base^2 <> base**2
'''
#%% e^pi versus pi^e
# https://math.stackexchange.com/questions/7892/comparing-pie-and-e-pi-without-calculating-themzz
# a. apply natual log to both sides and concavity of ln, x-1 > lnx for x<>1
# b. with x = pi/e-1, e^x > 1+x;            ~ https://math.stackexchange.com/questions/504663/simplest-or-nicest-proof-that-1x-le-ex
#                                           ~ e^x convex, y=1+x tangent to e^x at x = 0
#                                           ~ 1+x <= 1+x+x^2/2!+... = e^x, Taylor Series
#            e^(pi/e - 1) > pi/e,           
#            e^(pi/e) / e > pi / e,         ~ e^-1 = 1/e 
#                e^(pi/e) > pi,             ~ remove e
#                    e^pi > pi^e            ~ exponential of e on both sides

#%% Sliding window minimum

arr = [-3,-3,-3]; k = 1
mins = []
if len(arr)==k==1: mins=arr
for i in range(len(arr)-k+1):
    k_window = arr[i:i+k]
    print(i, i+k)
    if len(k_window) == k:
        print(arr[i:i+k],i, len(arr), min(k_window))
        mins.append(min(arr[i:i+k]))
        
#%% pivot in pandas
import pandas as pd
rows = [{"ticker": "AAPL", "amount": 10, "region":"US"}, 
        {"ticker": "MSFT", "amount": 4, "region":"US"}, 
        {"ticker": "AAPL", "amount": 6, "region":"US"}]

df = pd.DataFrame(rows)
df.groupby('ticker').sum()
c = df.groupby('ticker').agg(
    total = ('amount', 'sum'),
    averg = ('amount', 'mean'),
    count = ('amount', 'count')
    )

'''pivot = pd.pivot_table(df, 
                       values = 'amount',
                       fill_value=0,
                       index = 'region',
                       columns = 'ticker',
                       aggfunc= 'sum')

rolling = df['amount'].rolling(3).mean()

resample = df['amount'].resample('ME').last()'''
#%%
'''Provide both recursive and iterative implementations, and explain the key idea.
'''
import numpy as np
import math

# 3^4
# lne^6 = 6 lne
# ln3^4 = e^(4 ln3)

base = 3
exponent = 4
math.e**(np.log(base)*exponent) #invalid for negative base



#%%Levenshtein Distance, recursive search, dynamic programming
'''
    MIN(Del., Ins., Sub.)
    
    EXAMPLE s1='ab' s2='ac'
       Taking substitute-step at f(2,2) as an example, 
    because s1[i]='b' and s2[j]='a', 
    one of three approaches for addressing 'b' and 'c' is 
    to substitute at this step and forward, the cost will be 1+f(1,1), 
    where f(1,1) will include the cost after comparing again del., ins., or substitution. 
    It means addressing 'b' and 'a' is the start point of fixing two strings, 
    rather than one-state of only fixing 'b' and 'a', 
    because f(1,1) includes fixing i-1, j-1 elements until reaches 0.
    
        In terms of Delete branch, for s1[2] and s2[2] are 'b' and 'c' that are different, 
    1+f(1,2) has the cost of deleting s1[2] is 1 
    and after deleting s1[2], s1 becomes 'a' so it compares s1[1] with s2[2] 'c' 
    because the deletion is only applied to s1 string and s2 is not impacted; 
    my initial understanding was s2-index will change as well, so that's a misunderstanding. 
    At the one-step forward stage, comparing s1[1] and s2[2], 
    it will go through del., ins. and sub. to check the costless way to address 'a' and 'ac';
    after the three branches there, it locates the cost at the one-step-forward stage, 
    and brings it up as cost of f(1,2), then add the 1 to locate cost of f(2,2) 
    by using del. for addressing s1[2] <> s2[2].
    
        To reiterate, in Insertion situation, 
    1+f(2,1) suggests the underlying s1 is 'abc' and s2 'ac' 
    while in the coding implementation, this information isnt tracked 
    and instead marked as cost of an insertion process to be aggregated at f(2,1); 
    it means after implicitly "tracking" 'abc' and 'ac', 
    f(2,1) looks to find min cost of addressing 'ab' and 'a' since element-c is handled. 
    For 'ab' and 'a', it locates the costless operation after comparing del., ins. and sub., 
    and bring the cost of f(2,1) to 1+f(2,1) for aggregated cost of handling the two strings 
    by entering insertion to handle s1[2]<>s2[2] as the initial step.
    '''

def f(i, j):
    # Base cases
    if i == 0: return j  # insert j characters
    if j == 0: return i  # delete i characters

    # If they match, no cost, just move on
    if s1[i-1] == s2[j-1]:
        return f(i-1, j-1)
    
    # IF THEY DON'T MATCH: Try ALL THREE operations!
    # 1. Delete s1[i-1] -> cost 1, then fix s1[:i-1] vs s2[:j]
    delete = 1 + f(i-1, j)
    # 2. Insert s2[j-1] into s1 -> cost 1, then fix s1[:i] vs s2[:j-1]
    insert = 1 + f(i, j-1)
    # 3. Substitute s1[i-1] to match s2[j-1] -> cost 1, then fix s1[:i-1] vs s2[:j-1]
    substitute = 1 + f(i-1, j-1)
    
    return min(delete, insert, substitute)


#%% meeting room bookings

# [start, end)
intervals = [[0, 30], [5, 10], [15, 20]] 
                       
def min_rooms(intervals):
    '''
    Find the minimum number of rooms required so that every interval is assigned to a room with no overlaps. 
    Additionally, output an explicit assignment of each interval to a room, 
    and prove that your assignment is optimal.
    '''
    # 0 ---------- 30
    #   5-10 15-20
    
    # 1-5
    #  2-6
    #   3-7
    #    4-8
    
    rooms = [1]*len(intervals)
    a_int = [1]*len(intervals)
    #to check if following interval is part of current interval 
    
    for each in range(len(intervals)-1):
        current_start,current_end = intervals[each]
        next_start, next_end = intervals[each+1]
        if next_start >= current_end: #skipped checking for intervals that share a room ^^^###^^^
            rooms[each] = 0
    
    a = 0
    for room in rooms:
        a+=room
    return a
    #return sum(intervals)

min_rooms(intervals)        
#%% kth hamming number 

k = 7
h = [1]*k
i2 = i3 = i5 = 0
n2, n3, n5 = 2, 3, 5

for i in range(1,k):
    h[i] = min(n2, n3, n5)
    print(h, n2)
    if h[i] == n2:
        i2 += 1 
        n2 = h[i2]*2 #update next2/3/5 for the next round min comparing 
    if h[i] == n3:
        i3 += 1
        n3 = h[i3]*3 #h[i3] 
    if h[i] == n5:
        i5 += 1
        n5 = h[i5]*5 #h[i5]
print(h[-1])
#%% Levenstein distance
s1 = 'kitten'
s2 = 'sitting'

m,n = len(s1), len(s2)
dp = [[0]* (n+1) for _ in range (m+1)]

for i in range(m+1):
    dp[i][0] = i

for j in range(n+1):
    dp[0][j] = j
    
for i in range(1, m+1):
    for j in range(1, n+1):
        if s1[i-1] == s2[j-1]:
            dp[i][j] = dp[i-1][j-1]
        else:
            #min(deletion, insertion, substitution) an autonomy for these three
            #how does min correspond to the correct operation?
            dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) 
#%%            
''' Dynamic Programming
14 July
1. A deck has 50 red cards and 50 black cards. 
   Card is drawn one at a time without replacement,
   one may stop after any draw, and payoff is 2*#red/#drawn. 
   If never stops, all 100 cards are drawn.
   What is E[Payoff in $] if play optimally.
   
'''
#V(r,b) = max(2r/(r+b), (50-r)/(100-r-b)V(r+1,b)+(50-b)/(100-r-b)V(r,b+1))





'''
2. Best candidate selection
   Given the best candidate is at k, the best will be selected 
   if secondary-best candidate prior to k is within the rejection window
   reindex summation bounds to align with Harmonic Series

'''


