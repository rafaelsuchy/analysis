"""Processing time of _full_solution() function of `respy` time only."""
import datetime
import sys

import numpy as np
import pandas as pd
from caller_scalability_analysis import PATH_AUXINPUT_PARAMS
from config import ITERATIONS_PROCESSES
from config import MAX_PROCESSES
from respy.solve import _full_solution


if __name__ == "__main__":

    if len(sys.argv) > 1:
        num_processes = int(sys.argv[1])

    input_params = np.load(PATH_AUXINPUT_PARAMS, allow_pickle=True).item()

    times = []
    for _j in range(ITERATIONS_PROCESSES):

        start = datetime.datetime.now()
        calc = _full_solution(
            input_params["wages"],
            input_params["nonpecs"],
            input_params["continuation_values"],
            input_params["period_draws_emax_risk"],
            input_params["optim_paras"],
        )
        end = datetime.datetime.now()

        times.append((end - start).microseconds)

    df_times = pd.DataFrame(times, columns=[f"{num_processes}"])

    if int(num_processes) > 1:
        (
            pd.read_pickle(
                f"./resources/times_df_processes_{MAX_PROCESSES}.pickle"
            ).join(df_times, lsuffix="_")
        ).to_pickle(f"./resources/times_df_processes_{MAX_PROCESSES}.pickle")
    else:
        df_times.to_pickle(f"./resources/times_df_processes_{MAX_PROCESSES}.pickle")
