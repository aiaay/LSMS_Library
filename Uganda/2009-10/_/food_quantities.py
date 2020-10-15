#!/usr/bin/env python

import sys
sys.path.append('../../_')
from uganda import food_quantities

myvars = dict(fn='Uganda/2009-10/Data/GSEC15b.dta',item='h15bq2',HHID='hh',
              purchased='h15bq4',
              away='h15bq6',
              produced='h15bq8',
              given='h15bq10',units='untcd')

q = food_quantities(**myvars)

q.to_parquet('food_quantities.parquet')

