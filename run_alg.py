import argparse
from tqdm import tqdm
import numpy as np
from time import time
import os

parser = argparse.ArgumentParser()
parser.add_argument("-db", help="path to dataset input file")
parser.add_argument("-dbl", help="path to labels input file")
parser.add_argument("-op", help="output prefix (def. empty)", default="")
parser.add_argument("-r", help="regularization parameter (def 0.0001)", type=float, default=0.0001)
parser.add_argument("-k", help="max number of rules in a rule list (def = 5)", type=int, default=5)
parser.add_argument("-v", help="verbose level (def. 1)", type=int, default=1)
args = parser.parse_args()

max_num_nodes = "1000000000"
#cmd = "./src/corels -n "+max_num_nodes+" -r "+str(args.r)+" -c 1 -p 2 "+args.db+" "+args.dbl+" -d "+str(args.k)+" |& tee out.txt"
corels_cmd = "./src/corels -n "+max_num_nodes+" -r "+str(args.r)+" -c 1 -p 1 "+args.db+" "+args.dbl+" -d "+str(args.k)
#cmd = "script -c \"./src/corels -n "+max_num_nodes+" -r "+str(args.r)+" -c 1 -p 1 "+args.db+" "+args.dbl+" -d "+str(args.k)+"\" -f "+str(args.op)+"out.txt"
fout_path = str(args.op)+"out.txt"
if args.v > 0:
    cmd = "script -c \""+corels_cmd+"\" -f "+fout_path
    print(cmd)
else:
    cmd = corels_cmd+" > "+fout_path
ret_val = os.system(cmd)
if ret_val > 0:
    print("ERROR with CORELS!!!")
    print(cmd)
    exit(1)
#os.system("tail out.txt")
