import pandas as pd
import argparse
from tqdm import tqdm
import numpy as np
from time import time

parser = argparse.ArgumentParser()
parser.add_argument("-incsv", help="path to results input file", default="results.csv")
parser.add_argument("-outcsv", help="path to output csv file", default="results_true_losses.csv")
parser.add_argument("-v", help="verbose level (def. 1)", type=int, default=1)
args = parser.parse_args()

results_csv = pd.read_csv(args.incsv,sep=";")
print(results_csv)

dbs = results_csv["dataset"].unique()
print(dbs)

def parse_rule_list(rule_list):
    if args.v > 10:
        print("Parsing rule list")
        print(rule_list)
    rules_str = rule_list.split(", ")
    if args.v > 10:
        print(rules_str)
    for i in range(len(rules_str)):
        rule_str = rules_str[i]
        if "then" in rule_str:
            items = rule_str.split(" then ")
            cond = items[0]
            pred = items[1]
            cond = cond.replace("else if (","")
            cond = cond.replace("if (","")
            cond = cond.replace(")","")
            pred = pred.replace("(","")
            pred = pred.replace(")","")
        else:
            cond = ""
            pred = rule_str.replace("else (","")
            pred = pred.replace(")","")
        rules_str[i] = (cond,pred)
    if args.v > 10:
        print(rules_str)
    return rules_str

def predict(df , cond_pred_list):
    if args.v > 10:
        print("****predicting",cond_pred_list)
    df_T = df[["{T}"]].copy()
    df_T["{P}"] = 0
    if args.v > 10:
        print(df_T)
    not_covered = df.copy()
    for (cond,pred) in cond_pred_list:
        if "1" in pred:
            pred_val = 1
        else:
            pred_val = 0
        if len(cond) > 0:
            covered = not_covered.loc[ not_covered[cond]==1 ]
            not_covered = not_covered.loc[ not_covered[cond]==0 ]
            pred_index = covered.index
        else:
            pred_index = not_covered.index
        if args.v > 10:
            print("pred_val",pred_val)
            print("pred_index",pred_index)
            print("before df_T.loc[pred_index]\n",df_T.loc[pred_index])
        df_T.loc[pred_index, '{P}'] = pred_val
        if args.v > 10:
            print("after df_T.loc[pred_index]\n",df_T.loc[pred_index])
        #print(df_T)
    loss = df_T["{P}"] == df["{T}"]
    loss = 1. - loss.mean() + 0.0001*(len(cond_pred_list)-1)
    if args.v > 10:
        print("loss",loss)
    return loss

df_list = []
for db in dbs:
    print("Loading",db,"...")
    df = pd.read_csv(db)
    df = df.astype(int)
    if args.v > 0:
        print(df)
    results_csv_db = results_csv.loc[ results_csv["dataset"]==db ]
    if args.v > 10:
        print(results_csv_db)
    results_csv_db_rules = results_csv_db["opt_rule"].unique()
    for rule_list in tqdm(results_csv_db_rules):
        cond_pred_list = parse_rule_list(rule_list)
        loss = predict(df , cond_pred_list)
        df_entry = dict()
        df_entry["dataset"] = db
        df_entry["opt_rule"] = rule_list
        df_entry["loss_db"] = loss
        df_list.append(df_entry)

df = pd.DataFrame.from_dict(df_list)
print(df)
df.to_csv(args.outcsv,sep=";")
