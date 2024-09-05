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
        {"includes_all": ["market for diesel, low-sulfur"], "excluding_locations": ["CO", "ZA", "CH", "BR", "PE", "IN", "Europe without Switzerland", "World", "RoW"]}
]
syn_diesel_keys = [
    {"includes_all": "diesel production, synthetic, from Fischer Tropsch process, hydrogen from coal gasification, energy allocation, at fuelling station"},
    {"includes_all": "diesel production, synthetic, from Fischer Tropsch process, hydrogen from coal gasification, with CCS, energy allocation, at fuelling station"},
    {"includes_all": "diesel production, synthetic, from Fischer Tropsch process, hydrogen from wood gasification, energy allocation, at fuelling station"},
    {"includes_all": "diesel production, synthetic, from Fischer Tropsch process, hydrogen from wood gasification, with CCS, energy allocation, at fuelling station"},
    {"includes_all": "diesel production, synthetic, from Fischer Tropsch process, hydrogen from electrolysis, energy allocation, at fuelling station"}
]

start = time.time()
storing_df =[]
for path in pyprind.prog_percent(paths):
    A, B, A_inds, B_inds, A_inds_rev, B_inds_rev = int_lca.create_matrices(path)
    diesel_market, diesel_syn_id = int_lca.filtering(A_inds, diesel_market_keys, syn_diesel_keys)

    fraction_syn1 = []
    for idx in diesel_market:
        syn_idx = A_inds_rev[idx]
        diesel_syn1_id = [int(j) for i, j in A_inds.items() if
                        "diesel production, synthetic, from Fischer Tropsch process, hydrogen from coal gasification, energy allocation, at fuelling station" in i[0]]
        syn_diesel_dict = {
            (syn_idx[0], syn_idx[4], syn_idx[5], syn_idx[3]): A[diesel_syn1_id, idx].sum()/A[diesel_syn_id,idx].sum() * 100
        }
        fraction_syn1.append(syn_diesel_dict)

    fraction_syn2 = []
    for idx in diesel_market:
        syn_idx = A_inds_rev[idx]
        diesel_syn2_id = [int(j) for i, j in A_inds.items() if
                        "diesel production, synthetic, from Fischer Tropsch process, hydrogen from coal gasification, with CCS, energy allocation, at fuelling station" in i[0]]
        syn_diesel_dict = {
            (syn_idx[0], syn_idx[4], syn_idx[5], syn_idx[3]): A[diesel_syn2_id, idx].sum()/A[diesel_syn_id,idx].sum() * 100
        }
        fraction_syn2.append(syn_diesel_dict)

    fraction_syn3 = []
    for idx in diesel_market:
        syn_idx = A_inds_rev[idx]
        diesel_syn3_id = [int(j) for i, j in A_inds.items() if
                        "diesel production, synthetic, from Fischer Tropsch process, hydrogen from wood gasification, energy allocation, at fuelling station" in i[0]]
        syn_diesel_dict = {
            (syn_idx[0], syn_idx[4], syn_idx[5], syn_idx[3]): A[diesel_syn3_id, idx].sum()/A[diesel_syn_id,idx].sum() * 100
        }
        fraction_syn3.append(syn_diesel_dict)

    fraction_syn4 = []
    for idx in diesel_market:
        syn_idx = A_inds_rev[idx]
        diesel_syn4_id = [int(j) for i, j in A_inds.items() if
                        "diesel production, synthetic, from Fischer Tropsch process, hydrogen from wood gasification, with CCS, energy allocation, at fuelling station" in i[0]]
        syn_diesel_dict = {
            (syn_idx[0], syn_idx[4], syn_idx[5], syn_idx[3]): A[diesel_syn4_id, idx].sum()/A[diesel_syn_id,idx].sum() * 100
        }
        fraction_syn4.append(syn_diesel_dict)

    fraction_syn5 = []
    for idx in diesel_market:
        syn_idx = A_inds_rev[idx]
        diesel_syn5_id = [int(j) for i, j in A_inds.items() if
                        "diesel production, synthetic, from Fischer Tropsch process, hydrogen from electrolysis, energy allocation, at fuelling station" in i[0]]
        syn_diesel_dict = {
            (syn_idx[0], syn_idx[4], syn_idx[5], syn_idx[3]): A[diesel_syn5_id, idx].sum()/A[diesel_syn_id,idx].sum() * 100
        }
        fraction_syn5.append(syn_diesel_dict)

    # default_df - Market
    rows_default_diesel = [(list(i.keys())[0][1], list(i.keys())[0][2]) for i in fraction_syn1]
    columns_default_diesel = [(list(i.keys())[0][0].split(" ")[0]) for i in fraction_syn1]
    set_columns_default_diesel= set(columns_default_diesel)
    df_default = pd.DataFrame(index=rows_default_diesel, columns=list(set_columns_default_diesel))

    for row in df_default.index:
        for column in df_default.columns:
            df_default.loc[[row], column] = [(list(i.keys())[0][0].split(",")[0].split(" ")[2]) for i in fraction_syn1]

    # default_df - Region
    rows_default1_diesel = [(list(i.keys())[0][1], list(i.keys())[0][2]) for i in fraction_syn1]
    columns_default1_diesel = ["Region"]
    df_default1 = pd.DataFrame(index=rows_default1_diesel, columns=columns_default1_diesel)

    for row in df_default1.index:
        for column in df_default1.columns:
            df_default1.loc[[row], column] = [(list(i.keys())[0][3].split(",")[0]) for i in fraction_syn1]

    #Column 1 - coal gasification wo CCS
    rows_diesel_syn = [(list(i.keys())[0][1], list(i.keys())[0][2]) for i in fraction_syn1]
    rows_diesel_syn1 = [(list(i.keys())[0][1], list(i.keys())[0][2], list(i.keys())[0][3]) for i in fraction_syn1]
    columns_diesel_syn = [list(i.keys())[0][0] for i in fraction_syn1]
    set_columns_diesel_syn = set(columns_diesel_syn)
    df_diesel_syn = pd.DataFrame(index=rows_diesel_syn, columns=list(columns_diesel_syn))
    df_diesel_syn1 = pd.DataFrame(index=rows_diesel_syn1, columns=list(set_columns_diesel_syn))

    for row in df_diesel_syn1.index:
        for column in df_diesel_syn.columns:
            df_diesel_syn1.loc[[row], [column]] = [np.abs(i[(column, *row)]) for i in fraction_syn1 if
                                                     list(i.keys())[0] == (column, *row)][0]

    newindex2 = []
    for i in df_diesel_syn1.index:
        newindex2.append(i[0:2])
    df_diesel_syn1 = df_diesel_syn1.reset_index()
    df_diesel_syn1["index_test"] = newindex2
    df_diesel_syn1 = df_diesel_syn1.set_index("index_test")
    df_diesel_syn1 = df_diesel_syn1.drop(columns=["index"])
    df_diesel_syn1.rename(columns={'market for diesel, low-sulfur': 'Coal gasification wo CCS'}, inplace=True)

    #Column 2 - coal gasification with CCS
    rows_diesel_syn = [(list(i.keys())[0][1], list(i.keys())[0][2]) for i in fraction_syn2]
    rows_diesel_syn2 = [(list(i.keys())[0][1], list(i.keys())[0][2], list(i.keys())[0][3]) for i in fraction_syn2]
    columns_diesel_syn = [list(i.keys())[0][0] for i in fraction_syn2]
    set_columns_diesel_syn = set(columns_diesel_syn)
    df_diesel_syn = pd.DataFrame(index=rows_diesel_syn, columns=list(columns_diesel_syn))
    df_diesel_syn2 = pd.DataFrame(index=rows_diesel_syn2, columns=list(set_columns_diesel_syn))

    for row in df_diesel_syn2.index:
        for column in df_diesel_syn.columns:
            df_diesel_syn2.loc[[row], [column]] = [np.abs(i[(column, *row)]) for i in fraction_syn2 if
                                                     list(i.keys())[0] == (column, *row)][0]

    newindex2 = []
    for i in df_diesel_syn2.index:
        newindex2.append(i[0:2])
    df_diesel_syn2 = df_diesel_syn2.reset_index()
    df_diesel_syn2["index_test"] = newindex2
    df_diesel_syn2 = df_diesel_syn2.set_index("index_test")
    df_diesel_syn2 = df_diesel_syn2.drop(columns=["index"])
    df_diesel_syn2.rename(columns={'market for diesel, low-sulfur': 'Coal gasification with CCS'}, inplace=True)


    #Column 3 - biomass gasification wo CCS
    rows_diesel_syn = [(list(i.keys())[0][1], list(i.keys())[0][2]) for i in fraction_syn3]
    rows_diesel_syn3 = [(list(i.keys())[0][1], list(i.keys())[0][2], list(i.keys())[0][3]) for i in fraction_syn3]
    columns_diesel_syn = [list(i.keys())[0][0] for i in fraction_syn3]
    set_columns_diesel_syn = set(columns_diesel_syn)
    df_diesel_syn = pd.DataFrame(index=rows_diesel_syn, columns=list(columns_diesel_syn))
    df_diesel_syn3 = pd.DataFrame(index=rows_diesel_syn3, columns=list(set_columns_diesel_syn))

    for row in df_diesel_syn3.index:
        for column in df_diesel_syn.columns:
            df_diesel_syn3.loc[[row], [column]] = [np.abs(i[(column, *row)]) for i in fraction_syn3 if
                                                     list(i.keys())[0] == (column, *row)][0]

    newindex2 = []
    for i in df_diesel_syn3.index:
        newindex2.append(i[0:2])
    df_diesel_syn3 = df_diesel_syn3.reset_index()
    df_diesel_syn3["index_test"] = newindex2
    df_diesel_syn3 = df_diesel_syn3.set_index("index_test")
    df_diesel_syn3 = df_diesel_syn3.drop(columns=["index"])
    df_diesel_syn3.rename(columns={'market for diesel, low-sulfur': 'Biomass gasification wo CCS'}, inplace=True)


    #Column 4 - biomass gasification with CCS
    rows_diesel_syn = [(list(i.keys())[0][1], list(i.keys())[0][2]) for i in fraction_syn4]
    rows_diesel_syn4 = [(list(i.keys())[0][1], list(i.keys())[0][2], list(i.keys())[0][3]) for i in fraction_syn4]
    columns_diesel_syn = [list(i.keys())[0][0] for i in fraction_syn4]
    set_columns_diesel_syn = set(columns_diesel_syn)
    df_diesel_syn = pd.DataFrame(index=rows_diesel_syn, columns=list(columns_diesel_syn))
    df_diesel_syn4 = pd.DataFrame(index=rows_diesel_syn4, columns=list(set_columns_diesel_syn))

    for row in df_diesel_syn4.index:
        for column in df_diesel_syn.columns:
            df_diesel_syn4.loc[[row], [column]] = [np.abs(i[(column, *row)]) for i in fraction_syn4 if
                                                     list(i.keys())[0] == (column, *row)][0]

    newindex2 = []
    for i in df_diesel_syn4.index:
        newindex2.append(i[0:2])
    df_diesel_syn4 = df_diesel_syn4.reset_index()
    df_diesel_syn4["index_test"] = newindex2
    df_diesel_syn4 = df_diesel_syn4.set_index("index_test")
    df_diesel_syn4 = df_diesel_syn4.drop(columns=["index"])
    df_diesel_syn4.rename(columns={'market for diesel, low-sulfur': 'Biomass gasification with CCS'}, inplace=True)

    #Column 5 - e-Diesel (CO2 + H2)
    rows_diesel_syn = [(list(i.keys())[0][1], list(i.keys())[0][2]) for i in fraction_syn5]
    rows_diesel_syn5 = [(list(i.keys())[0][1], list(i.keys())[0][2], list(i.keys())[0][3]) for i in fraction_syn5]
    columns_diesel_syn = [list(i.keys())[0][0] for i in fraction_syn5]
    set_columns_diesel_syn = set(columns_diesel_syn)
    df_diesel_syn = pd.DataFrame(index=rows_diesel_syn, columns=list(columns_diesel_syn))
    df_diesel_syn5 = pd.DataFrame(index=rows_diesel_syn5, columns=list(set_columns_diesel_syn))

    for row in df_diesel_syn5.index:
        for column in df_diesel_syn.columns:
            df_diesel_syn5.loc[[row], [column]] = [np.abs(i[(column, *row)]) for i in fraction_syn5 if
                                                     list(i.keys())[0] == (column, *row)][0]

    newindex2 = []
    for i in df_diesel_syn5.index:
        newindex2.append(i[0:2])
    df_diesel_syn5 = df_diesel_syn5.reset_index()
    df_diesel_syn5["index_test"] = newindex2
    df_diesel_syn5 = df_diesel_syn5.set_index("index_test")
    df_diesel_syn5 = df_diesel_syn5.drop(columns=["index"])
    df_diesel_syn5.rename(columns={'market for diesel, low-sulfur': 'e-Diesel'}, inplace=True)

    dfs_diesel = [df_default, df_default1, df_diesel_syn1, df_diesel_syn2, df_diesel_syn3, df_diesel_syn4, df_diesel_syn5]
    df_STORE_diesel = pd.concat(dfs_diesel, axis=1)

    set_rows_diesel_syn5 = set(rows_diesel_syn)
    df_World = pd.DataFrame(index=list(set_rows_diesel_syn5), columns=df_STORE_diesel.columns)
    df_World['market'] = "diesel"
    df_World['Region'] = "World"
    df_World['Coal gasification wo CCS'] = df_STORE_diesel["Coal gasification wo CCS"].mean()
    df_World['Coal gasification with CCS'] = df_STORE_diesel["Coal gasification with CCS"].mean()
    df_World['Biomass gasification wo CCS'] = df_STORE_diesel["Biomass gasification wo CCS"].mean()
    df_World['Biomass gasification with CCS'] = df_STORE_diesel["Biomass gasification with CCS"].mean()
    df_World['e-Diesel'] = df_STORE_diesel["e-Diesel"].mean()

    df_store = [df_STORE_diesel, df_World]
    df_diesel = pd.concat(df_store, axis=0)

    newindex1 = []
    for i in df_diesel.index:
        newindex1.append(i[0:1][0])
    newindex2 = []
    for i in df_diesel.index:
        newindex2.append(i[1:2][0])

    df_diesel = df_diesel.reset_index()
    df_diesel["Pathway"] = newindex1
    df_diesel["Year"] = newindex2
    df_diesel = df_diesel.reset_index()
    df_diesel = df_diesel.drop(columns=["index"])

    dfs = [df_diesel]
    storing_df = storing_df + dfs


df_STORE = pd.concat(storing_df)
df_STORE = df_STORE.reset_index()
df_STORE = df_STORE.drop(columns=["index"])
df_STORE = df_STORE.drop(columns=["level_0"])

print(print("Duration: {}".format(time.time() - start)))
df_STORE.to_excel(r"./Synthetic_diesel_breakdown_SSP2.xlsx")