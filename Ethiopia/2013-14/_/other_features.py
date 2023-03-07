#!/usr/bin/env python

import sys
sys.path.append('../../_/')
import pandas as pd
import numpy as np
from ethiopia import other_features
from pathlib import Path

pwd = Path.cwd()
round = str(pwd.parent).split('/')[-1]


myvars = dict(fn='../Data/sect_cover_hh_w2.dta',
              HHID='household_id',
              urban='rural',
              region='saq01',
              urban_converter = lambda x: x.lower() != 'rural')

df = other_features(**myvars)

df['Rural'] = 1 - df.urban.astype(int)

df = df.rename(columns={'region':'m'})

df['t'] = round

df = df.reset_index().set_index(['j','t','m'])[['Rural']]

df.to_parquet('other_features.parquet')
