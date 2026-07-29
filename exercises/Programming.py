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
        if next_start >= current_end: #skipped checking for intervals that share a room
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


