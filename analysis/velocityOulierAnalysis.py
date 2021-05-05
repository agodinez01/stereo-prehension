import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

#Takes velocityData4Distribution.csv and makes reach velocity figures.

myPath = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/Data/'
fig_dir = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/figs/velocity_traces_truncated/'

os.chdir(myPath)

data = pd.read_csv('velocityData4Distribution.csv')

subjects = data.subject.unique()
conditions = data.condition.unique()
trials = data.trial.unique()

##### VISUALIZATION #####

# Method 1. Box plot
sns.boxplot(x=data['velocity'])
plt.show()
plt.clf()

##### From the box plot, anything > 0.04 and < 0.04 are outliers. #####

# # Method 2. Scatter plot
#
# fig, ax = plt.subplots(figsize=(16,8))
# ax.scatter(data['time'], data['velocity'])
# ax.set_xlabel('Time')
# ax.set_ylabel('Velocity')
# plt.show()

# Method 3. Z-score

z = np.abs(stats.zscore(data['velocity']))
#print(z)

threshold = 3

print(np.where(z > 3))

# I don't like this method because I need the negative values. Besides, I just need to replace outliers with 'nan'

# IQR score

Q1 = data['velocity'].quantile(0.25)
Q3 = data['velocity'].quantile(0.75)

IQR = Q3 - Q1

print('Q3 = ' + str(Q3))
print('Q1 = ' + str(Q1))

# Calculate the lower and the upper whisker
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

print('lower = ' + str(lower))
print('upper = ' + str(upper))

abs_vel = np.absolute(data.velocity)

abs_Q1 = abs_vel.quantile(0.25)
abs_Q3 = abs_vel.quantile(0.75)

abs_IQR = abs_Q3 - abs_Q1

print('abs_Q3 = ' + str(abs_Q3))
print('abs_Q1 = ' + str(abs_Q1))

abs_lower = abs_Q1 - 1.5 * abs_IQR
abs_upper = abs_Q3 + 1.5 * abs_IQR

print('abs lower = ' + str(abs_lower))
print('abs upper = ' + str(abs_upper))

data