#!/usr/bin/env python
import sys
sys.path.append('../../_')
from uganda import food_expenditures

myvars = dict(fn='../Data/gsec15b.dta',item='itmds',HHID='HHID',
              purchased='h15bq5',
              away='h15bq7',
              produced='h15bq9',
              given='h15bq11')

x = food_expenditures(**myvars)

x.to_parquet('food_expenditures.parquet')

