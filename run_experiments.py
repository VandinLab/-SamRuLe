import argparse
from tqdm import tqdm
from time import time
import os
from multiprocessing import Pool

db_parameters = { "data/mushroom_tab.csv" : (5 , 200),  "data/susy_tab.csv" : (5 , 1),  "data/phishing_tab.csv" : (8 , 100), "data/adult_tab.csv" : (4 , 100), "data/bank_tab.csv" : (4 , 100), "data/higgs_tab.csv" : (3 , 1), "data/ijcnn1_tab.csv" : (8 , 100), "data/a9a_tab.csv" : (4 , 100)}
exp_parameters = [ (0.025,1.) , (0.01,1.) , (0.005,1.) , (0.05,0.5) , (0.025,0.5) , (0.01,0.5) , (0.05,0.25) , (0.025,0.25) , (0.01,0.25) ]
num_runs = 10

num_workers = 5

def execute_cmd(cmd):
    print(cmd)
    os.system(cmd)

pool = Pool(processes=num_workers)
parallel_res = []

for run_id in range(num_runs):
    for dataset in db_parameters:
        print("dataset",dataset)
        params_db = db_parameters[dataset]
        k = params_db[0]
        j = 0
        for params in exp_parameters:
            theta = params[0]
            eps = params[1]
            print("NEW EXPERIMENT: ",dataset," t =",theta," k =",k, " e =",eps)
            db_pref = dataset
            db_pref = db_pref.replace("data/","")
            db_pref = db_pref.replace("tab.csv","")
            db_pref = db_pref+str(j)+"_"
            j += 1
            cmd = "python main.py -db "+dataset+" -theta "+str(theta)+" -k "+str(k)+" -epsilon "+str(eps)+" -op "+db_pref+" -v 0"
            #print(cmd)
            #os.system(cmd)
            res = pool.apply_async(execute_cmd, (cmd,))
            parallel_res.append(res)
    for res in tqdm(parallel_res):
        res.get()
