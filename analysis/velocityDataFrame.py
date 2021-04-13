import pandas as pd
import os
import numpy as np

myPath = r'C:/Users/angie/Git Root/stereo-prehension/data/'
os.chdir(myPath)

data = pd.read_csv('reachingData.csv')

subjects = data.subject.unique()
conditions = data.condition.unique()
trials = data.trial.unique()

def makeVelocityDataFrame():
    subjectVals = []
    conditionVals = []
    trialVals = []
    sensorVals = []
    directionVals = []
    timeVals = []
    positionVals = []

    for sub in subjects:
        for cond in conditions:
            for t in trials:

                subData = data.loc[(data.subject == sub) & (data.condition == cond) & (data.trial == t)]

                if len(subData) == 0:
                    continue

                else:

                    position = np.hstack((subData.grasping_finger_x, subData.grasping_finger_y, subData.grasping_finger_z,
                                          subData.thumb_x, subData.thumb_y, subData.thumb_z, subData.wrist_x, subData.wrist_y, subData.wrist_z))

                    subL = [sub] * len(subData) * 9
                    condL = [cond] * len(subData) * 9
                    trialL = [t] * len(subData) * 9

                    sensorL = np.hstack((['finger'] * len(subData) * 3, ['thumb'] * len(subData)* 3,
                                         ['wrist'] * len(subData) * 3))

                    directionL = np.hstack((['x'] * len(subData), ['y'] * len(subData), ['z'] * len(subData),
                                         ['x'] * len(subData), ['y'] * len(subData), ['z'] * len(subData),
                                         ['x'] * len(subData), ['y'] * len(subData), ['z'] * len(subData)))

                    timeL = np.hstack(([subData.time_stamp] * 9))

                subjectVals.append(subL)
                conditionVals.append(condL)
                trialVals.append(trialL)
                sensorVals.append(sensorL)
                directionVals.append(directionL)
                timeVals.append(timeL)
                positionVals.append(position)

    return subjectVals, conditionVals, trialVals, sensorVals, directionVals, timeVals, positionVals

sub_list, cond_list, trial_list, sensor_list, direction_list, time_list, position_list = makeVelocityDataFrame()

sub_flat_list = [item for sublist in sub_list for item in sublist]
cond_flat_list = [item for sublist in cond_list for item in sublist]
trial_flat_list = [item for sublist in trial_list for item in sublist]
sensor_flat_list = [item for sublist in sensor_list for item in sublist]
direction_flat_list = [item for sublist in direction_list for item in sublist]
time_flat_list = [item for sublist in time_list for item in sublist]
position_flat_list = [item for sublist in position_list for item in sublist]

frames = {'subject': sub_flat_list, 'condition': cond_flat_list, 'trial': trial_flat_list, 'sensor': sensor_flat_list, 'direction': direction_flat_list,
          'time': time_flat_list, 'position': position_flat_list}

dataFrame = pd.DataFrame(frames)

dataFrame.to_csv(r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/Data/velocityData.csv', index=False)




