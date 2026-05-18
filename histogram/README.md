# Modeling and Simulation

## Distributions

### 1. Normal
**Data:** final_score (mean and standard deviation)  
**Purpose:** Models bell-shaped data with most values clustering around a mean. Represents typical academic performance where most students score near average.

### 2. Uniform
**Data:** previous_score (min and max)  
**Purpose:** Models data evenly distributed across a range with no concentration points. Shows uniform distribution of previous scores across the full range.

### 3. Binomial
**Data:** passed (success probability)  
**Purpose:** Models outcomes of repeated trials with two possible results (success/failure). Shows how many students are likely to pass across multiple trials.

### 4. Gamma
**Data:** final_score (shape and scale)  
**Purpose:** Models durations and waiting times with shape control. Provides insight into score distribution patterns with flexible shape parameters.

### 5. Beta
**Data:** attendance_rate (mean and standard deviation)  
**Purpose:** Models proportions bounded between 0 and 1 (like percentages). Shows whether attendance is concentrated near low, high, or middle values.

### 6. Weibull
**Data:** final_score (shape parameter)  
**Purpose:** Models reliability and failure rates with flexible shape. Useful for analyzing score distribution patterns with flexible shape control.

### 7. Lognormal
**Data:** final_score (log-transformed)  
**Purpose:** Models right-skewed positive values. Shows realistic score distribution where most cluster lower with fewer very high scores.

## Distributions Not Included

The three distributions **Exponential**, **Triangular**, and **Poisson** were excluded from the analysis due to poor fit with the student performance dataset:

- **Exponential:** This distribution models rapid decay from zero and is designed for "time until event" phenomena. Student performance data (scores, rates, and counts) does not exhibit this decay pattern.
  
- **Triangular:** This distribution requires a single-peaked triangle shape with defined minimum, mode, and maximum values. The bounded nature of student performance variables does not form a sharp triangular peak.
  
- **Poisson:** This distribution models count data for discrete, unbounded events over time or space (e.g., number of occurrences). While age and certain performance counts are discrete, they don't follow the characteristic patterns that make Poisson appropriate. Additionally, the dataset's variables are typically bounded or limited in range, violating Poisson's assumption of unbounded event counts.