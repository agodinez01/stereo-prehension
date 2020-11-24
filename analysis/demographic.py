import os
import pandas as pd
import seaborn as sns
from datetime import date
from datetime import datetime

os.chdir("C:/Users/angie/Git Root/stereo-prehension/data")
data = pd.read_csv('demographic.csv')

subjects = data.id.unique()

def main(dob, dot):
    dob_date = datetime.strptime(dob, '%Y-%m-%d')
    test_date = datetime.strptime(dot, '%Y-%m-%d')

    years = (dob_date - test_date).days

    return years

def get_age():
    age = []

    for sub in subjects:

        d1 = data.dob[data.id == sub]
        d2 = data.dotest[data.id == sub]

        sub_age = main(d1, d2)
        #sub_age = main(data.dob[data.id == sub], data.dotest[data.id == sub])
        age.append(sub_age)

    return age

a = get_age()

data