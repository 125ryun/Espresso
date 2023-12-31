from define import *
import os
import pandas as pd
import csvdata as csvdt

def screenview():    
    stat_screenclass_type = []
    stat_screenclass_series_2 = []
    stat_screenclass_series_3 = []
    
    for filename in os.listdir(SLICED_DIR_PATH):
        data = csvdt.read_data(os.path.join(SLICED_DIR_PATH, filename))
        df = pd.DataFrame(data)
        
        id = df.iloc[0][ID]
        
        screen_view_df = df[df[EVENTNAME]=="screen_view"]
        csvdt.write_data(screen_view_df, CLEAN_DIR_PATH, f"screen_view_{id}.csv")
        
        screen_view_df_len = screen_view_df.shape[0]
        
        sessions = []
        session = []
        first_row = 1
        for i, row in enumerate(screen_view_df.iloc):
            curr_sc = row[CURR_SC]
            usetime = row[USETIME]
            
            if first_row:
                first_row = 0
                null = row[PREV_SC]
                prev_sc = row[PREV_SC]
                session.append(prev_sc)
                session.append(curr_sc)
                prev_sc = curr_sc
                continue
            
            if row[PREV_SC] == null or row[PREV_SC] != prev_sc:
                sessions.append(session)
                # initialize session
                session = ["null",]
                session.append(curr_sc)
                prev_sc = curr_sc
                continue
                
            if row[PREV_SC] == prev_sc:
                session.append(curr_sc)
                prev_sc = curr_sc
            else:
                print("**** error: ", id, i)
        
            if i == screen_view_df_len-1:
                session.append("null")
                sessions.append(session)            
            
        sessions_df = pd.DataFrame(sessions)
        csvdt.write_data(sessions_df, SESSIONS_DIR_PATH, f"sessions_{id}.csv")
        
        stat_screenclass_series_2_dict = {}
        stat_screenclass_series_3_dict = {}
        for i, session in enumerate(sessions):
            session_len = len(session)            
            for j, sc in enumerate(session):
                if j == session_len-1: break
                key = "-".join([session[j], session[j+1]])
                stat_screenclass_series_2_dict[key] = stat_screenclass_series_2_dict.get(key, 0) + 1
                if j == session_len-2: break
                key = "-".join([session[j], session[j+1], session[j+2]])
                stat_screenclass_series_3_dict[key] = stat_screenclass_series_3_dict.get(key, 0) + 1
        
        sessions_df_transpose = sessions_df.transpose()
        session_df_colwise = []
        for i in range(sessions_df_transpose.shape[1]):
            session_df_colwise.append(sessions_df_transpose.iloc[:,i])
        sessions_df_reshape = pd.concat(session_df_colwise)
        
        sc_type_cnt = sessions_df_reshape.value_counts()
        sc_type_cnt_df = pd.DataFrame({id: sc_type_cnt}, index=sc_type_cnt.index.tolist())
        stat_screenclass_type.append(sc_type_cnt_df)
        
        sc_series_cnt = stat_screenclass_series_2_dict.values()
        sc_series_cnt_df = pd.DataFrame({id:sc_series_cnt}, index=stat_screenclass_series_2_dict.keys())
        stat_screenclass_series_2.append(sc_series_cnt_df)
        
        sc_series_cnt = stat_screenclass_series_3_dict.values()
        sc_series_cnt_df = pd.DataFrame({id:sc_series_cnt}, index=stat_screenclass_series_3_dict.keys())
        stat_screenclass_series_3.append(sc_series_cnt_df)
        
    stats_screenclass_type_df = pd.concat(stat_screenclass_type, axis=1)
    stats_screenclass_type_df = stats_screenclass_type_df.sort_index()
    csvdt.write_data(stats_screenclass_type_df, STATS_DIR_PATH, "count_screenclass_type.csv", index=True, na_rep=0)

    stats_screenclass_series_2_df = pd.concat(stat_screenclass_series_2, axis=1)
    stats_screenclass_series_2_df = stats_screenclass_series_2_df.sort_index()
    csvdt.write_data(stats_screenclass_series_2_df, STATS_DIR_PATH, "count_screenclass_series_2.csv", index=True, na_rep=0)
    
    stats_screenclass_series_3_df = pd.concat(stat_screenclass_series_3, axis=1)
    stats_screenclass_series_3_df = stats_screenclass_series_3_df.sort_index()
    csvdt.write_data(stats_screenclass_series_3_df, STATS_DIR_PATH, "count_screenclass_series_3.csv", index=True, na_rep=0)