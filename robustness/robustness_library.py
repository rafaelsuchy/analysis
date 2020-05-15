import os
import warnings
from pathlib import Path

import multiprocessing as mp
import numpy as np
import pandas as pd
import respy as rp

# Initialize the subdirectory path for reference to pickle files.
subdir_robustness = Path(
    f"{os.environ['PROJECT_ROOT']}/uncertainty-propagation"
)

# Set the ambiguity values that will be considered throughout the project.
AMBIGUITY_VALUES = {
    "absent": 0.00,
    "low": 0.1,
    "high": 0.2,
}

# Need to initialize this stuff in a config file (potentially)
YEARS_EDUCATION = 10
NUM_PERIODS = 40
NUM_AGENTS = 1000

# Should potentially go to an auxiliary module
def get_dict_labels(dictionary):
    """Returns the keys of a dictionary as list.

    Args:
        dictionary (dict): Arbitrary dictionary, e.g. used for parametrization.

    Returns:
        dict_labels (list): List of dicationary keys.

    """
    dict_labels = list(dictionary.keys())

    return dict_labels


# ToDo: Write a wrapper that loads the model specification

def simulation_ambiguity(ambiguity_values, model="kw_94_two"):
    """Simulate models under various levels of ambiguity (ambiguity_values).

    Args:
        ambiguity_values (dict): Dictionary with various levels of ambiguity
            to be implemented (key = name of scenario).

        model (string): Number of Keane and Wolpin model.

    Returns:
        dfs_ambiguity (list): List of pd.DataFrame objects that contain the
            simulated samples under specified ambiguity scenarios.
    """
    dfs_ambiguity = []

    for ambiguity_value in ambiguity_values.values():
        params, _ = rp.get_example_model(model, with_data=False)
        # Maybe write a wrapper for params, and just params.copy()
        params.loc[("eta", "eta"), "value"] = ambiguity_value
        params.loc[("eta", "eta"), "comment"] = "value of the ambiguity set"  # Not really necessary at all

        simulate_func = rp.get_simulate_func(params, options)
        # Debugging
        # print("Current ambiguity value:", params.loc[("eta", "eta"), "value"], ".")
        dfs_ambiguity.append(simulate(params))

    # save as pickle file
    # TODO: need to re-check syntax of this thing)
    for num in range(0, len(df_ambiguity)):
        dfs_ambiguity[num].to_pickle(subdir_robustness + f"/df_ambiguity_{num}")

    return dfs_ambiguity


# ToDo: Think how to include YEARS_EDUCATION and NUM_PERIODS in a proper way.
def eval_experiece_effect_ambiguity(ambiguity_values, dfs_ambiguity, years_education, num_periods):
    """Evaluate effects on average years of experience in certain occupations
    when ambiguity is in place.

    Args:
        ambiguity_values (dict): Dictionary with various levels of ambiguity
            to be implemented (key = name of scenario).

        dfs_ambiguity (list): List of pd.DataFrame objects that containt the
            of simulated models.

    Returns:
        df_yoe_effect_ambiguity (pd.DataFrame): Dataframe that summarizes the
            effect of ambiguity levels (from dfs_ambiguity) on years of experience.

    """
    yoe_effect_ambiguity = {}
    ambiguity_labels = get_dict_labels(ambiguity_values)

    for df, ambiguity_label in zip(dfs_ambiguity, ambiguity_labels):
        exp_edu = df.groupby("Identifier")["Experience_Edu"].max().mean()
        exp_b = df.groupby("Identifier")["Experience_B"].max().mean()  # white collar
        exp_a = df.groupby("Identifier")["Experience_A"].max().mean()  # blue collar

        yoe_effect_ambiguity[ambiguity_label] = [
            exp_edu,
            exp_b,
            exp_a,
            (years_education + num_periods) - exp_edu - exp_b - exp_a
        ]

    # Assemble data frames
    df_yoe_effect_ambiguity = pd.DataFrame.from_dict(yoe_effect_ambiguity, orient="index")
    df_yoe_effect_ambiguity.rename(
        columns={0: "School", 1: "White", 2: "Blue", 3: "Home"}
    )

    # Save data frame
    df_yoe_effect_ambiguity.to_pickle(subdir_robustness + "/df_yoe_effect_ambiguity")

    return df_yoe_effect_ambiguity


def eval_eu_loss(ambiguity_values, dfs_ambiguity, num_agents):
    """Calculate the expected utility loss that results from a setting that
    incorporates different levels of ambiguity.

    Args:
        ambiguity_values (dict): Dictionary with various levels of ambiguity
            to be implemented (key = name of scenario).

         dfs_ambiguity (list): List of pd.DataFrame objects that containt the
             of simulated models.

    Returns:
        df_EU (pd.DataFrame): Dataframe that summarizes that expected utility
            loss under the various ambiguity scenarios.
    """
    EU, EU_Loss = {}, {}
    ambiguity_labels = get_dict_labels(ambiguity_values)

    # Calculate the Expected Utility and EU loss for each ambiguity value
    # Expected utility = value function at the initial period
    for df, ambiguity_label in zip(dfs_ambiguity, ambiguity_labels):
        EU[ambiguity_label] = []
        EU_Loss[ambiguity_label] = []

    # Retrieve the last identifier within looped dataframe
    num_agents = df.index[-1][0]+1
    for i in range(0, num_agents):
        EU[ambiguity_label].append(df[index_value_func].loc[(i,0)].max())

    EU[ambiguity_label] = np.mean(EU[ambiguity_label])
    EU_Loss[ambiguity_label] = np.abs(EU[ambiguity_label] - EU["absent"])/EU["absent"]

    # Assemble data frames
    df_EU = pd.DataFrame.from_dict(EU, orient="index", columns=["EU"])
    df_EU["EU_Loss"] = pd.Series(EU_Loss)

    # Save data frame
    df_EU.to_pickle(subdir_robustness + "/df_EU")

    return df_EU


# Copied direclty from
# https://github.com/OpenSourceEconomics/ose-code-templates/blob/master/
# templates/01_embarssingly_parallel_loop/core_functions.py
def distribute_tasks(func_task, tasks, num_proc=1, is_distributed=False):
    """Distribute workload.
    This function distributes the workload using the ``multiprocessing`` or ``mpi4py`` library.
    It simply creates a pool of processes that allow to work on the tasks using shared or
    distributed memory.
    Notes
    -----
    We need to ensure that the number of processes is never larger as the number of tasks as
    otherwise the MPI implementation does not terminate properly.
    * MP Pool, see `here <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool>`_ for details
    * MPI Pool, see `here <https://mpi4py.readthedocs.io/en/stable/mpi4py.futures.html#mpipoolexecutor>`_ for details
    """
    num_proc_intern = min(len(tasks), num_proc)

    if is_distributed:
        assert "PMI_SIZE" in os.environ.keys(), "MPI environment not available."
        from mpi4py.futures import MPIPoolExecutor

        executor = MPIPoolExecutor(num_proc_intern)

    else:
        executor = mp.Pool(num_proc_intern)

    with executor as e:
        rslt = list(e.map(func_task, tasks))

    return rslt