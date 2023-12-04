import os
import csv
import pandas as pd

DATA_FILE_PATH = "./data/dw_user_events.csv"
TMP_FILE_PATH = "./out/tmp.csv"
OUT_FILE_PATH = "./out/out.csv"

ID = "auth_id"
EVENTNAME = "event_name"
PREV_SC = "previous_screen_class"
CURR_SC = "screen_class"
FORMATTED_TIMESTAMP = "fomatted_event_timestamp_w_timezone"
TIMESTAMP = "event_timestamp_w_timezone"
USETIME = "use_time_msec"

USECOLS = [ID, EVENTNAME, PREV_SC, CURR_SC, TIMESTAMP, USETIME]
OUT_COL_ORDER = [ID, FORMATTED_TIMESTAMP, EVENTNAME, PREV_SC, CURR_SC, USETIME]

# read csv file
try:
    data = pd.read_csv(DATA_FILE_PATH, keep_default_na=False, na_values='-', usecols=USECOLS)
except:
    print(f"*** ERROR: cannot open file {DATA_FILE_PATH}")
    exit(1)
    
# make dataframe
df = pd.DataFrame(data)
df = df[USECOLS]
df = df.sort_values(by=[ID, TIMESTAMP])

df[TIMESTAMP] = df[TIMESTAMP] / 1000
col_idx_formatted_timestamp = USECOLS.index(TIMESTAMP)
col_name_formatted_timestamp = "fomatted_event_timestamp_w_timezone"
col_data_formatted_timestamp = pd.to_datetime(df[TIMESTAMP], unit="ms")
df.insert(col_idx_formatted_timestamp, col_name_formatted_timestamp, col_data_formatted_timestamp)

# write tmp csv file
# df.to_csv(TMP_FILE_PATH, sep=",", na_rep=".", header=True,index=False, encoding="utf8")
        
prev = 0
curr = 0
delete_row_idx = []
for i in range(df.shape[0]):
    if i==0:
        continue
    prev = df.iloc[i-1]
    curr = df.iloc[i]
    if prev[ID] == curr[ID]:
        if prev[EVENTNAME] == curr[EVENTNAME]:
            if prev[CURR_SC] == curr[CURR_SC]:
                if  prev[PREV_SC] == curr[PREV_SC]:
                    delete_row_idx.append(i-1)
                    #print("** delete index: ", i-1)
                    if prev[CURR_SC] == curr[PREV_SC]:
                        delete_row_idx.append(i)
                        #print("** delete index: ", i)
            if prev[TIMESTAMP] == curr[TIMESTAMP]:
                delete_row_idx.append(i)
                    #print("** same timestamp index: ", i)
                    #input("y/n")
    i += 1


df.drop(delete_row_idx, axis=0, inplace=True)
df = df[OUT_COL_ORDER]
df.reset_index(drop=True, inplace=True)

last_idx = 0
for i in range(df.shape[0]):
    if i==0: continue
    if df.iloc[i][ID] != df.iloc[i-1][ID] or i==df.shape[0]-1:
        sliced_df = df.truncate(before=last_idx, after=i-1, axis=0, copy=False)
        sliced_df.to_csv(f"./out/out_{df.iloc[i-1][ID]}.csv", sep=",", na_rep=".", header=True,index=False, encoding="utf8")
        last_idx = i        