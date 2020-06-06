"""Plotting module for vizualization of time vs. number of threads / processes."""
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from caller_scalability_analysis import SCALABILITY_ANALYSIS
from config import MAX_PROCESSES
from config import MAX_THREADS
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import MaxNLocator


def plot_time_threads(MAX_THREADS):
    """Illustration of execution time to available threads.

    Parameters:
    -----------
    MAX_THREADS: int
        maximum number of available (used) threads set in config.py

    Returns:
    --------
    TBD

    """
    times_df_threads = pd.read_pickle(
        f"./resources/times_df_threads_{MAX_THREADS}.pickle"
    )

    ys = [*times_df_threads.iloc[:1].mean()]
    # 1 second = 10^6 microseconds
    xs = [*range(1, MAX_THREADS + 1)]

    fig, ax = plt.subplots(1, 1)
    ax.plot(xs, ys)

    ax.set_xlabel("Number of threads")
    ax.set_ylabel("Microseconds")

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ",")))

    # Save or show
    if len(sys.argv) > 1 and sys.argv[1] == "save":
        fig.savefig("./resources/figure_time_num_threads.pdf", bbox_inches="tight")
    else:
        plt.show()


def plot_time_processes(MAX_PROCESSES):
    """Illustration of execution time to available processes in mpiexec.

    Parameters:
    -----------
    MAX_PROCESSES: int
        maximum number of available (used) processes set in config.py

    Returns:
    --------
    TBD

    """
    ys = [
        np.load(f"./resources/times_numproc_{i}.npy", allow_pickle=True)
        .item()
        .microseconds
        for i in range(1, MAX_PROCESSES + 1)
    ]

    xs = [*range(1, MAX_PROCESSES + 1)]

    plt.style.use("seaborn-dark-palette")
    fig, ax = plt.subplots(1, 1)

    ax.plot(xs, ys)

    ax.set_xlabel("Number of processes to use (mpiexec)")
    ax.set_ylabel("Microseconds")

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ",")))

    if len(sys.argv) > 1:
        if sys.argv[1] == "show":
            plt.show()
        if sys.argv[1] == "save":
            fig.savefig("./resources/process_time_plot.pdf", bbox_inches="tight")


if __name__ == "__main__":

    if SCALABILITY_ANALYSIS == "THREADS":
        plot_time_threads(MAX_THREADS)
    elif SCALABILITY_ANALYSIS == "PROCESSES":
        plot_time_processes(MAX_PROCESSES)
    else:
        pass
