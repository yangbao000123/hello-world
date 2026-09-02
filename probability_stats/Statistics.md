### Statistical analysis
-  Jensen's inequality: convex f and random variable X: $E[f(x)] \geq f(E[X])$; concave f has the opposite relation

- expectations, $\mu=E[X]$

- variance
  - $Var(X) = E[(X - \mu)^2]$
    -    $= E[X^2] - 2E[X E[X]] + E[E[X]^2]= E[X^2] - 2E[X]^2 + E[X]^2 = E[X^2] - E[X]^2 $
  - $Var(X+Y)$
    - X,Y dependent: $Var(X+Y) = Var(X) + Var(Y) + 2Cov(X,Y)$ 
    - X,Y independent: $Var(X+Y) = Var(X)+Var(Y)$ ~ $Cov(X,Y) = 0$
  - $E[X^2] - E[X]^2 \geq 0$
    - a. $f(x) = x^2$ with Jensen's inequality
    - b. X to be constant
      
- covariance, correlation
  - $Cov(X,Y) = E[(X-E[X])(Y-E[Y])]$
    - X,Y dependent: $Cov(X,Y) = 2*corr(X,Y) * \sigma_X \sigma_Y $ 
    - X,Y independent: $Cov(X,Y) = 0$
  - $Cov(X,X) = Var(X)$

  - correlated: linear pattern between two variables

- Gaussian Moment Generating Function

### Statistical significance, power, effect size and hypothesis test
- $H_0$ and $H_1$ to be true or false are mutually exclusive while the test can only reject or fail reject $H_0$, then in support of $H_1$
  - s. significance by design: reject $H_0$ given $H_0$ is true
  - s. power, to be observed: reject $H_0$ given $H_1$ is true
  - Type I error: reject $H_0$ given $H_0$ is true
  - Type II error: fail to reject $H_0$ given $H_1$ is true

### OLS assumptions, multicollinearity, error measurement and duplicative observations

- BLUE
- Multicollinearity
- Measurement error
  - TRUE model: $y = \beta X_{true}^* + \epsilon$ and OBSERVE $X = X_{true}^* + \mu$
     - regressor, contaminated X variable: $X = X_{true}^* + \mu$ where $\mu$ the measurement error is independent of $X, X_{true}^*$
     - having true model $y = \beta X^* + \epsilon$ and observe $X = X^* + \mu$, substituting $X^* = X-\mu$ into true model $y$, it has $y=\beta (X-\mu) + \epsilon = \beta X + \epsilon - \beta\mu$
     - "If that composite error were just a constant or uncorrelated noise, OLS on $y$ against $X$ would work" meaning
        - a. $-\beta \mu + \epsilon$ and $X$ has $cov(X,\mu_{composite})=Var(\mu_{composite}) \neq 0$, then $X$ and $\mu$ are correlated, which violates OLS assumption of uncorrelated regressor and error term
        - b.OLS on y against with no need of reliability ratio? 





