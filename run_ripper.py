import argparse
import pandas as pd
from tqdm import tqdm
import numpy as np
import time
import os
import math
import wittgenstein as lw
import random

parser = argparse.ArgumentParser()
parser.add_argument("-db", help="path to dataset input file")
parser.add_argument("-dbl", help="path to labels input file")
parser.add_argument("-r", help="regularization parameter (def 0.0001)", type=float, default=0.0001)
parser.add_argument("-k", help="max number of rules in a rule list (def = 5)", type=int, default=5)
parser.add_argument("-s", help="number of replications (def. 1)", type=int, default=1)
parser.add_argument("-z", help="max number of conjunctions in each rule", type=int, default=1)
parser.add_argument("-ores", help="output results path (def. results_sblr.csv)", default="results_ripper.csv")
parser.add_argument("-v", help="verbose level (def. 0)", type=int, default=0)
args = parser.parse_args()

k = args.k
z = args.z

df = pd.read_csv(args.db)
df["{default}"] = 1.
df = df.loc[df.index.repeat(args.s)]
df.reset_index(drop=True, inplace=True)
if args.v > 1:
    print(df)

clf = lw.RIPPER(max_rules=k , random_state=random.randint(10, 20242024) , max_rule_conds=z, max_total_conds=z*k, k=10)

if args.v > 0:
    print("training ripper...")
start = time.time()
clf.fit(df, class_feat='{T}', pos_class=1)
end = time.time()
running_time = end - start
if args.v > 0:
    print("done in",running_time,"s")
    print(clf)
    print(clf.out_model())

df_label = df['{T}']
df.drop('{T}', axis=1, inplace=True)
accuracy = clf.score(df, df_label)
min_objective = 1.0-accuracy+args.r*k
if args.v > 0:
    print("loss",min_objective)


# save results to file
res_file_path = args.ores
if not os.path.isfile(res_file_path):
    fout = open(res_file_path,"w")
    fout.write("dataset;k;z;alpha;exact;running_time;min_loss;opt_rule\n")
    fout.close()
fout = open(res_file_path,"a")
opt_rule_str = ""
res = args.db+";"+str(k)+";"+str(z)+";"+str(args.r)+";"+str(args.s)+";"+str(running_time)+";"+str(min_objective)+";"+opt_rule_str
fout.write(res+"\n")
fout.close()
