import pandas as pd
import argparse
from tqdm import tqdm
import numpy as np
from time import time
from itertools import chain, combinations

parser = argparse.ArgumentParser()
parser.add_argument("-db", help="path to input file")
parser.add_argument("-od", help="path to output data file")
parser.add_argument("-ol", help="path to output labels file")
parser.add_argument("-z", help="max number of conjunctions in each rule", type=int, default=1)
parser.add_argument("-minf", help="min freq of conjunctions", type=float, default=0.)
parser.add_argument("-s", help="sampling rate (def=-1 for no sampling)", type=float, default=-1)
parser.add_argument("-m", help="sampling size (def=-1 for no sampling)", type=int, default=-1)
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
        if new_col_freq <= args.minf:
            to_add = 0
        if to_add == 1:
            df[new_feature_name] = df_new_col
    if args.v > 0:
        print("num cols after combinations",df.columns.shape[0])


# sampling of data
if args.s > 0 or args.m > 0:
    if args.s > 0:
        #df = df.sample(frac=args.s , replace=True, axis=0)
        df = df.loc[df.index.repeat(args.s)]
    else:
        df = df.sample(n=args.m , replace=True, axis=0)
    df.reset_index(drop=True, inplace=True)
    if args.v > 0:
        print("After resampling:")
        print(df)

def get_str_array(array_vals):
    #print(array_vals.shape[0])
    thrs = 3*(array_vals.shape[0]+10)
    vals_str = np.array2string(array_vals,separator=" ",prefix="",suffix="",threshold=thrs,max_line_width=thrs)
    return vals_str[1:-1]

# write label file
start = time()
if args.v > 0:
    print("Printing labels...")
target_col_name = "{T}"
df["{T=1}"] = df[target_col_name]
df["{T=0}"] = (df[target_col_name]-1)*(-1)
df_targ = df[["{T=1}","{T=0}"]]
df_targ = df_targ.transpose(copy=True)
df_targ.to_csv(args.ol,sep=" ",header=None)
elaps = time()-start
if args.v > 0:
    print("Done in",elaps)

# write data file
start = time()
if args.v > 0:
    print("Printing data...")
df.drop(target_col_name,axis=1,inplace=True)
df.drop("{T=1}",axis=1,inplace=True)
df.drop("{T=0}",axis=1,inplace=True)
df = df.transpose(copy=True)
df.to_csv(args.od,sep=" ",header=None)
elaps = time()-start
if args.v > 0:
    print("Done in",elaps)
