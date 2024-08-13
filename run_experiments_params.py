import argparse
from tqdm import tqdm
from time import time
import os
from multiprocessing import Pool

db_parameters = { "data/mushroom_tab.csv" : (5 , 200),  "data/phishing_tab.csv" : (8 , 100)}
exp_parameters = [ (0.025,0.5) ]
max_z = 3
max_k = 5
minf = 0.0
num_runs = 10

num_workers = 5

def execute_cmd(cmd):
    print(cmd)
    os.system(cmd)

pool = Pool(processes=num_workers)
parallel_res = []

# first create z versions of datasets
for dataset in db_parameters:
    for z in range(2,max_z+1):
        out_db_path = dataset.replace("data/","data/z_"+str(z)+"_")
        print(out_db_path)
        if not os.path.isfile(out_db_path):
            cmd = "python tabularbinary_to_tabularbinary_z.py -db "+dataset+" -od "+out_db_path+" -z "+str(z)+" -minf "+str(minf)+" -v 0"
            res = pool.apply_async(execute_cmd, (cmd,))
            parallel_res.append(res)
for res in tqdm(parallel_res):
    res.get()

parallel_res = []
j = 0
for run_id in range(num_runs):
    for dataset in db_parameters:
        print("dataset",dataset)
        params_db = db_parameters[dataset]
        #max_k = params_db[0]
        params = exp_parameters[0]
        theta = params[0]
        eps = params[1]
        for k in range(1,max_k+1):
            for z in range(1,max_z+1):
                print("NEW EXPERIMENT: ",dataset," t =",theta," k =",k," z =",z, " e =",eps)
                if z > 1:
                    db_path = dataset.replace("data/","data/z_"+str(z)+"_")
                else:
                    db_path = dataset
                db_pref = dataset
                db_pref = db_pref.replace("data/","")
                db_pref = db_pref.replace("tab.csv","")
                db_pref = db_pref+"_par_"+str(j)+"_"
                j += 1
                cmd = "python main.py -db "+db_path+" -theta "+str(theta)+" -k "+str(k)+" -z 1 -epsilon "+str(eps)+" -op "+db_pref+" -v 0 -ores results_params.csv"
                #print(cmd)
                #os.system(cmd)
                res = pool.apply_async(execute_cmd, (cmd,))
                parallel_res.append(res)
for res in tqdm(parallel_res):
    res.get()
