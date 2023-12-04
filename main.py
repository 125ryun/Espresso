import os
import csv
import pandas as pd

DATA_FILE_PATH = "./data/dw_user_events.csv"
TMP_FILE_PATH = "./out/tmp.csv"

ID = "auth_id"
EVENTNAME = "event_name"
PREV_SC = "previous_screen_class"
CURR_SC = "screen_class"
TIMESTAMP = "event_timestamp_w_timezone"
USETIME = "use_time_msec"

USECOLS = [ID, EVENTNAME, PREV_SC, CURR_SC, TIMESTAMP, USETIME]

# read csv file
try:
    data = pd.read_csv(DATA_FILE_PATH, usecols=USECOLS)
except:
    print(f"*** ERROR: cannot open file {DATA_FILE_PATH}")
    exit(1)
    
# make dataframe
N = data.shape[0]
df = pd.DataFrame(data)
df = df[USECOLS]
df = df.sort_values(by=[ID, TIMESTAMP])

# df[TIMESTAMP] = df[TIMESTAMP] / 1000
# col_idx_formatted_timestamp = USECOLS.index(TIMESTAMP)
# col_name_formatted_timestamp = "fomatted_event_timestamp_w_timezone"
# col_data_formatted_timestamp = pd.to_datetime(df[TIMESTAMP], unit="ms")
# df.insert(col_idx_formatted_timestamp, col_name_formatted_timestamp, col_data_formatted_timestamp)

# write tmp csv file
df.to_csv(TMP_FILE_PATH, sep=",", na_rep=".", header=True,index=False, encoding="utf8")
# exit(1)

# class Node:
#     def __init__(self):
#         pass
    
#     def __init__(self, row):
#         self.id = row[]
    
#     def pass(self, new):
#         self.id = new.id
    
prev_ts = 0
prev_sc = ""
curr_ts = 0
curr_sc = ""
for i, row in enumerate(df.loc):
    if prev_ts == 0:
        prev_ts = row["event_timestamp_w_timezone"]
        prev_sc = row["screen_class"]
        continue
    curr_ts = row["event_timestamp_w_timezone"]
    curr_sc = row["screen_class"]
    if curr_ts == prev_ts:
        print("%%%% same timestamp at", i)
        print(prev_sc, curr_sc)
        input("y/n")
    prev_ts = curr_ts
    prev_sc = curr_sc
    