import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy import signal

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
    condList = []
    trialList = []
    velExcludeList = []
    graspExcludeList = []

    for sub in subjects:
        for cond in conditions:
            for t in trials:

                velStartAvg = vel_data.vel_bw[0:4].mean()

                if velStartAvg > 0.5:
                    noGoodVelTrial = 'Exclude'
                else:
                    noGoodVelTrial = 'Keep'

                subL = [sub] * len()
                condL = [cond] * len()
                trialL = [t] * len()



            subVals.append()


