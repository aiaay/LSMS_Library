#!/usr/bin/env python

import sys
sys.path.append('../../_/')
import pandas as pd
import numpy as np
import dvc.api
from lsms import from_dta
import sys
sys.path.append('../../_/')
from tanzania import other_features

round_match = {1:'2008-09', 2:'2010-11', 3:'2012-13', 4:'2014-15'}

myvars = dict(fn='../Data/upd4_hh_a.dta',
              HHID='r_hhid',
              urban='urb_rur',
              region='domain',
              wave = 'round',
              urban_converter = lambda x: True if x=='URBAN' else False)

df = other_features(**myvars)

df['Rural'] = 1 - df.urban.astype(int)

df = df.rename(columns={'region':'m','wave':'t'})

df = df.replace({'t':round_match})

df = df.reset_index().set_index(['j','t','m'])
df = df[['Rural']]

regions = set(df.index.get_level_values('m'))
df = df.rename(index={k:k.title() for k in regions})

df.to_parquet('other_features.parquet')
