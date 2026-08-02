# Distributions
Core distributions, inter-relationships, considerations and implications

### Normal/Gaussian Distribution

### Log-Normal Distribution

### Chi-Squared Distribution

### Geometric Distribution
a. total trials of reaching a success, including the success 
<br />$E[Geom] = \frac{1}{p}$

b. total trials of failure before reaching a success 
<br />$E[Geom_f] = \frac{1}{p} - 1 = \frac{1-p}{p}$

### Negative Binomial Distribution

### Exponential Distribution

### Poisson Distribution
- memoryless property of arrivals
   - uniformly random arrival with length-biased sampling, meaning a.the random arrival is b.not expected to occur at mid-point of a waiting interval
   - per each fresh start, E[waiting time] = $\frac{1}{\lambda}$ following Poisson Process with arrival rate $\lambda$ = $\frac{1}{2} * \frac{2}{\lambda}$
   - uniformly random arrival at on Unif~[0,L] produces E[remaining waiting time] = E[ $\frac{L}{2}$ ]
   - length-based sampling indicates E[length of whole arrival interval one landed in] = E[L] = $\frac{2}{\lambda}$ ~ Gamma(2,$\lambda$) for density of interval arrival, $x \lambda e^{-\lambda x}$
