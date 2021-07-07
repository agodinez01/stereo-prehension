import os
from os import listdir
from os.path import isfile, join
import pandas as pd

# Goes through every folder and creates a list of items in each folder. In this case, the items refer to individual trials.
# It then creates a pandas dataframe joining the data from all subjects and saves it to a csv file.

data_dir = "C:/Users/angie/Box/StereoMotorStudy/StereoMotor MATLAB/analysis/csv_new"
os.chdir(data_dir)

# Go through every folder in the path and create a list
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

            if len(df.columns) < 10:
                print(file)

            df.columns = ['grasping_finger_x', 'grasping_finger_y', 'grasping_finger_z', 'thumb_x', 'thumb_y', 'thumb_z', 'wrist_x', 'wrist_y', 'wrist_z', 'time_stamp']
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
all_data = pd.DataFrame(all_data, columns=['subject', 'condition', 'trial', 'time_stamp', 'grasping_finger_x', 'grasping_finger_y', 'grasping_finger_z', 'thumb_x', 'thumb_y', 'thumb_z', 'wrist_x', 'wrist_y', 'wrist_z'])

all_data.to_csv(r'C:\Users\angie\Box\Projects\2.Stereo-motor relationship\data\reachingData.csv', index=False)
