import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy

myPath = r'C:/Users/angie/Git Root/stereo-prehension/data/'
fig_dir = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/figs/velocity_traces/'

os.chdir(myPath)

data = pd.read_csv('velocityData.csv')

subjects = data.subject.unique()
conditions = data.condition.unique()
trials = data.trial.unique()
sensors = data.sensor.unique()
directions = data.direction.unique()

# Function for sensor now and sensor previous
def getNowandPrevious(sdata):

    # Convert to numpy array in order to be able to subtract later
    now_position = sdata.to_numpy()
    previous_position = pd.Series(np.hstack((sdata[-1:], sdata[:-1]))).to_numpy()

    return now_position, previous_position

def makeFig(sub, cond, t, velocity, time):
    plt.plot(time, velocity)
    #plt.plot(subData.time_stamp[(subData.subject == sub) & (subData.condition == cond) & (subData.trial == t)])

    plt.title(sub + ' ' + cond + ' ' + str(t))
    plt.xlabel('Time')
    plt.ylabel('Velocity')

    fig_name = 'velocity_' + sub + '_' + cond + '_' + str(t) + '.png'

    plt.savefig(fname=fig_dir + fig_name, bbox_inches='tight', format='png', dpi=300)
    plt.clf()

for sub in subjects:
    for cond in conditions:
        for t in trials:

            subData = data.loc[(data.subject == sub) & (data.condition == cond) & (data.trial == t) & (data.sensor == 'wrist')]

            # Get the position of the sensor now and the previous position, which means that we  circularly shift the array/series
            now_wrist_x_position, previous_wrist_x_position = getNowandPrevious(subData.position[subData.direction == 'x'])
            now_wrist_y_position, previous_wrist_y_position = getNowandPrevious(subData.position[subData.direction == 'y'])
            now_wrist_z_position, previous_wrist_z_position = getNowandPrevious(subData.position[subData.direction == 'z'])

            now_time, previous_time = getNowandPrevious(subData.time_stamp[subData.sensor == 'x'])

            # Calculate the 3d position of the sensor on the wrist
            wrist3d_position = np.sqrt((now_wrist_x_position - previous_wrist_x_position)**2
                                       + (now_wrist_y_position - previous_wrist_y_position)**2
                                       + (now_wrist_z_position - previous_wrist_z_position)**2)

            # Take the derivative of the 3d position
            velocity = np.diff(wrist3d_position)
            makeFig(sub, cond, t, velocity, now_time)

            #smoothed_velocity = scipy.signal.savgol_filter(velocity,5,2)


data