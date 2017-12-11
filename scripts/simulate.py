#!/usr/bin/env python3

__author__ = "Ankush Aniket Mishra"
__copyright__ = "Copyright 2017, Ankush A. Mishra"
__license__ = "MIT"

import os, subprocess as sp, sys
import multiprocessing as mp
from queue import Queue
from threading import Thread
import threading
import argparse
import numpy as np

path_to_ns = '/home/emanon/Desktop/NW/code/ns-allinone-3.27/ns-3.27'


def log(*args):
    print(*args)

def ns_run(run_file, output_file, num_wifis, seed, run, sir=False, args=""):
    """
    Runs the simulation run_file based on the params.
    """
    os.chdir(path_to_ns)
    sir_str = "true" if sir else "false"
    cmd = './waf --run \"' + run_file + ' --log-route=true --seed=' + str(seed) + ' --run=' + str(run) + ' --nWifis=' \
          + str(num_wifis)  + ' --SIR=' + sir_str + ' ' + args + ' \" > ' + output_file + ' 2>&1 '

    process = ["/bin/bash", "-c", cmd]

    with sp.Popen(process, stderr=sp.DEVNULL, stdout=sp.DEVNULL) as p:
        retcode = p.wait()
        if retcode:
            p.kill()
            p.wait()
            cmd = "./waf"
            raise sp.CalledProcessError(retcode, cmd)
        else:
            log("Finished simulation on cmd {}".format(cmd))

def worker(queue, run):
    """Process files from the queue."""
    for args in iter(queue.get, None):
        try:
            run(*args)
        except Exception as e: # catch exceptions to avoid exiting the thread prematurely
            print('{} failed: {}'.format(args, e), file=sys.stderr)

def start_processes_in_parallel(queue, func, number_of_process=None):
    """
        Starts threads to run the function with processes in parallel
        :param queue: Queue of tasks i.e. files to process, also the arguments to run()
        :param number_of_process: If none is provided, the total number of CPU Cores - 1 is taken.
        :return: Nothing is returned.
    """
    if not number_of_process:
        number_of_process = mp.cpu_count() - 1

        # start threads
    threads = [Thread(target=worker, args=(queue, func)) for _ in range(number_of_process)]
    for t in threads:
        t.daemon = True  # threads die if the program dies
        t.start()
    for _ in threads: queue.put_nowait(None)  # signal no more files
    for t in threads: t.join()  # wait for completion

def ns_compile():
    """
    Compiles any not compiled code.
    """
    os.chdir(path_to_ns)

    cmd = './waf'

    process = ["/bin/bash", "-c", cmd]

    with sp.Popen(process, stderr=sp.DEVNULL, stdout=sp.DEVNULL) as p:
        retcode = p.wait()
        if retcode:
            p.kill()
            p.wait()
            cmd = "./waf"
            raise sp.CalledProcessError(retcode, cmd)
        else:
            log("Finished compilation of all files.")

def simulate(max_runs, nWifis, sir, init=1, run_file="scratch/epidemic-comp", file_prefix="logs/log_", num_proc=None, prog_args=[], seed=None):
    seed = np.random.randint(2 ** 31, dtype=np.int32) if seed is None else seed
    os.chdir(path_to_ns)

    # Ensure code is compiled to avoid any troubles
    ns_compile()
        
    q = Queue()
    for run in range(init, init + max_runs):
        q.put_nowait((run_file, file_prefix + str(run) + ".log", nWifis, seed, run, sir, " ".join(prog_args)))

    start_processes_in_parallel(q, ns_run, num_proc)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--max-runs', type=int, dest='max_runs', nargs='?', default=10, const=10, help='Maximum number of simulation runs.')
    parser.add_argument('-i', '--init-run', type=int, dest='init', nargs='?', default=1, const=1, help='Initial Run number.')
    parser.add_argument('-nw', '--nWifis', type=int, dest='nWifis', nargs='?', default=10, const=10, help='Number of wifi nodes in simulations.')
    parser.add_argument('-n', '--proc', type=int, dest='proc', default=mp.cpu_count() - 1, nargs='?', help='Number of processes to run in parallel', metavar='N')
    parser.add_argument('-rf', '--run-file', type=str, nargs='?', dest='run_file', default="scratch/epidemic-comp", const="scratch/epidemic-comp", help="File to be run under waf.")
    parser.add_argument('-fp', '-file-prefix', type=str, nargs='?', dest='file_prefix', default="logs/log_", const="logs/log_",help='File Prefix of generated files')
    parser.add_argument('--sir', dest='sir', action='store_const', const=True, default=False, help='Enable SIR')
    parser.add_argument('--seed', dest='seed', nargs='?', const=None, default=None, help='Value of seed to use', type=int)
    parser.add_argument('args', nargs=argparse.REMAINDER, help="Optional arguments to the program")
    args = parser.parse_args()
    log("Program args: {}".format((args.max_runs, args.nWifis, args.sir, args.init, args.run_file, args.file_prefix, args.proc, args.args, args.seed)))
    simulate(args.max_runs, args.nWifis, args.sir, args.init, args.run_file, args.file_prefix, args.proc, args.args, args.seed)
