import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from general_functions import makeFlatList

# 6/16/21 Made function to calculate peak velocity per subject, trial and condition

myPath = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/data/'

os.chdir(myPath)

vel_data = pd.read_csv('abs_bw_velocity.csv')
g_data = pd.read_csv('graspingData.csv')

subjects = vel_data.subject.unique()
trials = vel_data.trial.unique()
conditions = vel_data.condition.unique()

def getReachingKinematics():
    subVals = []
    groupVals = []
    condVals = []
    trialVals = []
    pvTimeVals = []
    peakVelocity = []
    mgaTimeVals = []
    maxGAVals = []

    for sub in subjects:
        for cond in conditions:
            for t in trials:

                subData = vel_data.loc[(vel_data.subject == sub) & (vel_data.condition == cond) & (vel_data.trial == t)]
                grip_subData = g_data.loc[(g_data.subject == sub) & (g_data.condition == cond) & (g_data.trial == t)]

                if len(subData) == 0:
                    continue

                else:

                    pVelocity = subData.vel_bw.iloc[0:round(len(subData)/2)].max()
                    max_grip_aperture = grip_subData.position.iloc[0:round(len(grip_subData)/2)].max()

                    g = subData.group.iloc[0]

                    time_of_max_pv = subData.time.loc[subData.vel_bw == pVelocity].to_numpy()[0]
                    time_of_max_ga = grip_subData.time_stamp.loc[grip_subData.position == max_grip_aperture].to_numpy()[0]

                subVals.append([sub])
                groupVals.append([g])
                condVals.append([cond])
                trialVals.append([t])
                pvTimeVals.append([time_of_max_pv])
                peakVelocity.append([pVelocity])
                mgaTimeVals.append([time_of_max_ga])
                maxGAVals.append([max_grip_aperture])

    return subVals, groupVals, condVals, trialVals, pvTimeVals, peakVelocity, mgaTimeVals, maxGAVals

sub_list, group_list, cond_list, trial_list, pv_time_list, peakVel_list, mga_time_list, mga_list = getReachingKinematics()

list_of_lists = [sub_list, group_list, cond_list, trial_list, pv_time_list, peakVel_list, mga_time_list, mga_list]
flatL = makeFlatList(list_of_lists)

frame = {'subject': flatL[0], 'group': flatL[1], 'condition': flatL[2], 'trial': flatL[3], 'pv_time': flatL[4], 'pv': flatL[5], 'mga_time': flatL[6], 'mga': flatL[7]}

dFrame = pd.DataFrame(frame)
dFrame.to_csv(r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/data/kinematic_data.csv', index=False)
