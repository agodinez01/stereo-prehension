import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.stats import kstest
import seaborn as sns

myPath = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/Data/'
os.chdir(myPath)

fig_dir = r'C:/Users/angie/Box/Projects/2.Stereo-motor relationship/figs/'
fig_name = 'normality_distribution.png'

data = pd.read_csv('abs_bw_velocity.csv')

fig, axs = plt.subplots(2, 1, sharex=True, sharey=True)

sns.histplot(ax=axs[0], x=data.vel_bw[data.group == 'stereo-normal'])
axs[0].set_title('Stereo-normal distribution')

sns.histplot(ax=axs[1], x=data.vel_bw[data.group == 'stereo-anomalous'])
axs[1].set_title('Stereo-anomalous distribution')
axs[1].set_xlabel('velocity')

#plt.show()
plt.savefig(fname= fig_dir + fig_name, bbox_inches='tight', format='png', dpi=300)
plt.clf()
plt.close('all')

total_data = data.vel_bw.count()
nans = data['vel_diff'].isnull().sum()

# Test for normality of data for each group

statistic_norm, pvalue_norm = kstest(data.vel_filled[data.group == 'stereo-normal'], 'norm')
statistic_anom, pvalue_anom = kstest(data.vel_filled[data.group == 'stereo-anomalous'], 'norm')

data