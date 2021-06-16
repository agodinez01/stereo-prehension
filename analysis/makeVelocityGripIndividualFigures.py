import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy import signal

# Takes vel_data_with_Ter_analysis and compares my analysis with Terence's 2016 analysis.

run_figures = 0 # 1 = run figures; 0 = make dataframe without figures

myPath = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/data/'
fig_dir = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/figs/velocity_and_grasp/'

os.chdir(myPath)

data = pd.read_csv('vel_data_with_Ter_analysis2.csv')
grasp_data = pd.read_csv('graspingData.csv')

subjects = data.subject.unique()
conditions = data.condition.unique()
trials = data.trial.unique()

# Plot variables
colors = ['#cfcfcf', '#FF0000', '#000000', '#4b4b4b', '#8BC34A'] #light grey, red, black, dark grey, green

# Add butterworth low-pass filter
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

# Get a visual
def makeFig(sub, cond, t, subData, gData, bw_vel):
    fig, axs = plt.subplots(2, 1, sharex=True)

    axs[0].set_title(sub + ' ' + cond + ' ' + str(t))
    axs[0].plot(subData['time'], np.abs(subData['ter_velocity']), color=colors[4])
    axs[0].plot(subData['time'], bw_vel, color=colors[2])
    axs[0].set_ylabel('Velocity (cm/s)')
    axs[0].set_ylim(-10, 280)

    axs[1].plot(gData['time_stamp'], gData['position'])
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Grip')
    axs[1].set_ylim(10, 80)

    fig_name = sub + '_' + cond + '_' + str(t) + '.png'
    plt.savefig(fname=fig_dir + fig_name, bbox_inches='tight', format='png', dpi=300)

    #plt.show()
    plt.clf()
    plt.close('all')

for sub in subjects:
    for cond in conditions:
        for t in trials:

            subData = data.loc[(data.subject == sub) & (data.condition == cond) & (data.trial == t)]
            gData = grasp_data.loc[(grasp_data.subject == sub) & (grasp_data.condition == cond) & (grasp_data.trial == t)]

            if len(subData) == 0:
                continue

            else:
                bw_vel = butter_lowpass_filter(np.abs(subData['ter_velocity']), cutoff, fs, order)

                makeFig(sub, cond, t, subData, gData, bw_vel)

# Define function to make velocity dataframe and save to csv
def makeVelocityFillDataframe(input_data):
    sub_vals = []
    cond_vals = []
    trial_vals = []
    time_vals = []
    vel_filled = []
    vel_bw_filter = []

    for sub in subjects:
        for cond in conditions:
            for t in trials:

                subData = input_data.loc[
                    (input_data.subject == sub) & (input_data.condition == cond) & (input_data.trial == t)]

                if len(subData) == 0:
                    continue

                else:
                    velocity_diff = subData.velocity.copy()

                    velocity_diff[velocity_diff < -7.07] = np.nan
                    velocity_diff[velocity_diff > 7.12] = np.nan

                    velocity_absolute = np.absolute(velocity_diff)

                    now_time = subData.time - subData.time.min()

                    # #Fill
                    filled_absolute = pd.Series(velocity_absolute).fillna(limit=100, method='ffill')
                    butterworth_velocity_absolute = butter_lowpass_filter(filled_absolute, cutoff, fs, order)

                    filled_reg = pd.Series(velocity_diff).fillna(limit=100, method='ffill')
                    butterworth_velocity_reg = butter_lowpass_filter(filled_reg, cutoff, fs, order)

                    subL = [sub] * len(velocity_absolute)
                    condL = [cond] * len(velocity_absolute)
                    trialL = [t] * len(velocity_absolute)

                sub_vals.append(subL)
                cond_vals.append(condL)
                trial_vals.append(trialL)
                time_vals.append(now_time)
                vel_diff_vals.append(velocity_diff)
                vel_abs.append(velocity_absolute)
                vel_filled.append(filled_absolute)
                vel_bw_filter.append(butterworth_velocity_absolute)

    return sub_vals, cond_vals, trial_vals, time_vals, vel_diff_vals, vel_abs, vel_filled, vel_bw_filter

# Function to make flat list
def makeFlatList(input_list):
    flatL = []

    for idx, itemL in enumerate(input_list):
        flat_list = [item for sublist in input_list[idx] for item in sublist]
        flatL.append(flat_list)

    return flatL