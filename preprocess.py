from define import *
import pandas as pd
import csvdata as csvdt

SLICED_DIR_PATH = "./out/sliced"
CLEAN_DIR_PATH = "./out/clean"

def format(df):
  USECOLS = [ID, EVENTNAME, PREV_SC, CURR_SC, USETIME, TIMESTAMP]

  # choose only useful columns
  df = df.loc[:, USECOLS]
  
  # sort by 1.ID, 2.TIMESTAMP
  df = df.sort_values(by=[ID, TIMESTAMP])
  df.reset_index(drop=True, inplace=True)

  # insert formatted_timestamp
  df[FORMATTED_TIMESTAMP] = df[TIMESTAMP] / 1000
  df[FORMATTED_TIMESTAMP] = pd.to_datetime(df[FORMATTED_TIMESTAMP], unit="ms")

  # slice userwise
  prev_first_idx = 0
  for i in range(df.shape[0]):
    if i==0: continue
    if df.iloc[i][ID] != df.iloc[i-1][ID] or i==df.shape[0]-1:
      sliced_df = df.iloc[prev_first_idx:i-1, :]
      csvdt.write_data(sliced_df, SLICED_DIR_PATH, f"sliced_{df.iloc[i-1][ID]}.csv")
      prev_first_idx = i

def preprocess(df):

  for filename in SLICED_DIR_PATH:
    data = csvdt.read_data(f"{SLICED_DIR_PATH}/{filename}")
    df = pd.DataFrame(data)

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

    csvdt.write_data(df, CLEAN_DIR_PATH, f"clean_{df.iloc[i-1][ID]}.csv")
