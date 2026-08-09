## Exercise

### Uniformly random i.i.d. particles, linearity of expectation
-  uniformally random -> independent events -> indicator variables -> linearity of expectation
    - subset and sum values of elements
        - independet inclusion/exclusion of $x_i$ contribution to subset sum value
        - time for all options to be exercised (application)
- bouncing leads to indistinguishable passing-through
    - 2 ants on a stick; 100 bugs on a stick: 
        - $\max(x_1, x_2, ..., x_n); $
        - $E[M] = \int_{0}^{1} t*p(t)dt$ 
        - where p(t) defines probability density function
          
### Choices available
- expecation worked out in backwards for discerning forfeit cutoff with 3-roll opportunity
    - forfeir if $E[V_{Current}] < E[V_{Next}]$
    - to roll three rounds, $E[V_{Current}] \geq E[V_{Next}]$
    - apply flooring, $E_{Next}$, to face values at each roll
        - $E_{Third} = E_{Last} = 3.5$
        - $E_{Second}$ to capture expected payout given 2nd round succeeds #E_{Third}$ and same applies to $E_{First}$
- non-divider occasions between dividier, divider and occasion prior to first divider
    - strict divider given 2 is before A, soft divider: E[cards after first 2 and before first A]
- passengers with one lost ticket to seat uniformly random
    - first passenger seating situation + all rest passengers
    - seating decision prior to passenger k only delays a mis-seating decision and not suspends the process
    - passenger k's options 
- best candidate selection
    - given the best candidate is at k, the best will be selected if secondary-best candidate prior to k is within the rejection window
    - reindex summation bounds to align with Harmonic Series
- seating with no adjacent neighbors, shrinking size of audience dependent on seating options
    - first audience seating situation + all rest audience
    - $1 + \sum_{i=1}^{n} max(0,left seatings) + max(0,rightseatings) = 1 + \frac{2}{n}$ * $\sum_{i}^{n-2} f(i)$
- surviving sharks, finite number of sharks 
    - a shark and out-pace its two neighbors
  
### Recursion, recurrence at uniformly random probabilities; OST
- absorbing state at 0 and N, $E_0 = E_N = 0$
    - Exit time of a random walk
    - $E_k = 1 + \frac{1}{2} E_{K-1} + \frac{1}{2} E_{k+1}$
- number of states, ending of game is dependent on one of states;
- E[event] is conditional on first or previous outcome
- cost of current step: 1
- additional step to reach a state given current state
    - E[filps until both head and tail]
    - E[rolling out same face value and end]
    - E[seated with no-adjacent rule]
    - E[steps to cover all edges of a triangle]
    - stop game when reach repetitive value {1, 2, 3, 1, 2, 3}
        - expected payout given last-roll result
        - earnings at each round
                
### Distinct-item set, indicator variable and symmetry
- indicator variable
    - expectation and probability
        - probability (2 dices roll number that are less than or equal to k) - probability ( 2 dices roll number that are less than or equal to k-1)
            - scenarios of first dice = k and second dice < k has 1*(k-1) ways, second scenario is a symmetry of the first scenario and also k-1 ways, and third scenario first=second=k, has 1*1=1 way to reach 
        - each of 5 boxes has 1 coupon drawn uniformly random without replacement. Number of boxes to acquire for collecting at least each of 5 coupons
        - 4 distinct cards in a set, 6 independent set; E[unique cards in total]
    - variance if independent, Var=$E[I^2]-E^2[I] = p-p^2 = p(1-p) = pq$
    - covariance of variables, $Cov(X_i, Y_i) = E[X_i, Y_i] - E[X_i]E[Y_i]$ 
            - rolling a dice 5 times, X and Y each be number of appearance for two number
    - cumulative probability
- Harmonic series
    - $\sum_{k=0}^{\inf}\frac{1}{k!} = e$ ~ Taylor Series
    - $\sum_{k=1}^{n}\frac{1}{k} = H_n = ln(n) + \gamma + O(\frac{1}{n})$
    - $H^(2)_n \to \frac{\pi^2}{6}$
      
### Optimal stopping; 
- number of states, reaching absorbing state is the end of game
- stop and collect $x_t$ or reach $x_n$ and forced to take $x_n$
    - stopping cutoff, $max (x_t, V_{t+1})$
    - $E[max(x_t, V_{t+1})] = \int_{0}^{V_{t+1}} V_{t+1} + \int_{V_{t+1}}^{1} x dx$      ~ Bellman Equation
- with two fair dices, when both dices don't roll out 1, accumulate face value to running total; if either dice rolls a 1, the game stops and lose the sum.
    - running sum to be E[Sum + expected-2-dice-sum] = P(2 dices not rolling 1) * E[Sum + 2* $\frac{2+3+4+5+6}{5}$ ] = E[Sum + 2*4] + P(2 dices rolling 1) * 0
- tail-result reflip with cost
- with Tail appears, keep current payout or forfeit it to play one more round 
    - N: total number of flips til the first tail, **inclusive** of the tail flip;
    - N~Geom($\frac{1}{2}$), $E[Heads] = \frac{1}{p} - 1$
    - situation to forfeit: first-round payout < $E[h_{payout} * (N-1)]$
        - where $E[h_{payout} * (N-1)]$ measures a fresh-round payout since hasn't flipped a tail
        - as first-round turns to be Head, it's equivalent to start the game fresh
      
### Tail-sum, volume of an n-dimensional simplex
- number of occassions to exceed 1 is equivalent to aggregated number of occasions when it hasn't reached 1
- because 1 hasn't been reached, the number of draws increases
    - let N = $\min {(n: U_1 + U_2 + ... + U_n > 1)}$
        - $U_i$ ~ Unif(0,1)
        - $\sum_{k=0}^{\inf} P(N\geq k) = \sum_{k=0}^{\inf} \frac{1}{n!} = e$ ~ Taylor's series expansion
        - P(N>0) = 1 ~ always needs the first draw
        - P(N>1) = 1 ~ in continuous distribution P(U=1)=0 for any pre-specified value draw, so needs a second draw

### Number anlaysis
- $e^\pi$ versus $\pi^e$, [source](https://math.stackexchange.com/questions/7892/comparing-pie-and-e-pi-without-calculating-themzz), [less equal](https://math.stackexchange.com/questions/504663/simplest-or-nicest-proof-that-1x-le-ex)
   - apply natual log to both sides and concavity of ln, $x-1 > ln x$ for x<>1
<br> with $x = \frac{\pi}{e}-1,$
```math
\begin{aligned}
  e^x > 1+x \\
  e^{\frac{\pi}{e}} - 1 > \frac{\pi}{e} \\
  \frac{e^{\frac{\pi}{e}}}{e} > \frac{\pi}{e} \\
  e^{\frac{\pi}{e}} > \pi \\              
  e^\pi > \pi^e \\
\end{aligned}
```
