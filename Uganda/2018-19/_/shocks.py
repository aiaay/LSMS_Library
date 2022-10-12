#!/usr/bin/env python

from calendar import month
import sys
sys.path.append('../../_/')
import pandas as pd
import dvc.api
from datetime import datetime

#test opening using read()
modelpkl = dvc.api.read(
    'GSEC16.dta.dvc',
    repo='../Data/',
    mode='rb'
)

#shock dataset
with dvc.api.open('../Data/GSEC16.dta.dvc',mode='rb') as dta:
         df = pd.read_stata(dta)
df = df[df['s16q02y'].notna()] #filter for valid entry 



#general hh dataset 
with dvc.api.open('../Data/GSEC1.dta.dvc',mode='rb') as dta:
         date = pd.read_stata(dta)
#filter for hhs who have taken the shock questionnaire 
date = date[date.set_index('hhid').index.isin(df.set_index('hhid').index)]


#calculate shock onset 
df['s16q02a'] = pd.to_datetime(df.s16q02a, format='%B').dt.month
df['start_date'] = pd.to_datetime(df.rename(columns={'s16q02y': 'year', 's16q02a': 'month'})[['year', 'month']].assign(DAY=1))
date['end_date'] = pd.to_datetime(date[['year', 'month']].assign(DAY=1))
date = date[["hhid", "end_date"]]
df = pd.merge(df, date, on='hhid')
df['Onset'] = (df.end_date.dt.to_period('M') - df.start_date.dt.to_period('M')).apply(lambda x: x.n)


shocks = pd.DataFrame({"i": df.hhid.values.tolist(),
                    "Shock":df.s16qa01.values.tolist(), 
                    "Onset":df.Onset.values.tolist(), 
                    "Duration":df.s16q02b.values.tolist(),
                    "EffectedIncome":df.s10q03a.values.tolist(), 
                    "EffectedAssets":df.s16q03b.values.tolist(), 
                    "EffectedProduction":df.s16q03c.values.tolist(), 
                    "EffectedConsumption":df.s16q03d.values.tolist(), 
                    "HowCoped0":df.s16q04a.values.tolist(),
                    "HowCoped1":df.s16q04b.values.tolist(),
                    "HowCoped2":df.s16q04c.values.tolist()})

shocks.insert(1, 't', '2018-19')
shocks.set_index(['i','t','Shock'])

shocks.to_parquet('shocks.parquet')
