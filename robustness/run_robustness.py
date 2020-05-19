"""This script runs the robustness analysis."""
import os
from pathlib import Path

import respy as rp
from robustness_library import distribute_tasks
from robustness_library import eval_eu_loss
from robustness_library import eval_experience_effect_ambiguity
from robustness_library import get_model_specification

# Automatic parallelism turned off
parallel_off = {
    "NUMBA_NUM_THREADS": "1",
    "OMP_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
}
os.environ.update(parallel_off)

subdir_robustness = Path(f"{os.environ['PROJECT_ROOT']}/data")

# Define parameters for ambiguity set
AMBIGUITY_VALUES = {
    "absent": 0.00,
    "low": 0.01,
    "high": 0.02,
}

# Define processing parameters
YEARS_EDUCATION = 10
MODEL = "kw_94_two"
NUM_PERIODS = 40
NUM_AGENTS = 1000
SAVE = False


def main():

    # Load the example model
    params, options = get_model_specification(MODEL, NUM_AGENTS, NUM_PERIODS, False)

    # Build the simulate function with baseline ambiguity level
    simulate_func = rp.get_simulate_func(params, options)

    # Create the tasks
    tasks = []
    for ambiguity_value in AMBIGUITY_VALUES.values():
        params, _ = get_model_specification(MODEL, NUM_AGENTS, NUM_PERIODS, False)
        params.loc[("eta", "eta"), "value"] = ambiguity_value
        tasks.append(params)

    # MPI processing
    num_proc, is_distributed = 3, True
    dfs_ambiguity = distribute_tasks(simulate_func, tasks, num_proc, is_distributed)

    # Evaluate effect of ambiguity on years of experience.
    df_yoe_effect_ambiguity = eval_experience_effect_ambiguity(
        AMBIGUITY_VALUES, dfs_ambiguity, 10, NUM_PERIODS
    )

    # Evaluate expected utility loss
    df_eu_loss = eval_eu_loss(AMBIGUITY_VALUES, dfs_ambiguity)

    # Save as pickle files
    if SAVE:
        for num in range(0, len(dfs_ambiguity)):
            dfs_ambiguity[num].to_pickle(subdir_robustness / f"dfs_ambiguity_{num}.pkl")

        df_yoe_effect_ambiguity.to_pickle(
            subdir_robustness / "df_yoe_effect_ambiguity.pkl"
        )

        df_eu_loss.to_pickle(subdir_robustness / "df_EU.pkl")


if __name__ == "__main__":
    main()
