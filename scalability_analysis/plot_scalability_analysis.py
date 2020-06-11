"""Plotting module for vizualization of computation time vs. number of threads / processes."""
import sys

import matplotlib.pyplot as plt
import pandas as pd
from caller_scalability_analysis import SCALABILITY_ANALYSIS
from config import MAX_THREADS_PROCESSES
from config import PERIOD
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import MaxNLocator


def plot_time(processes_threads, max_processes_threads, period=""):
    """Illustration of execution time to available threads / processes.

    Parameters:
    -----------
    SCALABILITY_ANALYSIS: str
        Type of scalability analysis to perform: processes or threads.
    max_processes_threads: int
        Maximum number of available (used) processes or threads set in config.py.

    Returns:
    --------
    figure_time_{max_processes_threads}_{SCALABILITY_ANALYSIS}: fig
        Figure saved in ./resources as .pdf.

    """
    times_df = pd.read_pickle(
        f"./resources/times_df_{max_processes_threads}{processes_threads}_{period}.pickle"
    )

    # Exclude first time measurement due to numba "burn-in".
    ys = [*times_df.iloc[:1].mean()]
    xs = [*range(1, max_processes_threads + 1)]

    fig, ax = plt.subplots(1, 1)
    ax.plot(xs, ys)

    ax.set_xlabel(f"Number of {processes_threads}")
    ax.set_ylabel("Microseconds")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ",")))

    if len(sys.argv) > 1 and sys.argv[1] == "show":
        plt.show()
    else:
        fig.savefig(
            f"./resources/figure_time_{max_processes_threads}"
            + f"{processes_threads}_{period}.pdf",
            bbox_inches="tight",
        )


if __name__ == "__main__":

    plot_time(SCALABILITY_ANALYSIS, MAX_THREADS_PROCESSES[SCALABILITY_ANALYSIS], PERIOD)
