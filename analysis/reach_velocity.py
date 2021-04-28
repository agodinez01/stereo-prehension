import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy import signal

#Takes velocityData4Distribution.csv and makes reach velocity figures.

myPath = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/Data/'
fig_dir = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/figs/velocity_traces_truncated/'

os.chdir(myPath)

data = pd.read_csv('velocityData4Distribution.csv')

subjects = data.subject.unique()
conditions = data.condition.unique()
trials = data.trial.unique()

# Add butterworth low-pass filter
T = 0.25
fs = 30.0
cutoff = 2
nyq = 0.5 * fs
order = 2
n = int(T * fs)

# Plot variables
colors = ['#cfcfcf', '#FF0000', '#000000', '#4b4b4b'] #light grey, red, black, dark grey

def butter_lowpass_filter(input_data, cuttoff, fs, order):
    normal_cutoff = cutoff / nyq

    # Get filter coefficients
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    y = signal.filtfilt(b, a, input_data)

    return y

def makeFig(sub, cond, t, time, velocity, filled, smoothed_velocity):
    # Cut two points from time and one from velocity due to the circular shift and derivation.

    plt.plot(time, filled, color=colors[0])
    plt.plot(time, velocity, color=colors[1])
    plt.plot(time, smoothed_velocity, color=colors[2])

    plt.title(sub + ' ' + cond + ' ' + str(t))
    plt.xlabel('Time')
    plt.ylabel('Velocity')

    plt.ylim(-0.075, 0.075)
    plt.legend(['Raw data', 'Butterworth', 'Sav-Gol'], loc='upper left')

    fig_name = 'smoothed_velocity_' + sub + '_' + cond + '_' + str(t) + '.png'

    plt.show()
    #plt.savefig(fname=fig_dir + fig_name, bbox_inches='tight', format='png', dpi=300)
    plt.clf()

for sub in subjects:
    for cond in conditions:
        for t in trials:

                subData = data.loc[
                    (data.subject == sub) & (data.condition == cond) & (data.trial == t)]

                if len(subData) == 0:
                    continue

                else:
                    velocity_diff = subData.velocity.copy()
                    velocity_diff[velocity_diff < -3.57] = np.nan
                    velocity_diff[velocity_diff > 3.57] = np.nan

                    now_time = subData.time.copy()

                    # #Fill
                    filled = pd.Series(velocity_diff).fillna(limit=10, method='ffill')

                    velocity = butter_lowpass_filter(filled, cutoff, fs, order)
                    s_velocity = savgol_filter(velocity, 61, 2)
                    smoothed_velocity = pd.Series(s_velocity)
                    makeFig(sub, cond, t, now_time, velocity, filled, smoothed_velocity)

