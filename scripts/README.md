## Scripts

This folder contains scripts to help the simulation and the rest. 

Current list of scripts contains:

 * simulate.py
 
### Simulate.py

This contains scripts to run the experiment under various random states, and parallel execution of the multiple simulations, since, the simulations are single threaded. 

To run:

`python3 simulate.py [args...]`

Note: Has to be run from the top level directory of ns-3

The arguments are given as follows:

	usage: simulate.py [-h] [-r [MAX_RUNS]] [-i [INIT]] [-nw [NWIFIS]] [-n [N]]
					   [-rf [RUN_FILE]] [-fp [FILE_PREFIX]] [--sir]
					   [--seed [SEED]]
					   ...

	positional arguments:
	  args                  Optional arguments to the program

	optional arguments:
	  -h, --help            show this help message and exit
	  -r [MAX_RUNS], --max-runs [MAX_RUNS]
							Maximum number of simulation runs.
	  -i [INIT], --init-run [INIT]
							Initial Run number.
	  -nw [NWIFIS], --nWifis [NWIFIS]
							Number of wifi nodes in simulations.
	  -n [N], --proc [N]    Number of processes to run in parallel
	  -rf [RUN_FILE], --run-file [RUN_FILE]
							File to be run under waf.
	  -fp [FILE_PREFIX], -file-prefix [FILE_PREFIX]
							File Prefix of generated files
	  --sir                 Enable SIR
	  --seed [SEED]         Value of seed to use
