"""
determine the most popular companies to hand categorize
this will seed the classification algorithm
"""
import sys
sys.path.append("..")

import catagorise_transactions as ct
import pandas as pd
import get_config
import database as db

dirs = get_config.cfg['dirs']

num_merchants = 100 # adjust this if you want a larger seed

fileout = dirs['runDir'] + 'model_data\lookup_table.csv'

data = db.getTransactionData()
df = pd.DataFrame(data)
print(df)
# NOTE: Dont think all this bit is needed
#fileCities = dirs.data_dir + 'cities_by_state.pickle' # TODO hardcode
#us_cities = pd.read_pickle(fileCities)

# TODO: set up parsing function to parse out the merchants for this
ct.parse_transactions(df,'description')

counts = df.merchant.value_counts().head(num_merchants)
counts = counts.to_frame('count')
counts['merchant'] = counts.index
counts['category'] = None

counts.to_csv(fileout,index=False)
