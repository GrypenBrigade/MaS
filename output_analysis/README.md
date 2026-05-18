# Output analysis

### Brief Explanations of Output Analysis Methods

**Replication/Deletion**
Runs multiple independent replications (simulations) and deletes initial transient data (warmup period) from each. Computes confidence intervals from the replica means, reducing bias from startup effects.

**Batch Mean**
Runs a single long simulation, discards the warmup period, then divides remaining data into batches. Treats batch means as independent observations to estimate confidence intervals; useful for detecting correlation between batches.

**Welch Method**
Uses spectral analysis to estimate the asymptotic variance of the sample mean. Determines an appropriate warmup period and computes confidence intervals without requiring independent replications or batches.

## Results from outanalysis.py

M/M/1 Queue  |  λ=0.8, μ=1.0, ρ=0.8
Theoretical steady-state mean wait: 4.0000 min

**METHOD 1 — REPLICATION / DELETION**
  Replications    : 20
  Customers/rep   : 5000  |  Warmup: 500
  Grand mean      : 3.9300
  95% CI          : (3.6631, 4.1970)
  Theoretical     : 4.0000

**METHOD 2 — BATCH MEANS**
  Total customers : 50000  |  Warmup: 500
  Batches         : 30  |  Batch size: 1650
  Grand mean      : 3.9870
  95% CI          : (3.6622, 4.3117)
  Lag-1 autocorr  : -0.3314  (want ≈ 0)
  Theoretical     : 4.0000

**METHOD 3 — WELCH METHOD**
  Replications    : 20
  Moving avg win  : ±30
  Suggested warmup: 2500 customers
  Long-run avg    : 3.7684
  Theoretical     : 4.0000