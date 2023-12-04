import os
import csv

DATA_DIR_PATH = "./data"
OUT_DIR_PATH = "./out"

DATA_FILE_PATH = "./data/dw_user_events.csv"
USEFUL_COLNAMES = ["auth_id", "user_pseudo_id", "event_name", "event_timestamp_w_timezone", "screen_class", "previous_screen_class", "use_time_msec"]
    
try:
    f_r = open(DATA_FILE_PATH, "r", encoding="utf8")    
except:
    print(f"**** ERROR: cannot open file {DATA_FILE_PATH}")
    exit(1)
rdr = csv.reader(f_r)

if not os.path.exists(OUT_DIR_PATH):
    os.mkdir(OUT_DIR_PATH)
try:
    f_tmp = open(OUT_DIR_PATH + "tmp.csv", "w", encoding="utf8")
except:
    print(f"**** ERROR: cannot open file {OUT_DIR_PATH}/tmp.csv")
    exit(1)    
wtr = csv.writer(f_tmp)

colnames = []
for i, row in enumerate(rdr):
    if i==0: # header row
        for j, colname in enumerate(row):
            colnames.append(colname)

f_r.close()
f_tmp.close()

# for filename in os.listdir(DATA_DIR_PATH):
#     print(filename)
#     f = open(DATA_DIR_PATH+"/"+filename, "r", encoding="utf8")
#     rdr = csv.reader(f)
        
#     for row in rdr:
#         print(row)

#         arr = []
#         for j, colname in enumerate(row):
#             arr.append([j, colname])
#         print(arr)
        
#         f.close()
#         break
    
#     print("\n")