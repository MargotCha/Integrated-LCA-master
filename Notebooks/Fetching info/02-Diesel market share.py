import os
import sys
import pandas as pd
import pyprint

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../../')))
from IntLCA import intLCA
from IntLCA.utils.fetcher import ActivityFilter


project = "Integrated LCA project"  # --> Change this to the name of the project
scenarios = ["SSP2-Base", "SSP2-PkBudg1150", "SSP2-PkBudg500"]
years = [2020, 2025, 2030, 2035, 2040, 2045, 2050]
base_path = "PATH_TO_DIRECTORY" #--> Change this to the path where the data is stored
int_lca = intLCA.IntLCA(project, scenarios, years, base_path)
paths = int_lca.access_data()

#find activities -- user specific
diesel_market_keys = [
        {"includes_all": ["market for diesel, low-sulfur"], "excluding_locations": ["CO", "ZA", "CH", "BR", "PE", "IN", "Europe without Switzerland", "World", "RoW"]}
]
fossil_diesel_keys = [
        {"includes_all": "diesel production, petroleum refinery operation", "reference_product": "diesel"},
        {"includes_all": "diesel production, low-sulfur, petroleum refinery operation", "reference_product": "diesel, low-sulfur"},
        {"includes_all": "petroleum refinery operation","reference_product": "diesel"},
        {"includes_all": "pdiesel production, low-sulfur", "reference_product": "diesel, low-sulfur"}
]
bio_diesel_keys = [
        {"includes_all": "Biodiesel production, via transesterification, from rapeseed oil, energy allocation"},
        {"includes_all": "Biodiesel, from rapeseed oil, at fuelling station"},
        {"includes_all": "Biodiesel production, via transesterification, from palm oil, energy allocation"},
        {"includes_all": "Biodiesel, from palm oil, at fuelling station"}
]
syn_diesel_keys = [
    {"includes_all": "diesel production, synthetic, from Fischer Tropsch process, hydrogen from coal gasification, energy allocation, at fuelling station"},
    {"includes_all": "diesel production, synthetic, from Fischer Tropsch process, hydrogen from coal gasification, with CCS, energy allocation, at fuelling station"},
    {"includes_all": "diesel production, synthetic, from Fischer Tropsch process, hydrogen from wood gasification, energy allocation, at fuelling station"},
    {"includes_all": "diesel production, synthetic, from Fischer Tropsch process, hydrogen from wood gasification, with CCS, energy allocation, at fuelling station"},
    {"includes_all": "diesel production, synthetic, from Fischer Tropsch process, hydrogen from electrolysis, energy allocation, at fuelling station"}
]

storing_df =[]
for path in pyprind.prog_percent(paths):
    A, B, A_inds, B_inds, A_inds_rev, B_inds_rev = int_lca.create_matrices(path)
    diesel_market, diesel_fossil_id, diesel_bio_id, diesel_syn_id = int_lca.filtering(A_inds, diesel_market_keys, fossil_diesel_keys,
                                                                             bio_diesel_keys, syn_diesel_keys)

    fraction_fossil = []
    for idx in diesel_market:
        fossil_idx = A_inds_rev[idx]
        fossil_diesel_dict = {
            (fossil_idx[0], fossil_idx[4], fossil_idx[5], fossil_idx[3]): A[diesel_fossil_id, idx].sum() * 100
        }
        fraction_fossil.append(fossil_diesel_dict)

    fraction_bio = []
    for idx in diesel_market:
        bio_idx = A_inds_rev[idx]
        bio_diesel_dict = {
            (bio_idx[0], bio_idx[4], bio_idx[5], bio_idx[3]): A[diesel_bio_id, idx].sum() * 100
        }
        fraction_bio.append(bio_diesel_dict)

    fraction_syn = []
    for idx in diesel_market:
        syn_idx = A_inds_rev[idx]
        syn_diesel_dict = {
            (syn_idx[0], syn_idx[4], syn_idx[5], syn_idx[3]): A[diesel_syn_id, idx].sum() * 100
        }
        fraction_syn.append(syn_diesel_dict)

    # default_df - Market
    rows_default_diesel = [(list(i.keys())[0][1], list(i.keys())[0][2]) for i in fraction_fossil]
    columns_default_diesel = [(list(i.keys())[0][0].split(" ")[0]) for i in fraction_fossil]
    set_columns_default_diesel= set(columns_default_diesel)
    df_default = pd.DataFrame(index=rows_default_diesel, columns=list(set_columns_default_diesel))

    for row in df_default.index:
        for column in df_default.columns:
            df_default.loc[[row], column] = [(list(i.keys())[0][0].split(",")[0].split(" ")[2]) for i in fraction_fossil]

    # default_df - Region
    rows_default1_diesel = [(list(i.keys())[0][1], list(i.keys())[0][2]) for i in fraction_fossil]
    columns_default1_diesel = ["Region"]
    df_default1 = pd.DataFrame(index=rows_default1_diesel, columns=columns_default1_diesel)

    for row in df_default1.index:
        for column in df_default1.columns:
            df_default1.loc[[row], column] = [(list(i.keys())[0][3].split(",")[0]) for i in fraction_fossil]

    # fossil
    rows_diesel_fossil = [(list(i.keys())[0][1], list(i.keys())[0][2]) for i in fraction_fossil]
    rows_diesel = [(list(i.keys())[0][1], list(i.keys())[0][2], list(i.keys())[0][3]) for i in fraction_fossil]
    columns_diesel_fossil = [list(i.keys())[0][0] for i in fraction_fossil]
    set_columns_diesel_fossil = set(columns_diesel_fossil)
    df_diesel_fossil = pd.DataFrame(index=rows_diesel_fossil, columns=list(set_columns_diesel_fossil))
    df_diesel_fossil1 = pd.DataFrame(index=rows_diesel, columns=list(set_columns_diesel_fossil))

    for row in df_diesel_fossil1.index:
        for column in df_diesel_fossil.columns:
            df_diesel_fossil1.loc[[row], [column]] = [np.abs(i[(column, *row)]) for i in fraction_fossil if
                                                     list(i.keys())[0] == (column, *row)][0]

    newindex = []
    for i in df_diesel_fossil1.index:
        newindex.append(i[0:2])
    df_diesel_fossil1 = df_diesel_fossil1.reset_index()
    df_diesel_fossil1["new index"] = newindex
    df_diesel_fossil1 = df_diesel_fossil1.set_index("new index")
    df_diesel_fossil1 = df_diesel_fossil1.drop(columns=["index"])
    df_diesel_fossil1.rename(columns={'market for diesel, low-sulfur': 'Fossil'}, inplace=True)

    # bio-based
    rows_diesel_bio = [(list(i.keys())[0][1], list(i.keys())[0][2]) for i in fraction_bio]
    rows_diesel_bio1 = [(list(i.keys())[0][1], list(i.keys())[0][2], list(i.keys())[0][3]) for i in fraction_bio]
    columns_diesel_bio = [list(i.keys())[0][0] for i in fraction_bio]
    set_columns_diesel_bio = set(columns_diesel_fossil)
    df_diesel_bio = pd.DataFrame(index=rows_diesel_bio, columns=list(columns_diesel_bio))
    df_diesel_bio1 = pd.DataFrame(index=rows_diesel_bio1, columns=list(set_columns_diesel_bio))

    for row in df_diesel_bio1.index:
        for column in df_diesel_bio.columns:
            df_diesel_bio1.loc[[row], [column]] = [np.abs(i[(column, *row)]) for i in fraction_bio if
                                                     list(i.keys())[0] == (column, *row)][0]

    newindex1 = []
    for i in df_diesel_bio1.index:
        newindex1.append(i[0:2])
    df_diesel_bio1 = df_diesel_bio1.reset_index()
    df_diesel_bio1["index_test"] = newindex
    df_diesel_bio1 = df_diesel_bio1.set_index("index_test")
    df_diesel_bio1 = df_diesel_bio1.drop(columns=["index"])
    df_diesel_bio1.rename(columns={'market for diesel, low-sulfur': 'Bio-based'}, inplace=True)

    #Synthetic
    rows_diesel_syn = [(list(i.keys())[0][1], list(i.keys())[0][2]) for i in fraction_syn]
    rows_diesel_syn1 = [(list(i.keys())[0][1], list(i.keys())[0][2], list(i.keys())[0][3]) for i in fraction_syn]
    columns_diesel_syn = [list(i.keys())[0][0] for i in fraction_syn]
    set_columns_diesel_syn = set(columns_diesel_syn)
    df_diesel_syn = pd.DataFrame(index=rows_diesel_syn, columns=list(columns_diesel_syn))
    df_diesel_syn1 = pd.DataFrame(index=rows_diesel_syn1, columns=list(set_columns_diesel_syn))

    for row in df_diesel_syn1.index:
        for column in df_diesel_syn.columns:
            df_diesel_syn1.loc[[row], [column]] = [np.abs(i[(column, *row)]) for i in fraction_syn if
                                                     list(i.keys())[0] == (column, *row)][0]

    newindex2 = []
    for i in df_diesel_bio1.index:
        newindex2.append(i[0:2])
    df_diesel_syn1 = df_diesel_syn1.reset_index()
    df_diesel_syn1["index_test"] = newindex2
    df_diesel_syn1 = df_diesel_syn1.set_index("index_test")
    df_diesel_syn1 = df_diesel_syn1.drop(columns=["index"])
    df_diesel_syn1.rename(columns={'market for diesel, low-sulfur': 'Synthetic'}, inplace=True)

    dfs_diesel = [df_default, df_default1, df_diesel_fossil1, df_diesel_bio1, df_diesel_syn1]
    df_STORE_diesel = pd.concat(dfs_diesel, axis=1)

    set_rows_diesel= set(rows_diesel_fossil)
    df_World_diesel = pd.DataFrame(index=list(set_rows_diesel), columns=df_STORE_diesel.columns)
    df_World_diesel['market'] = "diesel"
    df_World_diesel['Region'] = "World"
    df_World_diesel['Fossil'] = df_STORE_diesel["Fossil"].mean()
    df_World_diesel['Bio-based'] = df_STORE_diesel["Bio-based"].mean()
    df_World_diesel['Synthetic'] = df_STORE_diesel["Synthetic"].mean()

    df_diesel_store = [df_STORE_diesel, df_World_diesel]
    df_diesel = pd.concat(df_diesel_store, axis=0)

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

df_STORE.to_excel(r"./diesel_pathway_breakdown.xlsx")
