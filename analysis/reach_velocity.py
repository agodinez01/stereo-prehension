import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy import signal
import seaborn as sns

# Takes vel_data_with_Ter_analysis2.csv and makes reach velocity figures.
# 5/04/21 Added absolute and bi-directional velocity to one plot
# 5/05/21 Added grip aperture
# 5/08/21 Created two versions, (1) Creates the individual velocity/grasp figures
#   (0) Creates the absolute velocity dataframes without creating the figure. If you change the
#   dataframe, you should run the figures again
# Sometime in June, removed outliers by

myPath = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/Data/'

os.chdir(myPath)

data = pd.read_csv('vel_data_with_Ter_analysis2.csv')

subjects = data.subject.unique()
conditions = data.condition.unique()
trials = data.trial.unique()

# Method 1. Box plot
sns.boxplot(x=np.abs(data['ter_velocity']), boxprops=dict(alpha=0.5))
sns.boxplot(x=np.abs(data.ter_velocity[data.type == 'stereo-normal']), color='#99ffcc', boxprops=dict(alpha=0.5))
sns.boxplot(x=np.abs(data.ter_velocity[data.type == 'stereo-anomalous']), color='#ff9999', boxprops=dict(alpha=0.5))
#plt.show()
plt.clf()

# Calculate First and third Quartile
Q1 = np.abs(data['ter_velocity']).quantile(0.25)
Q3 = np.abs(data['ter_velocity']).quantile(0.75)

# Calculate interquartile range
IQR = Q3 - Q1

# Calculate the lower and upper whiskers
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

# Calculate inner and outer fences
inner_fence = Q1 - 3.0 * IQR
outer_fence = Q3 + 3.0 * IQR

# Low-pass Butterworth variables for function butter_lowpass_filter
T = 1
fs = 50.0
cutoff = 3
nyq = 0.5 * fs
order = 2
n = int(T * fs)

def butter_lowpass_filter(input_data, cuttoff, fs, order):
    normal_cutoff = cutoff / nyq

    # Get filter coefficients
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    y = signal.filtfilt(b, a, input_data)

    return y

# Define function to make velocity dataframe and save to csv
def makeVelocityFillDataframe(input_data):
    sub_vals = []
    group_vals = []
    cond_vals = []
    trial_vals = []
    time_vals = []
    vel_vals = []
    vel_filled_vals = []
    vel_bw_filter = []

    for sub in subjects:
        for cond in conditions:
            for t in trials:

                subData = input_data.loc[
                    (input_data.subject == sub) & (input_data.condition == cond) & (input_data.trial == t)]

                if len(subData) == 0:
                    continue

                else:
                    velocity_diff = np.abs(subData.ter_velocity.copy())

                    velocity_diff[velocity_diff < inner_fence] = np.nan
                    velocity_diff[velocity_diff > outer_fence] = np.nan

                    #Fill
                    filled_velocity = pd.Series(velocity_diff).interpolate()
                    bw_filter = butter_lowpass_filter(filled_velocity, cutoff, fs, order)

                    subL = [sub] * len(velocity_diff)
                    condL = [cond] * len(velocity_diff)
                    trialL = [t] * len(velocity_diff)

                if sub in ('ag', 'el', 'jp', 'kp', 'll', 'sm', 'vd', 'wt'):
                    group = 'stereo-normal'
                elif sub in ('by', 'co', 'gd', 'jr', 'lb', 'mb', 'gp', 'mr', 'ha', 'id', 'jc', 'mg', 'tp'):
                    group = 'stereo-anomalous'

                groupL = [group] * len(velocity_diff)

                sub_vals.append(subL)
                group_vals.append(groupL)
                cond_vals.append(condL)
                trial_vals.append(trialL)
                time_vals.append(subData.time)
                vel_vals.append(velocity_diff)
                vel_filled_vals.append(filled_velocity)
                vel_bw_filter.append(bw_filter)

    #return sub_vals, cond_vals, trial_vals, time_vals, vel_vals
    return sub_vals, group_vals, cond_vals, trial_vals, time_vals, vel_vals, vel_filled_vals, vel_bw_filter

# Function to make flat list
def makeFlatList(input_list):
    flatL = []

    for idx, itemL in enumerate(input_list):
        flat_list = [item for sublist in input_list[idx] for item in sublist]
        flatL.append(flat_list)

    return flatL

#sub_list, cond_list, trial_list, time_list, vel_diff_list = makeVelocityFillDataframe(data)
sub_list, group_list, cond_list, trial_list, time_list, vel_diff_list, vel_filled_list, vel_bw_filter_list = makeVelocityFillDataframe(data)

#list_of_lists = [sub_list, cond_list, trial_list, time_list, vel_diff_list]
list_of_lists = [sub_list, group_list, cond_list, trial_list, time_list, vel_diff_list, vel_filled_list, vel_bw_filter_list]


flatL = makeFlatList(list_of_lists)

#velFrames = {'subject': flatL[0], 'condition': flatL[1], 'trial': flatL[2], 'time': flatL[3], 'vel_diff': flatL[4]}
velFrames = {'subject': flatL[0], 'group': flatL[1], 'condition': flatL[2], 'trial': flatL[3], 'time': flatL[4], 'vel_diff': flatL[5], 'vel_filled': flatL[6], 'vel_bw': flatL[7]}

velDataFrame = pd.DataFrame(velFrames)
velDataFrame.to_csv(r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/data/abs_bw_velocity.csv', index=False)