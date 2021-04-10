import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy import signal

myPath = r'C:/Users/angie/Git Root/stereo-prehension/data/'
fig_dir = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/figs/velocity_traces/'

os.chdir(myPath)

data = pd.read_csv('velocityData.csv')

subjects = data.subject.unique()
conditions = data.condition.unique()
trials = data.trial.unique()

def getList():
    list_of_trials = []

    for sub in subjects:
        for cond in conditions:
            for t in trials:

                name_of_trial = sub + '_' + cond + '_' + str(t)
                list_of_trials.append(name_of_trial)

    return list_of_trials

unique_trials = getList()
unique_list_of_trials = pd.DataFrame(unique_trials)

unique_list_of_trials.to_csv(r'C:/Users/angie/Git Root/stereo-prehension/data/Trial_list.csv', index=False)