# Modeling and Simulation

## Distributions

### 1. Normal
**Data:** final_score (mean and standard deviation)  
**Purpose:** Models bell-shaped data with most values clustering around a mean. Represents typical academic performance where most students score near average.

### 2. Uniform
**Data:** attendance_rate (min and max)  
**Purpose:** Models data evenly distributed across a range with no concentration points. Shows completely random attendance patterns between minimum and maximum values.

### 3. Exponential
**Data:** study_hours_per_week (mean)  
**Purpose:** Models decay or "time until event" patterns. Shows realistic study behavior where most students study very few hours, with few studying many hours.

### 4. Poisson
**Data:** age (mean)  
**Purpose:** Models count data for discrete events over time/space. Represents how student ages cluster around a typical school age with fewer outliers.

### 5. Binomial
**Data:** passed (success probability)  
**Purpose:** Models outcomes of repeated trials with two possible results (success/failure). Shows how many students are likely to pass across multiple trials.

### 6. Gamma
**Data:** study_hours_per_week (shape and scale)  
**Purpose:** Models durations and waiting times with shape control. Shows realistic study patterns with most shorter commitments but some longer ones.

### 7. Beta
**Data:** attendance_rate (mean and standard deviation)  
**Purpose:** Models proportions bounded between 0 and 1 (like percentages). Shows whether attendance is concentrated near low, high, or middle values.

### 8. Weibull
**Data:** study_hours_per_week (shape parameter)  
**Purpose:** Models reliability and failure rates with flexible shape. Useful for analyzing how likely students are to maintain study habits over time.

### 9. Lognormal
**Data:** final_score (log-transformed)  
**Purpose:** Models right-skewed positive values. Shows realistic score distribution where most cluster lower with fewer very high scores.

### 10. Triangular
**Data:** attendance_rate (min, mode, max)  
**Purpose:** Models realistic scenarios where you know the minimum, most likely, and maximum values. Shows attendance patterns with a defined peak likelihood.