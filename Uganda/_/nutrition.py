"""
Create a nutrition DataFrame for households based on food consumption quantities
"""

import pandas as pd
import numpy as np
from fct_addition import nutrient_df, harmonize_nutrient

apikey = "hAkb5LsLAS1capOD60K6ILrZDkC29eK6ZmqCumXB"
fct_add = pd.read_csv('fct_addition.csv').drop("Unnamed: 0", axis = 1)
fct = pd.read_csv('fct.csv').set_index('i')
q = pd.read_parquet('../var/food_quantities.parquet')

#create and restructure fct for fdc food items; 
n1 = nutrient_df(fct_add, apikey)
n1 = harmonize_nutrient(n1)

#combine two fcts 
final_fct = pd.concat([fct, n1]).sort_index().T

#sum all quantities 
q['q_sum'] = q.sum(axis=1)
q = q[['q_sum']].droplevel('units').reset_index()
final_q = q.pivot_table(index = ['j','t','m'], columns = 'i', values = 'q_sum')

#cross-filter two dfs to align matrices; replace NaN values with 0 
list1 = final_q.columns.values.tolist()
list2 = final_fct.columns.values.tolist()

final_q = final_q.filter(items=list2).replace(np.nan,0)
final_fct = final_fct.filter(items=list1).replace(np.nan,0)

n = final_q@final_fct.T
n.to_parquet('../var/nutrition.parquet')