from define import *
import os
import pandas as pd

import csvdata as csvdt
import eventname as en
import preprocess as prep

data = csvdt.read_data(DATA_FILE_PATH)
df = pd.DataFrame(data)

en.get_info_abt_eventname(df)

exit(1)

prep.format(df)

# prep.preprocess()