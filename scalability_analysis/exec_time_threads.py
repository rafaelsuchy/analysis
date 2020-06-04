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
        "MKL_NUM_THREADS",
    ],
    num_threads,
)

os.environ.update(update_)

import datetime
import numpy as np
from respy.solve import _full_solution

ITERATIONS = 8
MAX_THREADS = 8

if __name__ == "__main__":

    input_params = np.load(
        "robustness_inputs_kw_97_extended.npy", allow_pickle=True
    ).item()

    wages = input_params["wages"]
    nonpecs = input_params["nonpecs"]
    continuation_values = input_params["continuation_values"]
    period_draws_emax_risk = input_params["period_draws_emax_risk"]
    optim_paras = input_params["optim_paras"]

    start = datetime.datetime.now()

    for _j in range(ITERATIONS):
        calc = _full_solution(
            wages, nonpecs, continuation_values, period_draws_emax_risk, optim_paras,
        )
        print("Number of iteration:", _j)

    end = datetime.datetime.now()
    time = (end - start) / ITERATIONS

    np.save(f"./resources/time_num_threads_{num_threads}", time, allow_pickle=True)
