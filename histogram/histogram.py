import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("data/student_performance.csv")
print(data.dtypes)

scores = data['final_score']
attendance_rate = data['attendance_rate']
passed = data['passed']
age = data['age']
weekly_hours = data['study_hours_per_week']

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
        'Binomial', 
        'Gamma', 
        'Beta', 
        'Weibull', 
        'Lognormal'
        ]

def histogram():
    while True:
        user = input(f"\nSelect a distribution to visualize ({', '.join(dist)}) or 'exit' to quit: ")
        if user.lower() == 'normal':
            plt.hist(scores, bins=20, density=True, alpha=0.6, color='g')
            plt.text(0.02, 0.95, f'Data: final_score\nMean: {mean:.2f}\nStd Dev: {standard_deviation:.2f}', 
                     transform=plt.gca().transAxes, verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=9)
        elif user.lower() == 'uniform':
            min_previous_score = np.min(data['previous_score'])
            max_previous_score = np.max(data['previous_score'])
            plt.hist(data['previous_score'], bins=20, density=True, alpha=0.6, color='b')
            plt.text(0.02, 0.95, f'Data: previous_score\nMin: {min_previous_score:.2f}\nMax: {max_previous_score:.2f}', 
                     transform=plt.gca().transAxes, verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=9)
        elif user.lower() == 'binomial':
            p_passed = np.mean(passed == 'Yes')
            passed_binary = (passed == 'Yes').astype(int)
            plt.hist(passed_binary, bins=20, density=True, alpha=0.6, color='m')
            plt.text(0.02, 0.95, f'Data: passed\nP(success): {p_passed:.2f}', 
                     transform=plt.gca().transAxes, verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=9)
        elif user.lower() == 'gamma':
            gamma_mean = np.mean(scores)
            gamma_std_dev = np.std(scores)
            plt.hist(scores, bins=20, density=True, alpha=0.6, color='y')
            plt.text(0.02, 0.95, f'Data: final_score\nMean: {gamma_mean:.2f}\nStd Dev: {gamma_std_dev:.2f}', 
                     transform=plt.gca().transAxes, verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=9)
        elif user.lower() == 'beta':
            attendance_mean = np.mean(attendance_rate)
            attendance_std_dev = np.std(attendance_rate)
            plt.hist(attendance_rate, bins=20, density=True, alpha=0.6, color='k')
            plt.text(0.02, 0.95, f'Data: attendance_rate\nMean: {attendance_mean:.2f}\nStd Dev: {attendance_std_dev:.2f}', 
                     transform=plt.gca().transAxes, verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=9)
        elif user.lower() == 'weibull':
            weibull_mean = np.mean(scores)
            weibull_std_dev = np.std(scores)
            plt.hist(scores, bins=20, density=True, alpha=0.6, color='orange')
            plt.text(0.02, 0.95, f'Data: final_score\nMean: {weibull_mean:.2f}\nStd Dev: {weibull_std_dev:.2f}', 
                     transform=plt.gca().transAxes, verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=9)
        elif user.lower() == 'lognormal':
            log_scores = np.log(scores)
            log_mean = np.mean(log_scores)
            log_std_dev = np.std(log_scores)
            plt.hist(log_scores, bins=20, density=True, alpha=0.6, color='purple')
            plt.text(0.02, 0.95, f'Data: final_score (log-transformed)\nLog Mean: {log_mean:.2f}\nLog Std Dev: {log_std_dev:.2f}', 
                     transform=plt.gca().transAxes, verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=9)
        elif user.lower() == 'exit':
            print("Exiting the program.")
            break
        else:
            print("Invalid distribution. Please try again.")
            continue

        # Set distribution-specific labels
        labels = {
            'normal': ('Final Score', 'Final Score'),
            'uniform': ('Previous Score', 'Previous Score'),
            'binomial': ('Pass Count (out of 100 trials)', 'Pass Count'),
            'gamma': ('Final Score', 'Final Score'),
            'beta': ('Attendance Rate (proportion)', 'Attendance Rate'),
            'weibull': ('Final Score', 'Final Score'),
            'lognormal': ('Final Score', 'Final Score')
        }
        
        xlabel, data_label = labels.get(user.lower(), ('Value', 'Value'))
        plt.title(f"{user} Distribution of {data_label}")
        plt.xlabel(xlabel)
        plt.ylabel("Density")
        plt.grid()
        plt.show()

if __name__ == "__main__":
    histogram()