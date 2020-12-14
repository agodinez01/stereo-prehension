
import os
from os import listdir
from os.path import isfile, join
import csv
import pandas as pd
import seaborn as sns
from pathlib import Path

data_dir = "C:/Users/angie/Box/StereoMotorStudy/StereoMotor MATLAB/analysis/csv"
os.chdir(data_dir)

a = [x[0] for x in os.walk(data_dir)]
subject_list = [item[-2:] for item in a[1:]]
condition = ['b', 'D', 'N']

def get_csv_file():
    data = []
    for sub in subject_list:
        subject_directory = data_dir + '/' + sub
        os.chdir(subject_directory)


        sub_file_list = [f for f in listdir(subject_directory) if isfile(join(subject_directory, f))]

        for file in sub_file_list:
            df = pd.read_csv(subject_directory + '/' + file)
            df.columns = ['grasping_finger_x', 'grasping_finger_y', 'grasping_finger_z', 'thumb_x', 'thumb_y', 'thumb_z', 'wrist_x', 'wrist_y', 'wrist_z']
            df['subject'] = sub
            df['condition'] = file[3]

            if len(file) == 10:
                df['trial'] = file[5]
            elif len(file) == 11:
                df['trial'] = file[5:7]

            data.append(df)

    return data

data = get_csv_file()
all_data = pd.concat(data, sort=True)
all_data = pd.DataFrame(all_data, columns=['subject', 'condition', 'trial', 'grasping_finger_x', 'grasping_finger_y', 'grasping_finger_z', 'thumb_x', 'thumb_y', 'thumb_z', 'wrist_x', 'wrist_y', 'wrist_z'])

all_data.to_csv(r'C:\Users\angie\Git Root\stereo-prehension\data\reachingData.csv', index=False)
