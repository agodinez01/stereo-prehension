import pandas as pd
import os
import numpy as np

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
    typeVals = []
    condVals = []
    trialVals = []
    velocityVals = []
    timeVals = []
    tDiffVals = []

    for sub in subjects:
        for cond in conditions:
            for t in trials:

                subData = data.loc[(data.subject == sub) & (data.condition == cond) & (data.trial == t) & (data.sensor == 'wrist')]
                subData2 = data.loc[(data.subject == sub) & (data.condition == cond) & (data.trial == t)]

                if len(subData) == 0:
                    continue

                else:

                    # Get the position of the sensor now and the previous position, which means that we  circularly shift the array/series
                    now_wrist_x_position, previous_wrist_x_position = getNowandPrevious(subData.position[subData.direction == 'x'])
                    now_wrist_y_position, previous_wrist_y_position = getNowandPrevious(subData.position[subData.direction == 'y'])
                    now_wrist_z_position, previous_wrist_z_position = getNowandPrevious(subData.position[subData.direction == 'z'])

                    now_time, previous_time = getNowandPrevious(subData.time[subData.direction == 'x'])
                    real_now_time = now_time - now_time[0]
                    real_previous_time = previous_time - now_time[0]

                    # Calculate the 3d position of the sensor on the wrist
                    wrist3d_position = np.sqrt((np.abs(previous_wrist_x_position) - np.abs(now_wrist_x_position))**2
                                               + (np.abs(previous_wrist_y_position) - np.abs(now_wrist_y_position))**2
                                               + (np.abs(previous_wrist_z_position) - np.abs(now_wrist_z_position))**2)

                    poltimedifference = real_previous_time - real_now_time

                    a = wrist3d_position/ poltimedifference

                    # Terence way
                    # For Terence analysis, calculate previous and current position for finger and thumb sensor.
                    now_finger_x_position, previous_finger_x_position = getNowandPrevious(
                        subData2.position[(subData2.sensor == 'finger') & (subData2.direction == 'x')])
                    now_finger_y_position, previous_finger_y_position = getNowandPrevious(
                        subData2.position[(subData2.sensor == 'finger') & (subData2.direction == 'y')])
                    now_finger_z_position, previous_finger_z_position = getNowandPrevious(
                        subData2.position[(subData2.sensor == 'finger') & (subData2.direction == 'z')])

                    now_thumb_x_position, previous_thumb_x_position = getNowandPrevious(
                        subData2.position[(subData2.sensor == 'thumb') & (subData2.direction == 'x')])
                    now_thumb_y_position, previous_thumb_y_position = getNowandPrevious(
                        subData2.position[(subData2.sensor == 'thumb') & (subData2.direction == 'y')])
                    now_thumb_z_position, previous_thumb_z_position = getNowandPrevious(
                        subData2.position[(subData2.sensor == 'thumb') & (subData2.direction == 'z')])

                    polVelocityReal = ((np.sqrt((np.abs(previous_finger_x_position) - np.abs(now_finger_x_position)) ** 2
                                              + (np.abs(previous_finger_y_position) - np.abs(now_finger_y_position)) ** 2
                                              + (np.abs(previous_finger_z_position) - np.abs(now_finger_z_position)) ** 2)) / poltimedifference) + \
                                      ((np.sqrt((np.abs(previous_thumb_x_position) - np.abs(now_thumb_x_position)) ** 2
                                              + (np.abs(previous_thumb_y_position) - np.abs(now_thumb_y_position)) ** 2
                                              + (np.abs(previous_thumb_z_position) - np.abs(now_thumb_z_position)) ** 2)) / poltimedifference) / 2

                    if sub in ('ag', 'el', 'jp', 'kp', 'll', 'sm', 'vd', 'wt'):
                        type = 'stereo-normal'
                    elif sub in ('by', 'co', 'gd', 'jr', 'lb', 'mb', 'gp', 'mr', 'ha', 'id', 'jc', 'mg', 'tp'):
                        type = 'stereo-anomalous'

                    subL = [sub] * len(a)
                    typeL = [type] * len(a)
                    condL = [cond] * len(a)
                    trialL = [t] * len(a)
                    timeL = real_now_time

                subVals.append(subL)
                typeVals.append(typeL)
                condVals.append(condL)
                trialVals.append(trialL)
                timeVals.append(timeL)
                velocityVals.append(a)
                tDiffVals.append(polVelocityReal)

    return subVals, typeVals, condVals, trialVals, velocityVals, timeVals, tDiffVals

sub_list, type_list, cond_list, trial_list, velocity_list, time_list, tDiff_list = makeWristVelocityDataFrame()

sub_flat_list = [item for sublist in sub_list for item in sublist]
type_flat_list = [item for sublist in type_list for item in sublist]
cond_flat_list = [item for sublist in cond_list for item in sublist]
trial_flat_list = [item for sublist in trial_list for item in sublist]
velocity_flat_list = [item for sublist in velocity_list for item in sublist]
time_flat_list = [item for sublist in time_list for item in sublist]
tDiff_flat_list = [item for sublist in tDiff_list for item in sublist]

frames = {'subject': sub_flat_list, 'type': type_flat_list, 'condition': cond_flat_list, 'trial': trial_flat_list, 'time': time_flat_list, 'velocity': velocity_flat_list, 'ter_velocity': tDiff_flat_list}

dataFrame = pd.DataFrame(frames)

dataFrame['time'] = dataFrame['time'].astype(str).astype(float)

dataFrame.to_csv(r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/data/vel_data_with_Ter_analysis2.csv', index=False)