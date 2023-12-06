from define import *
import os
import pandas as pd

import csvdata as csvdt
import eventname as en
import preprocess as prep
import analyze as an

data = csvdt.read_data(DATA_FILE_PATH)
df = pd.DataFrame(data)

en.get_info_abt_eventname(df)

'''
df = df[[EVENTNAME, PREV_SC, CURR_SC]]

prev_null_df = df[(df[EVENTNAME]=="screen_view")&(df[PREV_SC]=="null")]
print(prev_null_df[CURR_SC].unique())
csvdt.write_data(prev_null_df, "./", "appopen_prev_null.csv")

curr_null_df = df[(df[EVENTNAME]=="screen_view")&(df[CURR_SC]=="null")]
print(prev_null_df[PREV_SC].unique())
csvdt.write_data(curr_null_df, "./", "appopen_curr_null.csv")
'''

#exit(1)

prep.format(df)

an.screenview()

# prep.preprocess()