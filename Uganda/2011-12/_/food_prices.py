#!/usr/bin/env python

import sys
sys.path.append('../../_')
from uganda import prices_and_units

myvars = dict(fn='Uganda/2011-12/Data/GSEC15B.dta',item='itmds',HHID='hh',market='h15bq12',farmgate='h15bq13',units='untcd')

prices = prices_and_units(**myvars)

prices.to_parquet('./food_prices.parquet')

