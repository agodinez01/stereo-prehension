import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy import signal

myPath = r'C:/Users/angie/Git Root/stereo-prehension/data/'
fig_dir = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/figs/velocity_traces_truncated/'

os.chdir(myPath)

data = pd.read_csv('velocityData.csv')

subjects = data.subject.unique()
conditions = data.condition.unique()
trials = data.trial.unique()
sensors = data.sensor.unique()
directions = data.direction.unique()

# Add butterworth low-pass filter
T = .13
fs = 30.0
cutoff = 2
nyq = 0.5 * fs
order = 2
n = int(T * fs)

# Plot variables
colors = ['#cfcfcf', '#FF0000', '#000000', '#4b4b4b'] #light grey, red, black, dark grey

# Function for sensor now and sensor previous
def getNowandPrevious(sdata):

    # Convert to numpy array in order to be able to subtract later
    now_position = sdata.to_numpy()
    previous_position = pd.Series(np.hstack((sdata[-1:], sdata[:-1]))).to_numpy()

    return now_position, previous_position

def butter_lowpass_filter(input_data, cuttoff, fs, order):
    normal_cutoff = cutoff / nyq

    # Get filter coefficients
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    y = signal.filtfilt(b, a, input_data)

    return y

def makeFig(sub, cond, t, time, velocity, filled, smoothed_velocity):
    # Cut two points from time and one from velocity due to the circular shift and derivation.

    plt.plot(time[:-2], filled, color=colors[0])
    plt.plot(time[:-2], velocity, color=colors[1])
    #plt.plot(time[:-2], velocity, color=colors[1])
    plt.plot(time[:-2], smoothed_velocity, color=colors[2])

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

            subData = data.loc[(data.subject == sub) & (data.condition == cond) & (data.trial == t) & (data.sensor == 'wrist')]

            if len(subData) == 0:
                continue

            else:

                # Get the position of the sensor now and the previous position, which means that we  circularly shift the array/series
                now_wrist_x_position, previous_wrist_x_position = getNowandPrevious(subData.position[subData.direction == 'x'])
                now_wrist_y_position, previous_wrist_y_position = getNowandPrevious(subData.position[subData.direction == 'y'])
                now_wrist_z_position, previous_wrist_z_position = getNowandPrevious(subData.position[subData.direction == 'z'])

                now_time, previous_time = getNowandPrevious(subData.time_stamp[subData.direction == 'x'])

                # Calculate the 3d position of the sensor on the wrist
                wrist3d_position = np.sqrt((now_wrist_x_position - previous_wrist_x_position)**2
                                           + (now_wrist_y_position - previous_wrist_y_position)**2
                                           + (now_wrist_z_position - previous_wrist_z_position)**2)

                velocity_diff = np.diff(wrist3d_position[1:])

                velocity_diff[velocity_diff < -0.04] = np.nan
                velocity_diff[velocity_diff > 0.04] = np.nan

                #Fill
                filled = pd.Series(velocity_diff).fillna(limit=10, method='ffill')

                velocity = butter_lowpass_filter(filled, cutoff, fs, order)
                smoothed_velocity = savgol_filter(velocity, 61, 2)

                makeFig(sub, cond, t, now_time, velocity, filled, smoothed_velocity)



