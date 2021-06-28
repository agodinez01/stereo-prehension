import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy import signal
from general_functions import makeFlatList

# 5/08/21 Created funtion to produce list of trials that should be excluded.

# Function to print out a list of trials that should be excluded.
# Excluding criteria includes trials where velocity start (first five values) is greater than 0.5
# or grip aperture is greater than 30 (though this should be changed!) Need to calibrate grip.

myPath = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/Data/'
#fig_dir = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/figs/velocity_and_grasp/'

os.chdir(myPath)

vel_data = pd.read_csv('abs_bw_velocity.csv')
grasp_data = pd.read_csv('graspingData.csv')

subjects = vel_data.subject.unique()
conditions = vel_data.condition.unique()
trials = vel_data.trial.unique()

def spitExludedTrials():
    subVals = []
    condVals = []
    trialVals = []
    trial_exclusion = []
    velVals = []
    graspVals = []

    for sub in subjects:
        for cond in conditions:
            for t in trials:

                vel_start_avg = vel_data.vel_bw[(vel_data.subject == sub) & (vel_data.condition == cond) & (vel_data.trial == t)][0:4].mean()
                grasp_start_avg = grasp_data.position[(grasp_data.subject == sub) & (grasp_data.condition == cond) & (grasp_data.trial == t)][0:4].mean()

                if (vel_start_avg > 2) or (grasp_start_avg > 25):
                    trial_EI = 'Exclude'

                else:
                    trial_EI = 'Include'

                subL = [sub]
                condL = [cond]
                trialL = [t]

                subVals.append(subL)
                condVals.append(condL)
                trialVals.append(trialL)
                trial_exclusion.append(trial_EI)
                velVals.append(vel_start_avg)
                graspVals.append(grasp_start_avg)

    return subVals, condVals, trialVals, trial_exclusion, velVals, graspVals

sub_list, cond_list, trial_list, trial_exclusion_list, vel_list, grasp_list = spitExludedTrials()

list_of_lists = [sub_list, cond_list, trial_list, trial_exclusion_list, vel_list, grasp_list]
flatL = makeFlatList(list_of_lists)

frame = {'subject': flatL[0], 'condition': flatL[1], 'trial': flatL[2], 'exclude_include': flatL[3], 'vel_start_avg': flatL[4], 'grasp_start_avg': flatL[5]}

dFrame = pd.DataFrame(frame)
dFrame.to_csv(r'C:/Users/angie/Box/Project/2.Stereo-motor relationship/data/trial_inclusion_exclusion_list.csv', index=False)

vel_data