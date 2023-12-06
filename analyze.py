from define import *
import os
import pandas as pd
import csvdata as csvdt

def screenview():
    for sliced_file_name in os.listdir(SLICED_DIR_PATH):
        data = csvdt.read_data(os.path.join(SLICED_DIR_PATH, sliced_file_name))
        df = pd.DataFrame(data)
        
        id = df.iloc[0][ID]
        
        scview_df = df[df[EVENTNAME]=="screen_view"]
        csvdt.write_data(scview_df, CLEAN_DIR_PATH, f"scview_{id}.csv")
        
        df_len = scview_df.shape[0]
        
        sessions = []
        session = []
        first_row = 1
        for i, row in enumerate(scview_df.iloc):
            curr_sc = row[CURR_SC]
            usetime = row[USETIME]
            
            sc_w_usetime = [curr_sc, usetime]
            
            if first_row:
                first_row = 0
                null = row[PREV_SC]
                prev_sc = row[PREV_SC]
                session.append([prev_sc, 0])
                #session.append(prev_sc)
                session.append(sc_w_usetime)
                #session.append(curr_sc)
                prev_sc = curr_sc
                continue
            
            if row[PREV_SC] == null or row[PREV_SC] != prev_sc:
                # append session to sessions list
                sessions.append(session)
                # initialize session
                #session = ["null",]
                session = [[row[PREV_SC],0],]
                session.append(sc_w_usetime)
                #session.append(curr_sc)
                prev_sc = curr_sc
                continue
                
            if row[PREV_SC] == prev_sc:
                session.append(sc_w_usetime)
                #session.append(curr_sc)
                prev_sc = curr_sc
            else:
                print("**** error: ", id, i)
        
            if i == df_len-1:
                #session.append("null")
                session.append(["null", 0])
                sessions.append(session)
            
        ss_df = pd.DataFrame(sessions)
        csvdt.write_data(ss_df, SESSIONS_DIR_PATH, f"sessions_{id}.csv")