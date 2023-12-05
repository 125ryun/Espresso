import os
import pandas as pd

def read_data(read_file_path):
  try:
    data = pd.read_csv(read_file_path, keep_default_na=False, na_values='-', usecols=USECOLS)
  except:
    print(f"*** ERROR: cannot open file {read_file_path}")
    exit(1)
  return data

def make_dataframe_with(data, options=[]):
  df = pd.DataFrame(data)
  if len(options)>0:
    df = df[options]
  return df

def sort_dataframe_by(df, options, reset_index=1):
  df = df.sort_values(by=options)
  if reset_index:
    df.reset_index(drop=True, inplace=True)
  return df

def write_data(df, write_dir_path, write_file_name, na_rep=".", header=True, index=False):
  if not os.path.exists(write_dir_path):
    os.mkdir(write_dir_path)
  df.to_csv(f"{write_dir_path}/{write_file_name}", na_rep=na_rep, header=header, index=index, sep=",", encoding="utf8")