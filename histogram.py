import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("data/student_performance.csv")
print(data.dtypes)

scores = data['final_score']
mean = np.mean(scores)
standard_deviation = np.std(scores)
min = np.min(scores)
max = np.max(scores)
print(f"\nScore Mean: {mean}")
print(f"Score Standard Deviation: {standard_deviation}")
print(f"Score Min: {min}")
print(f"Score Max: {max}")

dist = ['Normal', 
        'Uniform', 
        'Exponential', 
        'Poisson', 
        'Binomial', 
        'Gamma', 
        'Beta', 
        'Weibull', 
        'Lognormal'
        ]

def histogram():
    while True:
        user = input(f"\nSelect a distribution to visualize ({', '.join(dist)}): ")
        if user.lower() == 'Normal':
            plt.hist(scores, bins=20, density=True, alpha=0.6, color='g')
        elif user.lower() == 'Uniform':
            plt.hist(scores, bins=20, density=True, alpha=0.6, color='b')
        elif user.lower() == 'Exponential':
            plt.hist(scores, bins=20, density=True, alpha=0.6, color='r')
        elif user.lower() == 'Poisson':
            plt.hist(scores, bins=20, density=True, alpha=0.6, color='c')
        elif user.lower() == 'Binomial':
            plt.hist(scores, bins=20, density=True, alpha=0.6, color='m')
        elif user.lower() == 'Gamma':
            plt.hist(scores, bins=20, density=True, alpha=0.6, color='y')
        elif user.lower() == 'Beta':
            plt.hist(scores, bins=20, density=True, alpha=0.6, color='k')
        elif user.lower() == 'Weibull':
            plt.hist(scores, bins=20, density=True, alpha=0.6, color='orange')
        elif user.lower() == 'Lognormal':
            plt.hist(scores, bins=20, density=True, alpha=0.6, color='purple')
        else:
            print("Invalid distribution. Please try again.")
            continue

        plt.title(f"{user} Distribution of Final Scores")
        plt.xlabel("Final Score")
        plt.ylabel("Density")
        plt.grid()
        plt.show()
        break

if __name__ == "__main__":
    histogram()