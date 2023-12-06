from define import *
import os
import pandas as pd
import csvdata as csvdt

def screenview():
    final = []
    
    for sliced_file_name in os.listdir(SLICED_DIR_PATH):
        stat = []
        
        data = csvdt.read_data(os.path.join(SLICED_DIR_PATH, sliced_file_name))
        df = pd.DataFrame(data)
        
        id = df.iloc[0][ID]
        
        scview_df = df[df[EVENTNAME]=="screen_view"]
        csvdt.write_data(scview_df, CLEAN_DIR_PATH, f"scview_{id}.csv")
        
        df_len = scview_df.shape[0]
        
        sessions = []
        session = []
        # sc_w_usetime = []
        first_row = 1
        for i, row in enumerate(scview_df.iloc):
            curr_sc = row[CURR_SC]
            usetime = row[USETIME]
            
            # sc_w_usetime = []
            # sc_w_usetime.append(curr_sc)
            # sc_w_usetime.append(usetime)
            
            if first_row:
                first_row = 0
                null = row[PREV_SC]
                prev_sc = row[PREV_SC]
                # session.append([prev_sc, 0])
                session.append(prev_sc)
                # session.append(sc_w_usetime)
                session.append(curr_sc)
                prev_sc = curr_sc
                continue
            
            if row[PREV_SC] == null or row[PREV_SC] != prev_sc:
                # append session to sessions list
                sessions.append(session)
                # initialize session
                session = ["null",]
                # session = [[row[PREV_SC],0],]
                # session.append(sc_w_usetime)
                session.append(curr_sc)
                prev_sc = curr_sc
                continue
                
            if row[PREV_SC] == prev_sc:
                # session.append(sc_w_usetime)
                session.append(curr_sc)
                prev_sc = curr_sc
            else:
                print("**** error: ", id, i)
        
            if i == df_len-1:
                session.append("null")
                # session.append(["null", 0])
                sessions.append(session)            
            
        ss_df = pd.DataFrame(sessions)
        
        ss_df_transpose = ss_df.transpose()
        df_colwise = []
        for i in range(ss_df_transpose.shape[1]):
            df_colwise.append(ss_df_transpose.iloc[:,i])
        ss_df_onecol = pd.concat(df_colwise)
        # print(ss_df_onecol)
        print(id, "\n", ss_df_onecol.value_counts())
        continue
        
        tmp = ss_df.value_counts()
        print(id)
        print(ss_df.nunique())
        
        # for _ in tmp:
        #     print(_)
        
        # exit(1)
        
        # ss_df_len = ss_df.shape[0] * ss_df.shape[1]
        # ss_df_reshape = ss_df.shape(ss_df_len, ss_df.shape[2])
        # collist = ["screenview", "usetime"]
        # final_df = pd.DataFrame(ss_df_reshape, columns=collist)
        # session_num_list = []
        # for i in range(1, ss_df.shape[0]+1):
        #     session_num_list.extend([i]*ss_df.shape[1])
        # ss_df.insert(0, "#session", session_num_list)
        # csvdt.write_data(final_df, SESSIONS_DIR_PATH, f"3d_sessions_{id}.csv")
        
        csvdt.write_data(ss_df, SESSIONS_DIR_PATH, f"sessions_{id}.csv")
        
        