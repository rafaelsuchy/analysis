"""Plotting module for different amount of processes."""
import sys

import matplotlib.pyplot as plt
import numpy as np
from config import MAX_PROCESSES
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import MaxNLocator

if __name__ == "__main__":

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
