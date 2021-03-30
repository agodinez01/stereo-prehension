import pandas as pd
import os
import numpy as np

myPath = r'C:/Users/angie/Git Root/stereo-prehension/data/'
os.chdir(myPath)

data = pd.read_csv('reachingData.csv')

subjects = data.subject.unique()
conditions = data.condition.unique()
trials = data.trial.unique()

def makeGraspingTrace():
    subject_vals = []
    condition_vals = []
    trial_vals = []
    distance_3d = []
    time_vals = []

    for sub in subjects:
        sub_data = data.loc[(data.subject == sub)]
        for cond in conditions:
            for t in trials:

                sub_data = data.loc[(data.subject == sub) & (data.condition == cond) & (data.trial == t)]

                if len(sub_data) == 0:
                    continue

                else:

                    # Step 1. Find distance between thumb and grasping finger in 3D
                    distance = np.sqrt((sub_data.grasping_finger_x - sub_data.thumb_x)**2 + (
                        sub_data.grasping_finger_y - sub_data.thumb_y)**2 + (
                        sub_data.grasping_finger_x - sub_data.thumb_z)**2)

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

frames = {'subject': sub_flat_list, 'condition': condition_flat_list, 'trial': trial_flat_list, 'position': distance_flat_list, 'time_stamp': time_flat_list}

dataFrame = pd.DataFrame(frames)

dataFrame['position'] = dataFrame['position'].astype(str).astype(float)
dataFrame['time_stamp'] = dataFrame['time_stamp'].astype(str).astype(float)

print(dataFrame.dtypes)

dataFrame.to_csv(r'C:/Users/angie/Git Root/stereo-prehension/data/graspingData.csv', index=False)

# function to get now and previous sensor position
# def get_position(data):
#     now_position = data
#     previous_position = pd.Series(np.hstack((data[-1:], data[:-1])))
#
#     return now_position, previous_position

# finger_x_now_position, finger_x_previous_position = get_position(sub_data.grasping_finger_x[(sub_data.condition == cond) & (sub_data.trial == t)])
# finger_y_now_position, finger_y_previous_position = get_position(sub_data.grasping_finger_y[(sub_data.condition == cond) & (sub_data.trial == t)])
# finger_z_now_position, finger_z_previous_position = get_position(sub_data.grasping_finger_z[(sub_data.condition == cond) & (sub_data.trial == t)])
#
# thumb_x_now_position, thumb_x_previous_position = get_position(sub_data.thumb_x[(sub_data.condition == cond) & (sub_data.trial == t)])
# thumb_y_now_position, thumb_y_previous_position = get_position(sub_data.thumb_y[(sub_data.condition == cond) & (sub_data.trial == t)])
# thumb_z_now_position, thumb_z_previous_position = get_position(
#     sub_data.thumb_z[(sub_data.condition == cond) & (sub_data.trial == t)])

# finger_position = np.sqrt((finger_x_now_position[2:] - finger_x_previous_position[2:])**2 + (finger_y_now_position[2:] - finger_y_previous_position[2:])**2 + (finger_z_now_position[2:] - finger_z_previous_position[2:])**2)

# wrist_x_now_position = sub_data.wrist_x[(sub_data.condition == cond) & (sub_data.trial == t)]
# wrist_x_previous_position = np.vstack((sub_data.wrist_x[(sub_data.condition == cond) & (sub_data.trial == t)][-1:], sub_data.wrist_x[(sub_data.condition == cond) & (sub_data.trial == t)][:-1]))

# wrist_y_now_position = sub_data.wrist_y[(sub_data.condition == cond) & (sub_data.trial == t)]
# wrist_y_previous_position = np.hstack((sub_data.wrist_y[(sub_data.condition == cond) & (sub_data.trial == t)][-1:], sub_data.wrist_y[(sub_data.condition == cond) & (sub_data.trial == t)][:-1]))

# wrist_z_now_position = data.wrist_z[(data.subject == sub) & (data.condition == cond) & (data.trial == t)]
# wrist_z_previous_position = np.hstack((sub_data.wrist_z[(sub_data.condition == cond) & (sub_data.trial == t)][-1:], sub_data.wrist_z[(sub_data.condition == cond) & (sub_data.trial == t)][:-1]))

# x = np.arange(0, len(wrist_x_now_position), step=1)

# position = np.sqrt((wrist_x_now_position - wrist_x_previous_position)**2 + (wrist_y_now_position - wrist_y_previous_position)**2 + (wrist_z_now_position - wrist_z_previous_position)**2)



# def get_distance():
#     subject_vals = []
#     condition_vals = []
#     trial_vals = []
#     distance_vals = []
#
#     for sub in subjects:
#         sub_data = data.loc[data.subject == sub]
#
#         for cond in conditions:
#             for t in trials:
#
#                 distance = np.sqrt(
#
#                     sub_data[(sub_data.condition == cond) & (sub_data.trial == t]