"""Caller for time evaluation with different number of threads and/or processes."""
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from config import INPUT_DATA_THREADS
from config import MAX_PROCESSES
from config import MAX_THREADS
from config import PERIOD

SCALABILITY_ANALYSIS = "THREADS"  # @["THREADS", "PROCESSES"]
PATH_AUXINPUT_PARAMS = Path("./resources/sliced_input_params.npy")


def caller_exec_time_threads(MAX_THREADS):
    """Caller for execution of exec_time_threads.py .

    Parameters:
    -----------
    MAX_THREADS: int
        maximum number of threads that will be iterated through (set in config.py)

    Returns:
    --------
    times_df_threads_MAX_THREADS.pickle: pd.DataFrame
        saves the output in ./resources as dataframe

    """
    check = Path("./resources/times_df_threads_" + str(MAX_THREADS) + ".pickle")
    if not check.exists():

        input_params = np.load(INPUT_DATA_THREADS, allow_pickle=True).item()[PERIOD]
        # input_params = input_params[PERIOD]
        np.save(PATH_AUXINPUT_PARAMS, input_params, allow_pickle=True)

        for n_threads in range(1, MAX_THREADS + 1):
            call_ = "python exec_time_threads.py " + str(n_threads)
            subprocess.call(call_, shell=True)

    plot_ = "python plot_time_threads.py"
    if len(sys.argv) > 1 and sys.argv[1] == "save":
        plot_ = plot_ + " " + sys.argv[1]
    subprocess.call(plot_, shell=True)

    os.remove(PATH_AUXINPUT_PARAMS)


def caller_exec_time_processes(MAX_PROCESSES):
    """Caller for execution of exec_time_processes.py .

    Parameters:
    -----------
    MAX_PROCESSES: int
        maximum number of processes that will be used through mpiexec .

    Returns:
    --------
    TBD

    """
    for n_processes in range(1, MAX_PROCESSES + 1):

        mpiexec_ = (
            "mpiexec.hydra -n "
            + str(n_processes)
            + " -usize 3 python process_time_only.py "
            + str(n_processes)
        )
        subprocess.call(mpiexec_, shell=True)


if __name__ == "__main__":

    if SCALABILITY_ANALYSIS == "THREADS":
        caller_exec_time_threads(MAX_THREADS)
    elif SCALABILITY_ANALYSIS == "PROCESSES":
        caller_exec_time_processes(MAX_PROCESSES)
    else:
        pass
