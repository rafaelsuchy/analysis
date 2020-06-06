"""Plotting module for vizualization of time vs. number of threads / processes."""
import sys

import matplotlib.pyplot as plt
import pandas as pd
from config import MAX_THREADS
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import MaxNLocator

if __name__ == "__main__":

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
