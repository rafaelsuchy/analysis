import sys

import matplotlib.pyplot as plt
import numpy as np
from config import MAX_THREADS
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import MaxNLocator

if __name__ == "__main__":

    print("MAX THREADS")

    ys = [
        np.load(f"./resources/time_num_threads_{i}.npy", allow_pickle=True)
        .item()
        .microseconds
        for i in range(1, MAX_THREADS + 1)
    ]
    xs = [*range(1, MAX_THREADS + 1)]

    fig, ax = plt.subplots(1, 1)
    ax.plot(xs, ys)

    ax.set_xlabel("Number of threads")
    ax.set_ylabel("Microseconds")

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ",")))

    # Save or show
    if len(sys.argv) > 1 and sys.argv[1] == "save":
        fig.savefig("./resources/time_num_threads_plot.pdf", bbox_inches="tight")
    else:
        plt.show()
