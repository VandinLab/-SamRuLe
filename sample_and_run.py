import argparse
from tqdm import tqdm
import numpy as np
from time import time
import os

parser = argparse.ArgumentParser()
parser.add_argument("-db", help="path to tabulat dataset input file")
parser.add_argument("-r", help="regularization parameter (def 0.0001)", type=float, default=0.0001)
parser.add_argument("-k", help="max number of rules in a rule list (def = 5)", type=int, default=5)
parser.add_argument("-z", help="max number of conjunctions in each rule", type=int, default=1)
parser.add_argument("-minf", help="min freq of conjunctions", type=float, default=0.)
parser.add_argument("-op", help="output prefix (def. empty)", default="")
parser.add_argument("-s", help="sampling rate (def=-1 for no sampling)", type=float, default=-1)
parser.add_argument("-m", help="sampling size (def=-1 for no sampling)", type=int, default=-1)
parser.add_argument("-v", help="verbose level (def. 1)", type=int, default=1)
parser.add_argument("-f", help="1 = force creating new sample, 0 = use sample as is (def. 1)", type=int, default=1)
args = parser.parse_args()

# sample the dataset
sample_db = "data/"+str(args.op)+"sample_db_cor.db"
sample_labels = "data/"+str(args.op)+"sample_labels_cor.labels"
cmd = "python tabularbinary_to_corels.py -db "+args.db+" -od "+sample_db+" -ol "+sample_labels+" -s "+str(args.s)+" -m "+str(args.m)+" -v "+str(args.v)+" -z "+str(args.z)+" -minf "+str(args.minf)
if args.v > 0:
    print(cmd)
    print()
if args.f > 0:
    ret_val = os.system(cmd)
    if ret_val > 0:
        print("ERROR with tabularbinary_to_corels.py!!!")
        print(cmd)
        exit(1)

# run the alg
cmd = "python run_alg.py -db "+sample_db+" -dbl "+sample_labels+" -k "+str(args.k)+" -r "+str(args.r)+" -op "+str(args.op)+" -v "+str(args.v)
if args.v > 0:
    print(cmd)
    print()
ret_val = os.system(cmd)
if ret_val > 0:
    print("ERROR with run_alg.py!!!")
    print(cmd)
    exit(1)
