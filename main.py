from define import *
import pandas as pd

import csvdata as csvdt
import metadata as meta
import preprocess as prep
import analyze as an

data = csvdt.read_data(DATA_FILE_PATH)
df = pd.DataFrame(data)

meta.get_info_abt_eventname(df)
meta.get_info_abt_sc_null(df)

prep.preprocess(df)

an.screenview()