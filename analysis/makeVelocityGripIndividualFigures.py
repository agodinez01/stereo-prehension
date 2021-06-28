import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Makes grip and velocity figures for each subject and trial

myPath = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/data/'
fig_dir = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/figs/velocity_and_grasp/'

os.chdir(myPath)

vel_data = pd.read_csv('abs_bw_velocity.csv')
grasp_data = pd.read_csv('graspingData.csv')
kin_data = pd.read_csv('kinematic_data.csv')

subjects = vel_data.subject.unique()
conditions = vel_data.condition.unique()
trials = vel_data.trial.unique()

# Plot variables
colors = ['#cfcfcf', '#FF0000', '#000000', '#4b4b4b', '#8BC34A'] #light grey, red, black, dark grey, green

# Get a visual
def makeFig(sub, cond, t, vData, gData, kData):

    fig, axs = plt.subplots(2, 1, sharex=True)

    axs[0].set_title(sub + ' ' + cond + ' ' + str(t))
    axs[0].plot(vData['time'], vData['vel_filled'], color=colors[4])
    axs[0].plot(vData['time'], vData['vel_bw'], color=colors[2])
    axs[0].axvline(x=kData.pv_time.tolist(), color='red')

    axs[0].set_ylabel('Velocity (cm/s)')
    axs[0].set_ylim(vel_data['vel_filled'].min() - 10, vel_data['vel_filled'].max() + 10)

    axs[1].plot(gData['time_stamp'], gData['position'])
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Grip')
    axs[1].set_ylim(grasp_data['position'].min() - 10, grasp_data['position'].max() + 10)
    axs[1].axvline(x=kData.mga_time.tolist(), color='red')

    fig_name = sub + '_' + cond + '_' + str(t) + '.png'
    #plt.savefig(fname=fig_dir + fig_name, bbox_inches='tight', format='png', dpi=300)

    plt.show()
    plt.clf()
    plt.close('all')

for sub in subjects:
    for cond in conditions:
        for t in trials:

            vData = vel_data.loc[(vel_data.subject == sub) & (vel_data.condition == cond) & (vel_data.trial == t)]
            gData = grasp_data.loc[(grasp_data.subject == sub) & (grasp_data.condition == cond) & (grasp_data.trial == t)]
            kData = kin_data.loc[(kin_data.subject == sub) & (kin_data.condition == cond) & (kin_data.trial == t)]

            if len(vData) == 0:
                continue

            else:

                makeFig(sub, cond, t, vData, gData, kData)
