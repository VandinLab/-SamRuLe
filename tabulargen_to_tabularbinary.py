import math
import os
import time
import pandas as pd
import argparse
from tqdm import tqdm
import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument("-db", help="path to input file")
parser.add_argument("-target", help="string of target column")
parser.add_argument("-tval", help="value of target to consider")
parser.add_argument("-maxd", help="max number of conjunctions", type=int, default = 3)
parser.add_argument("-ns", help="number of splits for numeric features", type=int, default = 5)
parser.add_argument("-o", help="output path",default="results_signfsr.csv")
parser.add_argument("-cat", help="categorize data (def. 0)",default=0, type=int)
parser.add_argument("-head", help="1 if data has an header (def. 0)",default=0, type=int)
parser.add_argument("-v", help="verbose level (def. 1)", type=int, default=1)
args = parser.parse_args()

debug_ = False


# parse the separating character
fin = open(args.db,"r")
line = fin.readline()
if ";" in line:
    sep_char = ";"
else:
    sep_char = ","

if args.head == 1:
    data = pd.read_csv(args.db,sep=sep_char)
else:
    data = pd.read_csv(args.db,header=None,sep=sep_char)
if args.cat == 1:
    data = data.astype('category')
if args.cat == 1:
    args.geneexp = 1
data.columns = data.columns.astype(str)
num_features = data.shape[1]-1
target_col = args.target
target_val = args.tval
if data.dtypes[target_col] == 'float64':
    data[target_col] = data[target_col].astype(int)
data[target_col] = data[target_col].astype(str)
data[target_col] = (data[target_col] == target_val).astype(int)
target_vals = data[target_col].unique()

data["{T}"] = data[target_col]
data.drop(target_col,axis=1,inplace=True)
target_col = "{T}"

if args.v > 0:
    print("target_col",target_col)
    print("target_val",target_val)
    print("target_vals",target_vals)
if len(target_vals) != 2:
    print("the target could not be cast in a binary vector, check again!")
    exit()
#print(data)
if args.v > 0:
    print(data.columns)
    print(data)

#data[target_col] = data[target_col]==target_val
num_samples = data.shape[0]
mu_est = data[target_col].mean()
if args.v > 0:
    print("num_samples",num_samples)
    print("mu_est",mu_est)

numeric_features = [x for x in data.select_dtypes(include=['number']).columns.values if x not in [target_col]]
non_numeric_features = [x for x in data.columns.values if x not in [target_col] and x not in numeric_features]
if args.v > 0:
    print("numeric_features",len(numeric_features))
    #print(numeric_features)
    print("non_numeric_features",len(non_numeric_features))
    #print(non_numeric_features)

if args.v > 0:
    print("generating binary features from categorical features...")
for attr_name in tqdm(non_numeric_features):
    unique_vals = data[attr_name].unique()
    for feat_val in unique_vals:
        feature_str = "{"+attr_name+"="+str(feat_val)+"}"
        data[feature_str] = (data[attr_name] == feat_val).astype(int)
    data.drop(attr_name,axis=1,inplace=True)

num_splits = args.ns
q = []
for i in range(1,num_splits):
    q.append(float(i)/float(num_splits))
#print("q",q)

if args.v > 0:
    print("generating binary features from numeric features...")
for attr_name in tqdm(numeric_features):
    values = data[attr_name]
    min_val = values.min()
    max_val = values.max()
    unique_vals = data[attr_name].unique()
    val_quantiles = set(np.quantile(values , q))
    #val_quantiles_unique = set(np.quantile(unique_vals , q))
    split_vals = val_quantiles
    #for i in val_quantiles_unique:
        #split_vals.add(i)
    for i in q:
        split_vals.add(i*(max_val-min_val)-min_val)

    for split_val in split_vals:
        if split_val > min_val and split_val < max_val:
            feature_str = "{"+attr_name+">="+str(split_val)+"}"
            data[feature_str] = (data[attr_name] >= split_val).astype(int)
            feature_str = "{"+attr_name+"<"+str(split_val)+"}"
            data[feature_str] = (data[attr_name] < split_val).astype(int)

    #print(attr_name)
    #print("   val_quantiles",val_quantiles)
    #print("   val_quantiles_unique",val_quantiles_unique)
    #print("   split_vals",split_vals)
    #print("   unique_vals",unique_vals)
    #max_val = data[attr_name].max()
    #min_val = data[attr_name].min()
    data.drop(attr_name,axis=1,inplace=True)

if args.v > 0:
    print(data.columns)
    print(data)

if args.v > 0:
    print("creating dataframe...")
    print("target fraction of 1",data["{T}"].mean())
data.fillna(0,inplace=True)
#print(df)
data.to_csv(args.o,index=False)
