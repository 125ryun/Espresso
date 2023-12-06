from define import *
import sys

class event_class_stat:
  def __init__(self):
    self.prev = {}
    self.curr = {}
  def add(self, option, sc):
    if option == 'p':
      self.prev[sc] = self.prev.get(sc, 0) + 1
    if option == 'c':
      self.curr[sc] = self.curr.get(sc, 0) + 1

def get_info_abt_eventname(df):
  eventnames = df[EVENTNAME].unique()

  stats = {}
  for i in range(df.shape[0]):
    eventname = df.iloc[i][EVENTNAME]
    prev_sc = df.iloc[i][PREV_SC]
    curr_sc = df.iloc[i][CURR_SC]
    
    stat = stats.get(eventname, event_class_stat())
    stat.add('p', prev_sc)
    stat.add('c', curr_sc)
    stats[eventname] = stat

  sys.stdout = open("watch_eventnames.txt", "w")

  for eventname in eventnames:
    print(eventname)
  print("\n")
  
  for key, value in stats.items():
    print("------------------------")
    print(key)
    print("--- prev ---------------")
    for k, v in value.prev.items():
      print(f"{k} : {v}")
    print("--- curr ---------------")
    for k, v in value.curr.items():
      print(f"{k} : {v}")
    print("------------------------\n")

  sys.stdout.close()