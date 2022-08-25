#!/usr/bin/env python

import sys
sys.path.append('../../_')
from uganda import food_quantities

# See https://microdata.worldbank.org/index.php/catalog/3795/data-dictionary/F93?file_name=GSEC15B.dta
# Note that notations on Q don't seem to match!

myvars = dict(fn='../Data/GSEC15B.dta',item='CEB01',HHID='hhid',
              purchased='CEB06',
              away='CEB08',
              produced='CEB10',
              given='CEB012',
              units='CEB03C')

q = food_quantities(**myvars)

columns = [x for x in q.columns if type(x)==str]

q[columns].to_parquet('food_quantities.parquet')
