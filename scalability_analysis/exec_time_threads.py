"""Monitoring of execution time with respect to kernel amount."""
import os
import sys

if len(sys.argv) > 1:
    num_threads = sys.argv[1]

update_ = dict.fromkeys(
    [
        "NUMBA_NUM_THREADS",
        "MKL_NUM_THREADS",
        "OMP_NUM_THREADS",
        # "OPENBLAS_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
        # "VECLIB_MAXIMUM_THREADS",
    ],
    num_threads,
)


print(update_)
os.environ.update(update_)

import datetime
import numpy as np
import pandas as pd
from respy.solve import _full_solution
from config import ITERATIONS_THREADS
from config import MAX_THREADS
from config import INPUT_DATA_THREADS


if __name__ == "__main__":

    input_params = np.load(INPUT_DATA_THREADS, allow_pickle=True).item()

    wages = input_params["wages"]
    nonpecs = input_params["nonpecs"]
    continuation_values = input_params["continuation_values"]
    period_draws_emax_risk = input_params["period_draws_emax_risk"]
    optim_paras = input_params["optim_paras"]

    times = []
    for _j in range(ITERATIONS_THREADS):

        start = datetime.datetime.now()
        print(start)
        calc = _full_solution(
            wages, nonpecs, continuation_values, period_draws_emax_risk, optim_paras,
        )
        end = datetime.datetime.now()

        times.append((end - start).microseconds)

    df_times = pd.DataFrame(times, columns=[f"{num_threads}"])

    # Adding columns and saving
    if int(num_threads) > 1:
        (
            pd.read_pickle(f"./resources/times_df_threads_{MAX_THREADS}.pickle").join(
                df_times, lsuffix="_"
            )
        ).to_pickle(f"./resources/times_df_threads_{MAX_THREADS}.pickle")
    else:
        df_times.to_pickle(f"./resources/times_df_threads_{MAX_THREADS}.pickle")
