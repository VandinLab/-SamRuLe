import argparse
import pandas as pd
from tqdm import tqdm
import numpy as np
from time import time
import os
import math

parser = argparse.ArgumentParser()
parser.add_argument("-db", help="path to tabular dataset input file")
parser.add_argument("-r", help="regularization parameter (def 0.0001)", type=float, default=0.0001)
parser.add_argument("-k", help="max number of rules in a rule list (def = 5)", type=int, default=5)
parser.add_argument("-z", help="max number of conjunctions in each rule", type=int, default=1)
parser.add_argument("-minf", help="min freq of conjunctions", type=float, default=0.)
parser.add_argument("-exact", help="if > 0, run on the entire dataset with given duplication factor (defaul=0)", type=int, default=0)
parser.add_argument("-delta", help="confidence parameter", type=float, default=0.05)
parser.add_argument("-epsilon", help="relative accuracy parameter", type=float, default=1.)
parser.add_argument("-theta", help="absolute accuracy parameter", type=float, default=0.01)
parser.add_argument("-op", help="output prefix (def. empty)", default="")
parser.add_argument("-ores", help="output results path (def. results.csv)", default="results.csv")
parser.add_argument("-v", help="verbose level (def. 1)", type=int, default=0)
parser.add_argument("-f", help="1 = force creating new sample, 0 = use sample as is (def. 1)", type=int, default=1)
args = parser.parse_args()

if args.exact == 0:
    eps = args.epsilon
    theta = args.theta
    delta = args.delta
else:
    eps = theta = delta = 1.0
k = args.k
z = args.z

def check_current_sample_size(m):
    omega = k*z*math.log(2*math.e*d/z)+2
    ln_m = math.log(2./delta)/m
    ln_w_m = (omega+math.log(2./delta))/m
    term1 = math.sqrt(3*theta*ln_m)
    term2 = math.sqrt( 2*(theta+term1)*ln_w_m )
    term3 = 2*ln_w_m
    total = term1 + term2 + term3
    if total <= eps*theta:
        return 1
    else:
        return 0

m = 0
if args.exact == 0:
    # compute sample size

    #get number of features of the dataset
    df = pd.read_csv(args.db , nrows=10)
    d = df.columns.shape[0]
    if args.v > 0:
        print("number of features is",d)
    m_lb = 3*math.log(2./delta)/theta
    m_ub = m_lb
    while check_current_sample_size(m_ub)==0:
        m_ub = m_ub*2
    #print("m_lb",m_lb)
    #print("m_ub",m_ub)
    while m_ub-m_lb > 1.:
        m = (m_ub+m_lb)/2.
        #print("test m",m)
        test_check = check_current_sample_size(m)
        #print("check is",test_check)
        if test_check == 0:
            m_lb = m
        else:
            m_ub = m
    m = math.ceil(m_ub)
    if args.v > 0:
        print("sample size is",m)


# sample the dataset and run the algorithm
if args.exact == 0:
    cmd = "python sample_and_run.py -db "+args.db+" -k "+str(args.k)+" -z "+str(args.z)+" -minf "+str(args.minf)+" -r "+str(args.r)+" -m "+str(m)+" -op "+str(args.op)
else:
    cmd = "python sample_and_run.py -db "+args.db+" -k "+str(args.k)+" -z "+str(args.z)+" -minf "+str(args.minf)+" -r "+str(args.r)+" -s "+str(args.exact)+" -op "+str(args.op)
cmd = cmd+" -v "+str(args.v)
cmd = cmd+" -f "+str(args.f)
if args.v > 0:
    print(cmd)
ret_val = os.system(cmd)
if ret_val > 0:
    print("ERROR with sample_and_run.py!!!")
    print(cmd)
    exit(1)

# parse results
fin = open(str(args.op)+"out.txt","r")
running_time = 0.
min_objective = 0.
optimal_rule = ""
for line in fin:
    parse_term = "final total time: "
    if parse_term in line:
        line_parsed = line.replace("\n","")
        line_parsed = line_parsed.replace(parse_term,"")
        running_time = float(line_parsed)
        if args.v > 0:
            print("running time:",running_time)
    parse_term = "final min_objective: "
    if parse_term in line:
        line_parsed = line.replace("\n","")
        line_parsed = line_parsed.replace(parse_term,"")
        min_objective = float(line_parsed)
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

# save results to file
res_file_path = args.ores
if not os.path.isfile(res_file_path):
    fout = open(res_file_path,"w")
    fout.write("dataset;k;z;exact;theta;epsilon;delta;alpha;m;running_time;min_loss;opt_rule\n")
    fout.close()
fout = open(res_file_path,"a")
res = args.db+";"+str(k)+";"+str(z)+";"+str(args.exact)+";"+str(theta)+";"+str(eps)+";"+str(delta)+";"+str(args.r)+";"+str(m)+";"+str(running_time)+";"+str(min_objective)+";"+opt_rule_str
fout.write(res+"\n")
fout.close()
