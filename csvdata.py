from define import *
import os
import pandas as pd

def read_data(read_file_path):
  try:
    data = pd.read_csv(read_file_path, keep_default_na=False, na_values="-")
  except:
    print(f"*** ERROR: cannot open file {read_file_path}")
    exit(1)
  return data

def write_data(df, write_dir_path, write_file_name, header=True, index=False, na_rep="."):
  if not os.path.exists(write_dir_path):
    os.mkdir(write_dir_path)
  df.to_csv(f"{write_dir_path}/{write_file_name}", header=header, index=index, na_rep=na_rep, sep=",", encoding="utf8")

def slice_dataframe(df, direction=ROW, start=None, end=None, options=None):
  try:
    if direction == ROW:
      newdf = df.iloc[start:end, :]
    if direction == COL:
      newdf = df.loc[:,options]
  except:
    print(f"*** ERROR: cannot slice dataframe ... direction={direction}, start={start}, end={end}, options={options}")
    exit(1)
  return newdf