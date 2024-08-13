import argparse
import pandas as pd
from tqdm import tqdm
import numpy as np
from time import time
import os
import math

parser = argparse.ArgumentParser()
parser.add_argument("-db", help="path to dataset input file")
parser.add_argument("-dbl", help="path to labels input file")
parser.add_argument("-r", help="regularization parameter (def 0.0001)", type=float, default=0.0001)
parser.add_argument("-k", help="max number of rules in a rule list (def = 5)", type=int, default=5)
parser.add_argument("-i", help="number of iterations (def = 10000)", type=int, default=10000)
parser.add_argument("-z", help="max number of conjunctions in each rule", type=int, default=1)
parser.add_argument("-op", help="output prefix (def. empty)", default="")
parser.add_argument("-ores", help="output results path (def. results_sblr.csv)", default="results_sblr.csv")
parser.add_argument("-v", help="verbose level (def. 0)", type=int, default=0)
args = parser.parse_args()

k = args.k
z = args.z

# run the algorithm
ruleset_size_sbrl = k+1
out_path = str(args.op)+"sbrlout.txt"
cmd = "./sbrlmod/sbrlmod -d 1 -t 3 -s "+str(ruleset_size_sbrl)+" -i "+str(args.i)+" "+args.db+" "+args.dbl+" "+args.db+" "+args.dbl+" > "+out_path
if args.v > 0:
    print(cmd)
os.system(cmd)

# parse results
fin = open(out_path,"r")
running_time = -1.
min_objective = 0.
optimal_rule = ""
opt_rule_str = ""
for line in fin:
    parse_term = "Time to train"
    if parse_term in line:
        line_parsed = line.replace("\n","")
        line_parsed = line_parsed.replace("Time to train: Elapsed time ","")
        first_time_pos = line_parsed.find(".")
        line_parsed = line_parsed[:first_time_pos]
        print(line_parsed)
        running_time = float(line_parsed)
        if args.v > 0:
            print("running time:",running_time)
    parse_term = "test accuracy = "
    if parse_term in line:
        line_parsed = line.replace("\n","")
        line_parsed = line_parsed.replace(parse_term,"")
        min_objective = float(line_parsed)
        min_objective = 1-min_objective + k*args.r
        if args.v > 0:
            print("min_objective:",min_objective)
    parse_term = "OPTIMAL RULE LIST"
    if parse_term in line:
        line_parsed = line.replace("\n","")
        opt_rule_str = ""
        while len(line)>0:
            line = fin.readline()
            line = line.replace("\n","")
            if len(line)>0:
                opt_rule_str = opt_rule_str+line+", "
        last_comma_pos = opt_rule_str.rfind(',')
        opt_rule_str = opt_rule_str[:last_comma_pos]
        optimal_rule = opt_rule_str
        if args.v > 0:
            print("optimal rule:",opt_rule_str)

if running_time < 0:
    print("error for \n     ",cmd)
    exit()

# save results to file
res_file_path = args.ores
if not os.path.isfile(res_file_path):
    fout = open(res_file_path,"w")
    fout.write("dataset;k;z;alpha;iterations;running_time;min_loss;opt_rule\n")
    fout.close()
fout = open(res_file_path,"a")
res = args.db+";"+str(k)+";"+str(z)+";"+str(args.r)+";"+str(args.i)+";"+str(running_time)+";"+str(min_objective)+";"+opt_rule_str
fout.write(res+"\n")
fout.close()
