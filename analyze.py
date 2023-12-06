from define import *
import os
import pandas as pd
import csvdata as csvdt

def screenview():
    stat_screenclass_type = []
    stat_screenclass_series = []
    
    for filename in os.listdir(SLICED_DIR_PATH):
        data = csvdt.read_data(os.path.join(SLICED_DIR_PATH, filename))
        df = pd.DataFrame(data)
        
        id = df.iloc[0][ID]
        
        screen_view_df = df[df[EVENTNAME]=="screen_view"]
        csvdt.write_data(screen_view_df, CLEAN_DIR_PATH, f"screen_view_{id}.csv")
        
        screen_view_df_len = screen_view_df.shape[0]
        
        sessions = []
        session = []
        # sc_w_usetime = []
        first_row = 1
        for i, row in enumerate(screen_view_df.iloc):
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
        
            if i == screen_view_df_len-1:
                session.append("null")
                # session.append(["null", 0])
                sessions.append(session)            
            
        sessions_df = pd.DataFrame(sessions)
        csvdt.write_data(sessions_df, SESSIONS_DIR_PATH, f"sessions_{id}.csv")
        
        dict = {}
        for i, session in enumerate(sessions):
            session_len = len(session)            
            for j, sc in enumerate(session):
                if j == session_len-2:
                    break
                key = [session[i], session[i+1], session[i+2]]
                dict[key] = dict.get(key, 0) + 1
        print(dict.items)
        continue
            
        
        sessions_df_transpose = sessions_df.transpose()
        
        session_df_colwise = []
        for i in range(sessions_df_transpose.shape[1]):
            session_df_colwise.append(sessions_df_transpose.iloc[:,i])
        sessions_df_reshape = pd.concat(session_df_colwise)
        
        sc_type_cnt = sessions_df_reshape.value_counts()
        # print(id, "\n", val_cnt)
        # print(val_cnt.index.tolist())
        # print(val_cnt.tolist())
        
        # values = [_ for _ in zip(val_cnt.index.tolist(), val_cnt.tolist())]
        # values_df = pd.DataFrame(values)
        sc_type_cnt = pd.DataFrame({id: sc_type_cnt}, index=sc_type_cnt.index.tolist())
        stat_screenclass_type.append(sc_type_cnt)
        
        # # exit(1)
        
        # tmp = ss_df.value_counts()
        # print(id)
        # print(ss_df.nunique())
        
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
        
    stats_screenclass_type_df = pd.concat(stat_screenclass_type, axis=1)
    csvdt.write_data(stats_screenclass_type_df, STATS_DIR_PATH, "count_screenclass_type.csv", index=True)
    
    stats_screenclass_series_df = pd.concat(stat_screenclass_series, axis=1)
    csvdt.write_data(stats_screenclass_series_df, STATS_DIR_PATH, "count_screenclass_series.csv", index=True)