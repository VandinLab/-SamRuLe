import argparse
from tqdm import tqdm
from time import time
import os
from multiprocessing import Pool

parameters = { "data/mushroom_tab.csv" : (5 , 200),  "data/susy_tab.csv" : (5 , 1),  "data/phishing_tab.csv" : (8 , 100), "data/adult_tab.csv" : (4 , 100), "data/bank_tab.csv" : (4 , 100), "data/higgs_tab.csv" : (3 , 1), "data/ijcnn1_tab.csv" : (8 , 100), "data/a9a_tab.csv" : (4 , 100)}
num_runs = 10

num_workers = 5

def execute_cmd(cmd):
    print(cmd)
    os.system(cmd)

pool = Pool(processes=num_workers)

parallel_res = []
for run_id in range(num_runs):
    for dataset in parameters:
        print("dataset",dataset)
        params = parameters[dataset]
        #print(params)
        k = params[0]
        repl = params[1]
        print("NEW EXPERIMENT: ",dataset," k =",k, " repl =",repl)
        db_pref = "exact_"+dataset
        db_pref = db_pref.replace("data/","")
        db_pref = db_pref.replace("tab.csv","")
        cmd = "python main.py -db "+dataset+" -exact "+str(repl)+" -k "+str(k)+" -op "+str(db_pref)+" -ores results_exact.csv -v 0"
        if run_id > 0:
            cmd = cmd + " -f 0"
        #print(cmd)
        #os.system(cmd)
        res = pool.apply_async(execute_cmd, (cmd,))
        parallel_res.append(res)
    for res in tqdm(parallel_res):
        res.get()
