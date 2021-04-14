import pandas as pd
import os
import matplotlib.pyplot as plt

myPath = r'C:/Users/angie/Git Root/stereo-prehension/data/'
fig_dir = r'C:/Users/angie/Git Root/stereo-prehension/figs/grasping_traces/'

os.chdir(myPath)

data = pd.read_csv('graspingData.csv')

subjects = data.subject.unique()
conditions = data.condition.unique()
trials = data.trial.unique()

# Make figure

def makeFig(sub, cond, t):
    plt.plot(data.time_stamp[(data.subject == sub) & (data.condition == cond) & (data.trial == t)], data.position[(data.subject == sub) & (data.condition == cond) & (data.trial == t)])

    plt.title(sub + ' ' + cond + ' ' + str(t))
    plt.xlabel('Time (secs)')
    plt.ylabel('Grip Aperture (mm)')

    fig_name = 'grasping_' + sub + '_' + cond + '_' + str(t) + '.png'

    plt.savefig(fname=fig_dir + fig_name, bbox_inchces='tight', format='png', dpi=300)
    plt.clf()

for sub in subjects:
    for cond in conditions:
        for t in trials:

            makeFig(sub, cond, t)