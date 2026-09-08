### Statistical analysis
- Jensen's inequality: convex f and random variable X: $E[f(x)] \geq f(E[X])$; concave f has the opposite relation

- expectations, $\mu=E[X]$

- variance
  - $Var(X) = E[(X - \mu)^2] = E[X^2] - 2E[X E[X]] + E[E[X]^2]= E[X^2] - 2E[X]^2 + E[X]^2 = E[X^2] - E[X]^2 $
  - $Var(X+Y)$
    - $X,Y$ dependent: $Var(X+Y) = Var(X) + Var(Y) + 2Cov(X,Y)$ 
    - $X,Y$ independent: $Var(X+Y) = Var(X)+Var(Y)$ ~ $Cov(X,Y) = 0$
  - $E[X^2] - E[X]^2 \geq 0$
    - a. $f(x) = x^2$ with Jensen's inequality
    - b. $X$ to be constant
      
- covariance, correlation
  - $Cov(X,Y) = E[XY]-E[X]E[Y]$ 
  - $Cov(X,Y) = E[(X-E[X])(Y-E[Y])]$
    - $X,Y$ dependent: $Cov(X,Y) = 2*corr(X,Y) * \sigma_X \sigma_Y$ 
    - $X,Y$ independent: $Cov(X,Y) = 0$
  - $Cov(X,X) = Var(X)$
  - correlated: linear pattern between two variables
  - 0 covariance does not imply independence
- Gaussian Moment Generating Function

### Statistical significance, power, effect size and hypothesis test
- $H_0$ and $H_1$ to be true or false are mutually exclusive while the test can only reject or fail reject $H_0$, then in support of $H_1$
  - s. significance by design: reject $H_0$ given $H_0$ is true
  - s. power, to be observed: reject $H_0$ given $H_1$ is true
  - Type I error: reject $H_0$ given $H_0$ is true
  - Type II error: fail to reject $H_0$ given $H_1$ is true
- test score and p-value 

### OLS assumptions, multicollinearity, error measurement and duplicative observations
- BLUE
- Multicollinearity
  - potentially high standard errors of individual coefficient 
- Measurement error
  - TRUE model: $y = \beta X_{true}^* + \epsilon$ and OBSERVE $X = X_{true}^* + \mu$
     - regressor, contaminated X variable: $X = X_{true}^* + \mu$ where $\mu$ the measurement error is independent of $X, X_{true}^*$
     - having true model $y = \beta X^* + \epsilon$ and observe $X = X^* + \mu$, substituting $X^* = X-\mu$ into true model $y$, it has $y=\beta (X-\mu) + \epsilon = \beta X + \epsilon - \beta\mu$
     - "If that composite error were just a constant or uncorrelated noise, OLS on $y$ against $X$ would work" meaning
        - a. $-\beta \mu + \epsilon$ and $X$ has $cov(X,\mu_{composite})=Var(\mu_{composite}) \neq 0$, then $X$ and $\mu$ are correlated, which violates OLS assumption of uncorrelated regressor and error term
        - b.OLS on y against with no need of reliability ratio?

### Effect of modified variables, on $\beta$ and $R^2$
- Existing regressors
  - scaling or shifting $X$ variable
- Additional regressors
  - perfect-collinear $X$ variable, linear combination
      - redundant information, $x_3 = x_1 + 2, x_3 = x_1 * 3$
      - $x_3$ appears in column space of $x_1, x_2$
  - partial-collinearity, multiplicative variable
      - newly interactive term, $x_3 = x_1 * x_2$, expands column space of $x_1, x_2$
   
### Maximum and minimum of one and multiple distributions
- $E[max(X,Y)]=\int_0^1(2t*tdt)$ where t is the comparative threshold
  - CDF $P(X \leq t)=t=P(Y \leq t)$, $max(X,Y)=P(X \leq t)P(Y \leq t)=t^2$ ~ Unif[0,1]
  - PDF of $max(X,Y)=2t$
  - survival function, $E[P(X \leq t)P(Y \leq t)]=\int_0^{\inf} 1-t^2 dt$
- $E[min(X,Y)]=E[P(X\geq t)P(Y\geq t)]$
  - $P(X \geq t) = 1-P(X \leq t) = 1- \frac{x-a}{b+a} = \frac{b-x}{b+a}$
  - survival function, $E[P(X \geq t)P(Y \geq t)] = \int_0^{\inf} \frac{b_x-t}{b_x+a_x} \frac{b_y-t}{b_y+a_y} dt$





