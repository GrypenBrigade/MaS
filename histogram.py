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
        'Exponential', 
        'Poisson', 
        'Triangular',
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
            normal_scores = np.random.normal(mean, standard_deviation, size=len(scores))
            plt.hist(normal_scores, bins=20, density=True, alpha=0.6, color='g')
            plt.text(0.02, 0.95, f'Data: final_score\nMean: {mean:.2f}\nStd Dev: {standard_deviation:.2f}', 
                     transform=plt.gca().transAxes, verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=9)
        elif user.lower() == 'uniform':
            min_attendance_rate = np.min(attendance_rate)
            max_attendance_rate = np.max(attendance_rate)
            uniform_scores = np.random.uniform(min_attendance_rate, max_attendance_rate, size=len(scores))
            plt.hist(uniform_scores, bins=20, density=True, alpha=0.6, color='b')
            plt.text(0.02, 0.95, f'Data: attendance_rate\nMin: {min_attendance_rate:.2f}\nMax: {max_attendance_rate:.2f}', 
                     transform=plt.gca().transAxes, verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=9)
        elif user.lower() == 'exponential':
            exp_mean = weekly_hours.mean()
            exponential_scores = np.random.exponential(exp_mean, size=len(scores))
            plt.hist(exponential_scores, bins=20, density=True, alpha=0.6, color='r')
            plt.text(0.02, 0.95, f'Data: study_hours_per_week\nMean: {exp_mean:.2f}', 
                     transform=plt.gca().transAxes, verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=9)
        elif user.lower() == 'poisson':
            mean_age = np.mean(age)
            poisson_scores = np.random.poisson(mean_age, size=len(scores))
            plt.hist(poisson_scores, bins=20, density=True, alpha=0.6, color='c')
            plt.text(0.02, 0.95, f'Data: age\nMean: {mean_age:.2f}', 
                     transform=plt.gca().transAxes, verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=9)
        elif user.lower() == 'binomial':
            p_passed = np.mean(passed == 'Yes')
            binomial_scores = np.random.binomial(n=100, p=p_passed, size=len(scores))
            plt.hist(binomial_scores, bins=20, density=True, alpha=0.6, color='m')
            plt.text(0.02, 0.95, f'Data: passed\nP(success): {p_passed:.2f}\nn: 100', 
                     transform=plt.gca().transAxes, verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=9)
        elif user.lower() == 'gamma':
            gamma_scale = weekly_hours.mean()
            gamma_scores = np.random.gamma(shape=2, scale=gamma_scale, size=len(scores))
            plt.hist(gamma_scores, bins=20, density=True, alpha=0.6, color='y')
            plt.text(0.02, 0.95, f'Data: study_hours_per_week\nShape: 2\nScale: {gamma_scale:.2f}', 
                     transform=plt.gca().transAxes, verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=9)
        elif user.lower() == 'beta':
            attendance_mean = np.mean(attendance_rate)
            attendance_std_dev = np.std(attendance_rate)
            beta_scores = np.random.beta(a=attendance_mean, b=attendance_std_dev, size=len(scores))
            plt.hist(beta_scores, bins=20, density=True, alpha=0.6, color='k')
            plt.text(0.02, 0.95, f'Data: attendance_rate\na (mean): {attendance_mean:.2f}\nb (std_dev): {attendance_std_dev:.2f}', 
                     transform=plt.gca().transAxes, verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=9)
        elif user.lower() == 'weibull':
            weibull_shape = weekly_hours.mean()
            weibull_scores = np.random.weibull(a=weibull_shape, size=len(scores))
            plt.hist(weibull_scores, bins=20, density=True, alpha=0.6, color='orange')
            plt.text(0.02, 0.95, f'Data: study_hours_per_week\nShape (a): {weibull_shape:.2f}', 
                     transform=plt.gca().transAxes, verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=9)
        elif user.lower() == 'lognormal':
            log_scores = np.log(scores)
            log_mean = np.mean(log_scores)
            log_std_dev = np.std(log_scores)
            lognormal_scores = np.random.lognormal(log_mean, log_std_dev, size=len(scores))
            plt.hist(lognormal_scores, bins=20, density=True, alpha=0.6, color='purple')
            plt.text(0.02, 0.95, f'Data: final_score (log-transformed)\nLog Mean: {log_mean:.2f}\nLog Std Dev: {log_std_dev:.2f}', 
                     transform=plt.gca().transAxes, verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=9)
        elif user.lower() == 'triangular':
            min_attendance_rate = np.min(attendance_rate)
            mode_attendance_rate = np.mean(attendance_rate)
            max_attendance_rate = np.max(attendance_rate)
            triangular_scores = np.random.triangular(left=min_attendance_rate, mode=mode_attendance_rate, right=max_attendance_rate, size=len(scores))
            plt.hist(triangular_scores, bins=20, density=True, alpha=0.6, color='brown')
            plt.text(0.02, 0.95, f'Data: attendance_rate\nMin: {min_attendance_rate:.2f}\nMode: {mode_attendance_rate:.2f}\nMax: {max_attendance_rate:.2f}', 
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
            'uniform': ('Attendance Rate (%)', 'Attendance Rate (%)'),
            'exponential': ('Study Hours Per Week', 'Study Hours Per Week'),
            'poisson': ('Age (years)', 'Age'),
            'binomial': ('Pass Count (out of 100 trials)', 'Pass Count'),
            'gamma': ('Study Hours Per Week', 'Study Hours Per Week'),
            'beta': ('Attendance Rate (proportion)', 'Attendance Rate'),
            'weibull': ('Study Hours Per Week', 'Study Hours Per Week'),
            'lognormal': ('Final Score', 'Final Score'),
            'triangular': ('Attendance Rate (%)', 'Attendance Rate (%)')
        }
        
        xlabel, data_label = labels.get(user.lower(), ('Value', 'Value'))
        plt.title(f"{user} Distribution of {data_label}")
        plt.xlabel(xlabel)
        plt.ylabel("Density")
        plt.grid()
        plt.show()

if __name__ == "__main__":
    histogram()