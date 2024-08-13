import pandas as pd
import argparse
from tqdm import tqdm
import numpy as np
from time import time
from itertools import chain, combinations

parser = argparse.ArgumentParser()
parser.add_argument("-db", help="path to input file")
parser.add_argument("-od", help="path to output file")
parser.add_argument("-z", help="max number of conjunctions in each rule", type=int, default=1)
parser.add_argument("-minf", help="min freq of conjunctions", type=float, default=0.)
parser.add_argument("-v", help="verbose level (def. 1)", type=int, default=1)
args = parser.parse_args()

df = pd.read_csv(args.db)
df = df.astype(int)
if args.v > 0:
    print(df)

# higher-order features if z > 1
def subsetsiter(features_list , z):
    # note we return an iterator rather than a list
    return chain.from_iterable(combinations(features_list,n) for n in range(2,z+1))

if args.z > 1:
    if args.v > 0:
        print("num cols before combinations",df.columns.shape[0])
    z = args.z
    features_list = list(df.columns.values)
    features_list.remove("{T}")
    combinations_iter = subsetsiter(features_list , z)
    est_tot = df.columns.shape[0]**z
    for comb in tqdm(combinations_iter, total=est_tot):
        comb = list(comb)
        df_new_col = df[comb[0]].copy()
        freqs_ind = [df_new_col.mean()]
        new_feature_name = comb[0]
        for i in range(1,len(comb)):
            df_new_col = df_new_col * df[comb[i]]
            freqs_ind.append(df[comb[i]].mean())
            new_feature_name = new_feature_name.replace("}","") + " and " + comb[i].replace("{","")
        new_col_freq = df_new_col.mean()
        to_add = 1
        if args.v > 100:
            print(comb," freq ",new_col_freq," new name ",new_feature_name)
        if new_col_freq in freqs_ind:
            if args.v > 100:
                print("   to add 0 since ",freqs_ind)
            to_add = 0
        if new_col_freq == 0. or new_col_freq < args.minf:
            to_add = 0
        if to_add == 1:
            df[new_feature_name] = df_new_col
    if args.v > 0:
        print("num cols after combinations",df.columns.shape[0])

# write dataset to csv
if args.v > 0:
    print("writing to file...")
df.to_csv(args.od)
