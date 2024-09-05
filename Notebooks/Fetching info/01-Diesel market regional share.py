import os
import sys
import pandas as pd
import numpy as np
import time
import pyprint

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../../')))
from IntLCA import intLCA
from IntLCA.utils.fetcher import ActivityFilter


project = "Integrated LCA project"  # --> Change this to the name of the project
scenarios = ["SSP2-Base", "SSP2-PkBudg1150", "SSP2-PkBudg500"]
years = [2020, 2025, 2030, 2035, 2040, 2045, 2050]
base_path = "PATH_TO_DIRECTORY"
 #--> Change this to the path where the data is stored
int_lca = intLCA.IntLCA(project, scenarios, years, base_path)
paths = int_lca.access_data()

#find activities -- user specific
diesel_market_keys = [
        {"includes_all": "market for diesel, low-sulfur", "location": "World"}
]
diesel_market_regional_keys = [
        {"includes_all": "market for diesel, low-sulfur", "excluding_locations": "World"}
]

start = time.time()
storing_df =[]
for path in pyprind.prog_percent(paths):
    A, B, A_inds, B_inds, A_inds_rev, B_inds_rev = int_lca.create_matrices(path)
    diesel_market_world, diesel_market_regional = int_lca.filtering(A_inds, diesel_market_keys, diesel_market_regional_keys)


    fetch_fractions_diesel= []
    for idx in diesel_market_regional:
        diesel_countries= A_inds_rev[idx]
        if any(A[idx, diesel_market_world] != 0):
            fraction_dict_diesel = {
                (diesel_countries[0], diesel_countries[4], diesel_countries[5], diesel_countries[3]): A[idx, diesel_market_world].todense() * 100
            }
            fetch_fractions_diesel.append(fraction_dict_diesel)
    
    #diesel_df
    rows_diesel = [(list(i.keys())[0][0], list(i.keys())[0][1], list(i.keys())[0][2]) for i in fetch_fractions_diesel]
    set_rows_diesel = set(rows_diesel)
    columns_diesel = [list(i.keys())[0][3] for i in fetch_fractions_diesel]
    set_columns_diesel = set(columns_diesel)

    df_DIESEL = pd.DataFrame(index = list(set_rows_diesel), columns = list(set_columns_diesel))
    for row in df_DIESEL.index:
        for column in df_DIESEL.columns:
            df_DIESEL.loc[[row], column] = [np.abs(i[(*row, column)].tolist()[0][0]) for i in fetch_fractions_diesel if
                                        list(i.keys())[0] == (*row, column)][0]


    dfs = [df_DIESEL]
    storing_df = storing_df + dfs
df_STORE = pd.concat(storing_df)

newindex1 = []
for i in df_STORE.index:
    if any(x in i[0:1][0].split(",")[0].split(" ")[2] for x in ["diesel"]):
        newindex1.append(i[0:1][0].split(",")[0].split(" ")[2])
    
newindex2 = []
for i in df_STORE.index:
    newindex2.append(i[1:2][0])

newindex3 = []
for i in df_STORE.index:
    newindex3.append(i[2:3][0])

df_STORE = df_STORE.reset_index()
df_STORE["market"] = newindex1
df_STORE["Pathway"] = newindex2
df_STORE["Year"] = newindex3
df_STORE = df_STORE.reset_index()
df_STORE = df_STORE.drop(columns=["index"])
df_STORE = df_STORE.drop(columns=["level_0"])

df_STORE.to_excel(r"./fuelmarket_region_breakdown.xlsx")



