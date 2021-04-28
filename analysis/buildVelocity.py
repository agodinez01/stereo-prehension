import pandas as pd
import os
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy import signal

# Takes in VelocityData.csv and creates dataframe to calculate standard deviation

myPath = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/Data/'

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

def makeWristVelocityDataFrame():
    subVals = []
    condVals = []
    trialVals = []
    velocityVals = []
    timeVals = []

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

                    now_time, previous_time = getNowandPrevious(subData.time[subData.direction == 'x'])

                    # Calculate the 3d position of the sensor on the wrist
                    wrist3d_position = np.sqrt((now_wrist_x_position - previous_wrist_x_position)**2
                                               + (now_wrist_y_position - previous_wrist_y_position)**2
                                               + (now_wrist_z_position - previous_wrist_z_position)**2)

                    velocity_diff = np.diff(wrist3d_position[1:])

                    subL = [sub] * len(velocity_diff)
                    condL = [cond] * len(velocity_diff)
                    trialL = [t] * len(velocity_diff)
                    velL = velocity_diff
                    timeL = now_time[:-2]

                subVals.append(subL)
                condVals.append(condL)
                trialVals.append(trialL)
                velocityVals.append(velL)
                timeVals.append(timeL)

    return subVals, condVals, trialVals, velocityVals, timeVals

sub_list, cond_list, trial_list, velocity_list, time_list = makeWristVelocityDataFrame()

sub_flat_list = [item for sublist in sub_list for item in sublist]
cond_flat_list = [item for sublist in cond_list for item in sublist]
trial_flat_list = [item for sublist in trial_list for item in sublist]
velocity_flat_list = [item for sublist in velocity_list for item in sublist]
time_flat_list = [item for sublist in time_list for item in sublist]

frames = {'subject': sub_flat_list, 'condition': cond_flat_list, 'trial': trial_flat_list, 'velocity': velocity_flat_list, 'time': time_flat_list}

dataFrame = pd.DataFrame(frames)

dataFrame['time'] = dataFrame['time'].astype(str).astype(float)

dataFrame.to_csv(r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/data/velocityData4Distribution.csv', index=False)

print(dataFrame['velocity'].mean())
print(dataFrame['velocity'].std())

sns.distplot(dataFrame.velocity, kde=True, rug=True)
plt.show()


data