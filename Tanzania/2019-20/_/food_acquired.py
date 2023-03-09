#!/usr/bin/env python
import sys
sys.path.append('../../_/')
from tanzania import food_acquired
import numpy as np

fn='../Data/HH_SEC_J1.dta'

myvars = dict(item='itemcode',
              HHID='sdd_hhid',
              #year ='round',
              quant_ttl_consume='hh_j02_2',
              unit_ttl_consume = 'hh_j02_1',
              quant_purchase = 'hh_j03_2',
              unit_purchase = 'hh_j03_1',
              value_purchase = 'hh_j04',
              #place_purchase = 'hj_05', 
              quant_own = 'hh_j05_2',
              unit_own = 'hh_j05_1', 
              quant_inkind = 'hh_j06_2', 
              unit_inkind = 'hh_j06_1'
              )

d = food_acquired(fn,myvars)
d['t'] = '2019-20'
df = d.reset_index().set_index(['j','t','i'])

pair = {'quant': ['quant_ttl_consume', 'quant_purchase', 'quant_own', 'quant_inkind'] ,
        'unit': ['unit_ttl_consume', 'unit_purchase', 'unit_own', 'unit_inkind']}

unit_conversion = {'Kg': 1,
                   'Gram': 0.001,
                   'Litre': 1,
                   'Millilitre': 0.001,
                   'Piece': 'p'}

df = df.fillna(0).replace(unit_conversion).replace('NONE', 0)
pattern = r"[p+]"
for i in range(4):
    df[pair['quant'][i]] = df[pair['quant'][i]].astype(np.int64) * df[pair['unit'][i]]
    df[pair['quant'][i]].replace('', 0, inplace=True)
    if df[pair['quant'][i]].dtype != 'O':
        df[pair['unit'][i]] = 'kg'
    else: 
        df[pair['unit'][i]] = np.where(df[pair['quant'][i]].str.contains(pattern).to_frame() == True, 'piece', 'kg')
        df[pair['quant'][i]] = df[pair['quant'][i]].apply(lambda x: x if str(x).count('p') == 0 else str(x).count('p'))

df['agg_u'] = df[pair['unit']].apply(lambda x: max(x) if min(x) == max(x) else min(x) + '+' + max(x), axis = 1)

df['unitvalue_purchase'] = df['value_purchase']/df['quant_purchase']
df.replace([np.inf, -np.inf, 0], np.nan, inplace=True)

df.to_parquet('food_acquired.parquet')
