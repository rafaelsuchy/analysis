"""This script runs the robustness analysis."""

import os

# Automatic parallelism turned off
parallel_off = {
    "NUMBA_NUM_THREADS": "1",
    "OMP_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
}
os.environ.update(parallel_off)

from functool import partial
import pandas as pd
import numpy as np

from robustness_library import AMBIGUITY_VALUES
from robustness_library import get_dict_labels  # should enter module auxiliary functions
from robustness_library import simulation_ambiguity
from robustness_library import eval_experiece_effect_ambiguity
from robustness_library import eval_eu_loss
from robustness_library import distribute_tasks
# Recover path to load the pickle files
from robustness_library import subdir_robustness

# Define parameters (decide where they should go)
YEARS_EDUCATION = 10
NUM_PERIODS = 40
NUM_AGENTS = 1000

def main():

    # Load the example model
    # to do: write function for the model specifiction 
    params, options = rp.get_example_model("kw_94_two")




    # Core: simulate ambiguity data frames, which are the backbone of the analysis
    # In the following the implementation from simulation_ambiguity will be done with MPI

    # Create the tasks
    tasks = []
    for ambiguity_value in AMBIGUITY_VALUES.values():
        params, _ = rp.get_example_model("kw_94_two")
        params.loc[("eta", "eta"), "value"] = ambiguity_value
        params.loc[("eta", "eta"), "comment"] = "value of the ambiguity set"
        tasks.append(params)

    df_ambiguity = distribute_tasks(simulate, tasks)

    # Expected output: list of dataframes

    # With this list of dataframe we can perform all other tasks
    # eval_experiece_effect_ambiguity
    # eval_eu_loss

    # Minor: get different functions of all stuff

if __name__ == "__main__":
    main()




    def example_task(alpha, beta, gamma, x):
    x_ = np.array(x)
    result = alpha * (x_[1:] - x_[:-1] ** beta) ** gamma + (1 - x_[:-1]) ** gamma

    return result.sum()


if __name__ == "__main__":

    # We fix the details of our evaluation task and draw a sample of evaluation points.
    num_points, num_inputs = 300, 3

    total_draws = num_inputs * num_points
    eval_points = np.random.uniform(size=total_draws).reshape(num_points, num_inputs)

    # We partial out all function arguments that remain unchanged.
    alpha, beta, gamma = 100.0, 2.0, 3.0
    p_example_task = partial(example_task, alpha, beta, gamma)

    # We specify the amount and type of resources we have available and then start  the parallel
    # evaluation of our test function.
    num_proc, is_distributed = 3, True
    distribute_tasks(p_example_task, eval_points, num_proc, is_distributed)
