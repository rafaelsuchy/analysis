"""Caller for execution time evaluation under different number of threads and/or processes."""
import os
import pickle
import subprocess
import sys
from pathlib import Path

from config import DATA_FORMAT
from config import INPUT_DATA
from config import MAX_THREADS_PROCESSES
from config import PERIOD

SCALABILITY_ANALYSIS = "threads"  # @["threads", "processes"]
PATH_AUXINPUT_PARAMS = Path(f"./resources/sliced_input_params.{DATA_FORMAT}")


def caller_exec_time_threads(MAX_THREADS):
    """Caller for analysis of computation time under different number of threads.

    Parameters:
    -----------
    MAX_THREADS: int
        Maximum number of threads that will be iterated through (set in config.py).

    Returns:
    --------
    times_df_threads_MAX_THREADS.pickle: pd.DataFrame
        Output saved in ./resources as pd.DataFrame.

    """
    for n_threads in range(1, MAX_THREADS + 1):
        call_ = "python exec_time_scalability.py " + str(n_threads)
        subprocess.call(call_, shell=True)


def caller_exec_time_processes(MAX_PROCESSES):
    """Caller for analysis of computation time under different number of processes.

    Parameters:
    -----------
    MAX_PROCESSES: int
        Maximum number of processes that will be iterated through using mpiexec.

    Returns:
    --------
    times_df_processes_MAX_PROCESSES.pickle: pd.DataFrame
        Output saved in ./resources as pd.DataFrame.

    """
    for n_processes in range(1, MAX_PROCESSES + 1):

        mpiexec_ = (
            "mpiexec.hydra -n "
            + str(n_processes)
            + " -usize 3 python exec_time_scalability.py "
            + str(n_processes)
        )
        subprocess.call(mpiexec_, shell=True)


if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == "processes":
        SCALABILITY_ANALYSIS = "processes"

    check = Path(
        "./resources/times_df_"
        + str(MAX_THREADS_PROCESSES[SCALABILITY_ANALYSIS])
        + f"{SCALABILITY_ANALYSIS}_{PERIOD}.{DATA_FORMAT}"
    )

    if not check.exists():

        input_params = pickle.load(open(INPUT_DATA, "rb"))[PERIOD]
        pickle.dump(input_params, open(PATH_AUXINPUT_PARAMS, "wb"))

        if SCALABILITY_ANALYSIS == "threads":
            caller_exec_time_threads(MAX_THREADS_PROCESSES[SCALABILITY_ANALYSIS])
        elif SCALABILITY_ANALYSIS == "processes":
            caller_exec_time_processes(MAX_THREADS_PROCESSES[SCALABILITY_ANALYSIS])
        else:
            pass

    else:
        print(
            "Data set already available. Move, rename or delete to create a new dataset."
        )

    if PATH_AUXINPUT_PARAMS.exists():
        os.remove(PATH_AUXINPUT_PARAMS)

    plot_ = "python plot_scalability_analysis.py"
    if len(sys.argv) > 1 and sys.argv[1] == "save":
        plot_ = plot_ + " " + sys.argv[1]
    subprocess.call(plot_, shell=True)
