import pandas as pd
import os
import numpy as np
from scipy.stats import gmean

# Takes in the dataframe csv file (reachingData.csv) created from buildReachingDataFrame.py and finds the distance between
# the thumb and grasping finger, which will ultimately give us the grasping vector.
# Creates grip pandas dataframe and saves it as graspingData.csv
# 6/24/21 Added grip calibration

myPath = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/data/'
os.chdir(myPath)

data = pd.read_csv('reachingData.csv')
grip_cal_data = pd.read_csv('grip_calibrations.csv')

subjects = data.subject.unique()
conditions = data.condition.unique()
trials = data.trial.unique()

def calculate_grip_geometric_mean(input_data):
    condition_grip = []
    subject_gmean_grip = []

    for cond in conditions:
        condition_sensor_distance = np.sqrt((input_data.sensor1_x[input_data.condition == cond] - input_data.sensor2_x[input_data.condition == cond])**2 + (
            input_data.sensor1_y[input_data.condition == cond] - input_data.sensor2_y[input_data.condition == cond]) **2 +
                                            (input_data.sensor1_z[input_data.condition == cond] - input_data.sensor2_z[input_data.condition == cond])**2)

        condition_grip.append(condition_sensor_distance)

    grip_list = [item for sublist in condition_grip for item in sublist]
    subject_gmean_grip = gmean(grip_list)

    return subject_gmean_grip

#test1 = calculate_grip_geometric_mean(grip_cal_data[grip_cal_data.subject == 'ag'])

def makeGraspingTrace():
    subject_vals = []
    condition_vals = []
    trial_vals = []
    distance_3d = []
    time_vals = []

    for sub in subjects:
        closed_grip_distance = calculate_grip_geometric_mean(grip_cal_data.loc[grip_cal_data.subject == sub])

        for cond in conditions:
            for t in trials:

                sub_data = data.loc[(data.subject == sub) & (data.condition == cond) & (data.trial == t)]


                if len(sub_data) == 0:
                    continue

                else:

                    # Step 1. Find distance between thumb and grasping finger in 3D
                    distance = np.sqrt((sub_data.grasping_finger_x - sub_data.thumb_x)**2 + (
                        sub_data.grasping_finger_y - sub_data.thumb_y)**2 + (
                        sub_data.grasping_finger_x - sub_data.thumb_z)**2) - closed_grip_distance

                    time = sub_data.time_stamp - sub_data.time_stamp.iloc[0]

                    subjectL = [sub] * len(distance)
                    conditionL = [cond] * len(distance)
                    trialL = [t] * len(distance)

                distance_3d.append(distance)
                subject_vals.append(subjectL)
                condition_vals.append(conditionL)
                trial_vals.append(trialL)
                time_vals.append(time)

    return subject_vals, condition_vals, trial_vals, distance_3d, time_vals

subject_list, condition_list, trial_list, distance_list, time_list = makeGraspingTrace()

sub_flat_list = [item for sublist in subject_list for item in sublist]
condition_flat_list = [item for sublist in condition_list for item in sublist]
trial_flat_list = [item for sublist in trial_list for item in sublist]
distance_flat_list = [item for sublist in distance_list for item in sublist]
time_flat_list = [item for sublist in time_list for item in sublist]

frames = {'subject': sub_flat_list, 'condition': condition_flat_list, 'trial': trial_flat_list, 'thumb_finger_distance': distance_flat_list, 'grip_time': time_flat_list}

dataFrame = pd.DataFrame(frames)

dataFrame['thumb_finger_distance'] = dataFrame['thumb_finger_distance'].astype(str).astype(float)
dataFrame['grip_time'] = dataFrame['grip_time'].astype(str).astype(float)

print(dataFrame.dtypes)

dataFrame.to_csv(r'C:/Users/angie/Git Root/stereo-prehension/data/graspingData.csv', index=False)