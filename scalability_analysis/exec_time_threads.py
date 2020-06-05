"""Monitoring of execution time with respect to kernel amount."""
import os
import sys

if len(sys.argv) > 1:
    num_threads = sys.argv[1]

update_ = dict.fromkeys(
    [
        "NUMBA_NUM_THREADS",
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
        "MKL_NUM_THREADS",
    ],
    num_threads,
)

os.environ.update(update_)

import datetime
import numpy as np
from respy.solve import _full_solution
from config import ITERATIONS_THREADS
from config import MAX_THREADS
from config import INPUT_DATA_THREADS


if __name__ == "__main__":

    print("MAX THREADS", MAX_THREADS, ITERATIONS_THREADS)

    input_params = np.load(INPUT_DATA_THREADS, allow_pickle=True).item()

    wages = input_params["wages"]
    nonpecs = input_params["nonpecs"]
    continuation_values = input_params["continuation_values"]
    period_draws_emax_risk = input_params["period_draws_emax_risk"]
    optim_paras = input_params["optim_paras"]

    start = datetime.datetime.now()

    for _j in range(ITERATIONS_THREADS):
        calc = _full_solution(
            wages, nonpecs, continuation_values, period_draws_emax_risk, optim_paras,
        )
        if INPUT_DATA_THREADS == "robustness_inputs_kw_97_extended.npy":
            print("Number of iteration:", _j)

    end = datetime.datetime.now()
    time = (end - start) / ITERATIONS_THREADS

    np.save(f"./resources/time_num_threads_{num_threads}", time, allow_pickle=True)
