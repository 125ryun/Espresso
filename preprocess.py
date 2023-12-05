from define import *
import pandas as pd
import csvdata as csvdt

OUT_DIR_PATH = "./out/sliced"
USECOLS = [ID, EVENTNAME, PREV_SC, CURR_SC, USETIME, TIMESTAMP]

def preprocess(df):
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
      csvdt.write_data(sliced_df, OUT_DIR_PATH, f"out_{df.iloc[i-1][ID]}.csv")
      prev_first_idx = i