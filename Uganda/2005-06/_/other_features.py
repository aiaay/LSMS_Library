#!/usr/bin/env python

import sys
sys.path.append('../../_/')
import pandas as pd
import numpy as np
from uganda import other_features

myvars = dict(fn='Uganda/2005-06/Data/GSEC1.dta',
              HHID='HHID',
              urban='urban',
              region='region')

df = other_features(**myvars)

# Some "Central" households have region coded as 0?  These seem to be households in one of the 34
# Enumeration Areas (comm) of Kampala.
# See https://microdata.worldbank.org/index.php/catalog/1001/data-dictionary/F41?file_name=2005_GSEC1
df = df.replace({'region':{'0':'Kampala'})

df.to_parquet('other_features.parquet')