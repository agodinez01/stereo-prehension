import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

myPath = r'C:/Users/angie/Git Root/stereo-prehension/data/'
os.chdir(myPath)

data = pd.read_csv('reachingData.csv')

subjects = data.subject.unique()
conditions = data.condition.unique()
trials = data.trial.unique()

def makeVelocityTrace():
    subject_vals = []
    condition_vals = []
    trial_vals = []
    position_3d = []

    for sub in subjects:
        for cond in conditions:
            for t in trials:

                if len(data[(data.subject == sub) & (data.condition == cond) & (data.trial == t)]) == 0:
                    position = 'nan'

                else:
                    wrist_x_now_position = data.wrist_x[(data.subject == sub) & (data.condition == cond) & (data.trial == t)]
                    wrist_x_previous_position = np.hstack((data.wrist_x[(data.subject == sub) & (data.condition == cond) & (data.trial == t)][-1:], data.wrist_x[(data.subject == sub) & (data.condition == cond) & (data.trial == t)][:-1]))

                    wrist_y_now_position = data.wrist_y[(data.subject == sub) & (data.condition == cond) & (data.trial == t)]
                    wrist_y_previous_position = np.hstack((data.wrist_y[(data.subject == sub) & (data.condition == cond) & (data.trial == t)][-1:], data.wrist_y[(data.subject == sub) & (data.condition == cond) & (data.trial == t)][:-1]))

                    wrist_z_now_position = data.wrist_z[(data.subject == sub) & (data.condition == cond) & (data.trial == t)]
                    wrist_z_previous_position = np.hstack((data.wrist_z[(data.subject == sub) & (data.condition == cond) & (data.trial == t)][-1:], data.wrist_z[(data.subject == sub) & (data.condition == cond) & (data.trial == t)][:-1]))

                    position = np.sqrt((wrist_x_now_position - wrist_x_previous_position)**2 + (wrist_y_now_position - wrist_y_previous_position)**2 + (wrist_z_now_position - wrist_z_previous_position)**2)
                    subjectL = [sub] * len(position)
                    conditionL = [cond] * len(position)
                    trialL = [t] * len(position)

                position_3d.append(position)
                subject_vals.append(subjectL)
                condition_vals.append(conditionL)
                trial_vals.append(trialL)


    return subject_vals, condition_vals, trial_vals, position_3d

subject_list, condition_list, trial_list, position_list = makeVelocityTrace()

sub_flat_list = [item for sublist in subject_list for item in sublist]
condition_flat_list = [item for sublist in condition_list for item in sublist]
trial_flat_list = [item for sublist in trial_list for item in sublist]
position_flat_list = [item for sublist in position_list for item in sublist]

frames = {'subject': sub_flat_list, 'condition': condition_flat_list, 'trial': trial_flat_list, 'position': position_flat_list}

#sub_list = pd.Series((item[0] for item in subject_list))
#cond_list = pd.Series((item[0] for item in condition_list))
#t_list = pd.Series((item[0] for item in trial_list))
#frames = [subject_list, position_list]

#frames = [sub_list, cond_list, t_list, position_list]
dataFrame = pd.DataFrame(frames)

data






data