"""Processing time of _full_solution() function of `respy` time only."""
import datetime
import multiprocessing
import sys

import numpy as np
from respy.solve import _full_solution

ITERATIONS = 100_000
CORES = multiprocessing.cpu_count()

if __name__ == "__main__":

    if len(sys.argv) > 1:
        n_processes = int(sys.argv[1])

    input_params = np.load("robustness_inputs_kw_94_one.npy", allow_pickle=True).item()

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

    end = datetime.datetime.now()

    times = (end - start) / ITERATIONS

    np.save(f"./resources/times_numproc_{n_processes}", times, allow_pickle=True)
