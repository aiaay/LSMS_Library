import sys
sys.path.append('../../_')
from uganda import prices_and_units

myvars = dict(fn='Uganda/2010-11/Data/GSEC15b.dta',item='itmds',HHID='hh',market='h15bq12',farmgate='h15bq13',units='untcd')

prices_and_units(**myvars)

