import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy import signal

#Takes velocityData4Distribution.csv and makes reach velocity figures.

myPath = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/Data/'
fig_dir = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/figs/butterworth_velocity/moreFill/'

os.chdir(myPath)

data = pd.read_csv('velocityData4Distribution.csv')

subjects = data.subject.unique()
conditions = data.condition.unique()
trials = data.trial.unique()

# Add butterworth low-pass filter
T = 1
fs = 100.0
cutoff = 3
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

def makeFig(sub, cond, t, time, bw_velocity_abs, filled_abs, bw_velocity_reg, filled_reg):

    fig, axs = plt.subplots(2, 1, sharex=True)
    axs[0].set_title(sub + ' ' + cond + str(t))
    axs[0].plot(time, filled_abs, color=colors[0])
    axs[0].plot(time, bw_velocity_abs, color=colors[2])
    axs[0].set_ylabel('Absolute velocity')
    axs[0].set_ylim(-1, 9)
    #axs[0].set_legend(['Raw data', 'Butterworth'], loc='upper left')

    axs[1].plot(time, filled_reg, color=colors[0])
    axs[1].plot(time, bw_velocity_reg, color=colors[1])
    axs[1].set_ylabel('Bi-directional velocity')
    axs[1].set_ylim(-8, 8)
    axs[1].set_xlabel('Time (secs)')
    #axs[1].set_legend(['Raw data', 'Butterworth'], loc='upper left')

    #fig.plt.title(sub + ' ' + cond + str(t))

    #plt.plot(time, filled, color=colors[0])
    #plt.plot(time, bw_velocity, color=colors[2])
    #plt.plot(time, savgol_velocity, color=colors[2])

    #plt.title(sub + ' ' + cond + ' ' + str(t))
    #plt.xlabel('Time (secs)')
    #plt.ylabel('Velocity')


    #plt.ylim(-1, 9)
    #plt.legend(['Raw data', 'Butterworth'], loc='upper left')

    fig_name = 'raw_bw_' + sub + '_' + cond + '_' + str(t) + '.png'

    #plt.show()
    plt.savefig(fname=fig_dir + fig_name, bbox_inches='tight', format='png', dpi=300)
    plt.clf()
    plt.close('all')

for sub in subjects:
    for cond in conditions:
        for t in trials:

                subData = data.loc[
                    (data.subject == sub) & (data.condition == cond) & (data.trial == t)]

                if len(subData) == 0:
                    continue

                else:
                    velocity_diff = subData.velocity.copy()

                    velocity_diff[velocity_diff < -7.07] = np.nan
                    velocity_diff[velocity_diff > 7.12] = np.nan

                    velocity_absolute = np.absolute(velocity_diff)

                    #now_t = subData.time.copy()
                    now_time = subData.time - subData.time.min()

                    # #Fill
                    filled_absolute = pd.Series(velocity_absolute).fillna(limit=100, method='ffill')
                    butterworth_velocity_absolute = butter_lowpass_filter(filled_absolute, cutoff, fs, order)

                    filled_reg = pd.Series(velocity_diff).fillna(limit=100, method='ffill')
                    butterworth_velocity_reg = butter_lowpass_filter(filled_reg, cutoff, fs, order)

                    #s_velocity = savgol_filter(filled, 41, 3)
                    #sav_gol_velocity = pd.Series(s_velocity)
                    makeFig(sub, cond, t, now_time, butterworth_velocity_absolute, filled_absolute, butterworth_velocity_reg, filled_reg)

