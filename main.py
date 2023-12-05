from define import *
import os
import pandas as pd
import csvdata as csvdt
import preprocess as pre

data = csvdt.read_data(DATA_FILE_PATH)
df = pd.DataFrame(data)

pre.preprocess(df)

exit(1)


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
df.reset_index(drop=True, inplace=True)