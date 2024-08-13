import argparse
from tqdm import tqdm
from time import time
import os
from multiprocessing import Pool

parameters = { "data/mushroom_tab.csv" : (5 , 200),  "data/susy_tab.csv" : (5 , 1),  "data/phishing_tab.csv" : (8 , 100), "data/adult_tab.csv" : (4 , 100), "data/bank_tab.csv" : (4 , 100), "data/a9a_tab.csv" : (4 , 100)}
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
        db_pref = dataset
        db_pref = db_pref.replace("data/","")
        db_pref = db_pref.replace("_tab.csv","")
        db_path = "data/"+db_pref+"_tab.csv"
        cmd = "python run_ripper.py -db "+db_path+" -k "+str(k)+" -s "+str(repl)
        print(cmd)
        #os.system(cmd)
        res = pool.apply_async(execute_cmd, (cmd,))
        parallel_res.append(res)
    for res in tqdm(parallel_res):
        res.get()
