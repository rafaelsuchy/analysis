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

    # Core: simulate ambiguity data frames, which are the backbone of the analysis
    # In the following the implementation from simulation_ambiguity will be done with MPI

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
