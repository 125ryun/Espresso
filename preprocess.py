import pandas as pd
import csvdata as csvdt

DATA_FILE_PATH = "./data/dw_user_events.csv"
OUT_DIR_PATH = "./out/sliced"

USECOLS = [ID, EVENTNAME, PREV_SC, CURR_SC, USETIME, TIMESTAMP]

def insert_formatted_timestamp(df):
  df[FORMATTED_TIMESTAMP] = df[TIMESTAMP] / 1000
  df[FORMATTED_TIMESTAMP] = pd.to_datetime(df[FORMATTED_TIMESTAMP], unit="ms")
  return df

def slice_userwise(data_path):
  data = csvdt.read_data(data_path)
  df = csvdt.make_dataframe_with(data, USECOLS)
  df = csvdt.sort_dataframe_by(df, [ID, TIMESTAMP])


last_idx = 0
for i in range(df.shape[0]):
  if i==0: continue
  if df.iloc[i][ID] != df.iloc[i-1][ID] or i==df.shape[0]-1:
    sliced_df = df.truncate(before=last_idx, after=i-1, axis=0, copy=False)
    sliced_df.to_csv(f"{OUT_DIR_PATH}/out_{df.iloc[i-1][ID]}.csv", sep=",", na_rep=".", header=True,index=False, encoding="utf8")
    last_idx = i