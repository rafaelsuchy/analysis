"""This module contains functions needed for the robustness analysis. """
import multiprocessing as mp
import os

import numpy as np
import pandas as pd
import respy as rp


def get_model_specification(
    model="kw_94_two", num_sim_agents=1000, num_periods=40, import_data=False
):
    """Get the desired model specifications from respy model.

    Args:
        model (str): Model to simulate - default "kw_94_two".

        num_sim_agents (int): Number of agents within simulation.

        num_periods (int): Number of periods that will be simulated.

        data (bool): Binary option to load data - default False (no data).

    Returns:
        params_eta (pd.DataFrame): Paramteter data frame as generated by respy
            enriched with parameter for ambiguity, eta.

        options (dict): Options used in respy (see documentation - Add link)

    """
    params, options = rp.get_example_model(model, with_data=import_data)

    # Set model options
    options["simulation_agents"] = num_sim_agents
    options["n_periods"] = num_periods

    # Set model params (including eta)
    params.loc[("eta", "eta"), "value"] = 0.00
    params.loc[("eta", "eta"), "comment"] = "value of the ambiguity set"

    return params, options


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


def eval_experience_effect_ambiguity(
    ambiguity_values, dfs_ambiguity, years_education, num_periods
):
    """Evaluate effects on average years of experience in certain occupations
    when ambiguity is in place.

    Args:
        ambiguity_values (dict): Dictionary with various levels of ambiguity
            to be implemented (key = name of scenario).

        dfs_ambiguity (list): List of pd.DataFrame objects that contain the
            of simulated models under different sizes of the ambiguity set.

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
            (years_education + num_periods) - exp_edu - exp_b - exp_a,
        ]

    # Assemble data frames
    df_yoe_effect_ambiguity = pd.DataFrame.from_dict(
        yoe_effect_ambiguity, orient="index"
    )
    df_yoe_effect_ambiguity.rename(
        columns={0: "School", 1: "White", 2: "Blue", 3: "Home"}
    )

    return df_yoe_effect_ambiguity


def eval_eu_loss(ambiguity_values, dfs_ambiguity):
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
    # KW94 specific
    index_value_func = [
        "Value_Function_A",
        "Value_Function_B",
        "Value_Function_Edu",
        "Value_Function_Home",
    ]

    # Calculate the Expected Utility and EU loss for each ambiguity value
    # Expected utility = value function at the initial period
    for df, ambiguity_label in zip(dfs_ambiguity, ambiguity_labels):
        EU[ambiguity_label] = []
        EU_Loss[ambiguity_label] = []

        # Retrieve the last identifier within looped dataframe
        for i in range(0, df.index[-1][0] + 1):
            EU[ambiguity_label].append(df[index_value_func].loc[(i, 0)].max())

        EU[ambiguity_label] = np.mean(EU[ambiguity_label])
        EU_Loss[ambiguity_label] = np.abs(
            (EU[ambiguity_label] - EU["absent"]) / EU["absent"]
        )

    # Assemble data frames
    df_EU = pd.DataFrame.from_dict(EU, orient="index", columns=["EU"])
    df_EU["EU_Loss"] = pd.Series(EU_Loss)

    return df_EU


# Distributed tasks for MPI
def distribute_tasks(func_task, tasks, num_proc=1, is_distributed=False):
    """Distribute workload.
    This function distributes the workload using the ``multiprocessing`` or ``mpi4py`` library.
    It simply creates a pool of processes that allow to work on the tasks using shared or
    distributed memory.
    Notes
    -----
    We need to ensure that the number of processes is never larger as the number of tasks as
    otherwise the MPI implementation does not terminate properly.
    * MP Pool, for details
    <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool>
    * MPI Pool, for details for details
    <https://mpi4py.readthedocs.io/en/stable/mpi4py.futures.html#mpipoolexecutor>
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
