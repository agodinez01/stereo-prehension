import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy import signal
import seaborn as sns
from general_functions import butter_lowpass_filter
from general_functions import makeFlatList

myPath = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/Data/'

os.chdir(myPath)

data = pd.read_csv('graspingData.csv')

subjects = data.subject.unique()
conditions = data.condition.unique()
trials = data.trial.unique()

# # Low-pass Butterworth variables for function butter_lowpass_filter
# T = 1
# fs = 50.0
# cutoff = 3
# nyq = 0.5 * fs
# order = 2
# n = int(T * fs)

# Define function to make 'change in grip' dataframe and save to csv

def makeChangeInGrip(input_data):
    sub_vals = []
    group_vals = []
    cond_vals = []
    trial_vals = []
    time_vals = []
    thumb_finger_distance_vals = []
    raw_grip_change_vals = []
    smooth_grip_change_vals = []

    for sub in subjects:
        for cond in conditions:
            for t in trials:

                subData = input_data.loc[
                    (input_data.subject == sub) & (input_data.condition == cond) & (input_data.trial == t)]

                if len(subData) == 0:
                    continue

                else:

                    grip_change = pd.Series(subData.grip_change)
                    smooth_grip_change = butter_lowpass_filter(grip_change)

                    subL = [sub] * len(grip_change)
                    condL = [cond] * len(grip_change)
                    trialL = [t] * len(grip_change)

                if sub in ('ag', 'el', 'jp', 'kp', 'll', 'sm', 'vd', 'wt'):
                    group = 'stereo-normal'
                elif sub in ('by', 'co', 'gd', 'jr', 'lb', 'mb', 'gp', 'mr', 'ha', 'id', 'jc', 'mg', 'tp'):
                    group = 'stereo-anomalous'

                groupL = [group] * len(grip_change)

                sub_vals.append(subL)
                group_vals.append(groupL)
                cond_vals.append(condL)
                trial_vals.append(trialL)
                time_vals.append(subData.grip_time)
                thumb_finger_distance_vals.append(subData.thumb_finger_distance)
                raw_grip_change_vals.append(subData.grip_change)
                smooth_grip_change_vals.append(smooth_grip_change)

    return sub_vals, group_vals, cond_vals, trial_vals, time_vals, thumb_finger_distance_vals, raw_grip_change_vals, smooth_grip_change_vals

sub_list, group_list, cond_list, trial_list, time_list, thumb_finger_distance_list, raw_grip_list, smooth_grip_list = makeChangeInGrip(data)

list_of_lists = [sub_list, group_list, cond_list, trial_list, time_list, thumb_finger_distance_list, raw_grip_list, smooth_grip_list]

flatL = makeFlatList(list_of_lists)

gripFrames = {'subject': flatL[0], 'group': flatL[1], 'condition': flatL[2], 'trial': flatL[3], 'grip_time': flatL[4], 'thumb_finger_distance': flatL[5], 'raw_grip': flatL[6], 'smooth_grip': flatL[7]}
gripDataFrame = pd.DataFrame(gripFrames)

gripDataFrame.to_csv(r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/data/grip_and_derivative.csv', index=False)
