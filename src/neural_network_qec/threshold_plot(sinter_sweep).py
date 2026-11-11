"""My first inspection of the saved Sinter batches, before plotting them.

Run this file from the repository root. It prints representative grouped rows;
it does not yet combine batches, separate round counts, or estimate a threshold.
"""

import json

import pandas as pd

# import numpy as np
# from neural_network_qec import sinter_asymmetric_10x.csv

df = pd.read_csv("sinter_asymmetric_10x.csv")

# df['raw_ler'] = df['errors']/df['shots']

parsed_dicts = df["json_metadata"].apply(json.loads)

expanded_df = parsed_dicts.apply(pd.Series)
# print(expanded_df.value_counts())

df1 = pd.concat([df.drop(columns=["json_metadata"]), expanded_df], axis=1)
df2 = df1.drop(columns=["discards", "decoder", "custom_counts", "noise_model"])
# df1['raw_ler'] = df1['errors'] / df1['shots']
# print(df2.columns)
# print(df2.value_counts())

# I am inspecting the metadata layout here. first() selects the first
# non-null value per column, not a sum of repeated simulation batches. Grouping
# only by (d, p) also mixes round counts, so these are not aggregate LERs.
group_df = df2.groupby(["d", "p"])
print(group_df.first())

# print(df1['discards'].unique())
# value_counts().sum())
