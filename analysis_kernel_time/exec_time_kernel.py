"""Monitoring of execution time with respect to kernel amount."""
import datetime
import multiprocessing
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import MaxNLocator
from respy.solve import _full_solution

ITERATIONS = 100_000
CORES = 8

update_ = {
    "NUMBA_NUM_THREADS": "1",
    "OMP_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
}


def plot_time_cores(max_cores, time_dict, save=True):
    """Vizualization of executation time against number of kernels.

    Parameters
    ----------
    max_cores : int
        Maximum number of cores used in the calculation.
    time_dict : dict
        Dictionary with execution time (value) per number of kernels (key).
    save : bool
        Boolean whether to save figure.

    Returns
    -------
    fig.save
    """

    plt.style.use("seaborn-dark-palette")
    fig, ax = plt.subplots(1, 1)

    xs = [*range(1, max_cores)]
    ys = [time_dict[i].microseconds for i in range(1, len(time_dict.values()) + 1)]

    ax.plot(xs, ys)

    ax.set_xlabel("Number of cores")
    ax.set_ylabel("Microseconds")

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ",")))

    if save:
        fig.savefig("speed_plot.pdf", bbox_inches="tight")


if __name__ == "__main__":

    print("UPDATE", update_)
    os.environ.update(update_)
    print("CPU using", multiprocessing.cpu_count())

    if len(sys.argv) > 1:
        ITERATIONS = int(sys.argv[1])

    input_params = np.load("robustness_inputs_kw_94_one.npy", allow_pickle=True).item()

    # Assignment
    wages = input_params["wages"]
    nonpecs = input_params["nonpecs"]
    continuation_values = input_params["continuation_values"]
    period_draws_emax_risk = input_params["period_draws_emax_risk"]
    optim_paras = input_params["optim_paras"]

    times = {}

    print("TEST")
    for i in range(1, CORES + 1):

        update_.update(
            dict.fromkeys(
                [
                    "NUMBA_NUM_THREADS",
                    "OMP_NUM_THREADS",
                    "OPENBLAS_NUM_THREADS",
                    "NUMEXPR_NUM_THREADS",
                    "MKL_NUM_THREADS",
                ],
                str(i),
            )
        )

        os.environ.update(update_)

        start = datetime.datetime.now()

        for _j in range(ITERATIONS):
            calc = _full_solution(
                wages,
                nonpecs,
                continuation_values,
                period_draws_emax_risk,
                optim_paras,
            )

        end = datetime.datetime.now()

        times[i] = (end - start) / ITERATIONS

    plot_time_cores(CORES + 1, times)
