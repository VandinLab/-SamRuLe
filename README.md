# Scalable Rule Lists Learning with Sampling #

This repository contains the code for the SamRuLe algorithm, a sampling-based approach to learn almost optimal rule lists from large datasets. SamRuLe is described in the paper "Scalable Rule Lists Learning with Sampling" by Leonardo Pellegrina and Fabio Vandin, published in KDD 2024 https://doi.org/10.1145/3637528.3671989 (see also https://doi.org/10.48550/arXiv.2406.12803 ).

This README describes how to run SamRuLe and how to reproduce the experiments described in the paper.

Please address questions and bug reports to Leonardo Pellegrina (leonardo.pellegrina@unipd.it) and Fabio Vandin (fabio.vandin@unipd.it).

### Compilation of the code for all methods ###
To execute SamRuLe and all other methods, first compile all the code.
You can do so with the command `make` in the folders
`src` (to compile CORELS) and
`sbrlmod` (to compile SBRL).

### Reproducing the experiments of the paper ###

The experiments described in the paper can be reproduced with scripts included in this repository.

First, download the .zip archive containing all datasets from the link http://tinyurl.com/SamRuLedatasets

Extract the .zip archive creating the `data` folder.

To reproduce the experiments described in the paper, run the following scripts:

For the experiments of Section 5.1: execute the commands
`python run_experiments.py` and `python run_experiments_exact.py`.

For the experiments of Section 5.2: execute the commands
`python run_experiments_ripper.py` and `python run_experiments_sbrl.py`.

For the experiments of Section 5.3: execute the command
`python run_experiments_params.py`

All the scripts produce `.csv` files that contain tables with all results.


### Running SamRuLe ###

SamRuLe can be ran using the script `main.py`. This script accepts various parameters:

```
usage: main.py [-h] [-db DB] [-r R] [-k K] [-z Z] [-minf MINF] [-exact EXACT]
               [-delta DELTA] [-epsilon EPSILON] [-theta THETA] [-op OP]
               [-ores ORES] [-v V] [-f F]

optional arguments:
  -h, --help        show this help message and exit
  -db DB            path to tabular dataset input file
  -r R              regularization parameter (def 0.0001)
  -k K              max number of rules in a rule list (def = 5)
  -z Z              max number of conjunctions in each rule
  -minf MINF        min freq of conjunctions
  -exact EXACT      if > 0, run on the entire dataset with given duplication
                    factor (defaul=0)
  -delta DELTA      confidence parameter
  -epsilon EPSILON  relative accuracy parameter
  -theta THETA      absolute accuracy parameter
  -op OP            output prefix (def. empty)
  -ores ORES        output results path (def. results.csv)
  -v V              verbose level (def. 1)
  -f F              1 = force creating new sample, 0 = use sample as is (def.
                    1)
```

### Description of the main parameters ###

* `-db` specifies the path to the input dataset file (see below for input format)
* `-r` specifies the regularization parameter (alpha in the paper, default set to 0.0001)
* `-k` sets the maximum length of rule lists (the maximum number of rules in a rule list, not counting the default rule, default set to 5)
* `-z` sets the maximum number of terms for the rules' conjunctions (default set to 1)
* `-exact` flag to run an exact algorithm (1 , runs CORELS) or the approximation (0, runs SamRuLe) (default set to 0)
* `-delta` confidence of the approximation (default set to 0.05)
* `-epsilon` relative accuracy parameter of the approximation (default set to 1)
* `-theta` absolute accuracy parameter of the approximation (default set to 0.01)
* `-minf` parameter to ignore conjunctions with frequency (i.e., fraction of covered instances) below this threshold (default set to 0)
* `-ores` path where to output the results in a .csv file (default is results.csv)


### Input format ###

The `main.py` script accepts as input (`-db` parameter) the path to a csv file.
The csv file should have an header containing the titles of the columns.
Each column should be a binary feature.
One of the column should have the name `{T}` corresponding to the binary target.
