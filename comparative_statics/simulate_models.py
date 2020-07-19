"""Module that includes functions for model simulation."""
import pickle as pkl

import numpy as np
import respy as rp


def get_remove_name(dict_ambiguity_levels):
    """Extract name from dictionary and return cleaned dictionary.abs

    Parameters:
    -----------
    dict_ambiguity_levels: dict
        Dictionary that contains key value pairs of ambiguity levels.

    Returns:
    --------
    name: str
        Value behind name key included in passed dict_ambiguity_levels dictionary.

    _dict_ambiguity_levels: dict
        Dictionary without name key value pair.

    """

    _dict_ambiguity_levels = dict_ambiguity_levels.copy()

    if "name" in _dict_ambiguity_levels:
        name = _dict_ambiguity_levels["name"]
        del _dict_ambiguity_levels["name"]
    else:
        name = "arbitrary"

    return name, _dict_ambiguity_levels


def simulate_ambiguity_models_kw94(dict_ambiguity_levels, df_params, dict_options):
    """Simulation of KW94 models for given dictionary of ambiguity levels.

    Parameters:
    -----------
    dict_ambiguity_levels: dict
        Dictionary that contains key value pairs of ambiguity levels.

    df_params: pd.DataFrame
        Model parameters.

    dict_options: dict
        Model options.

    Returns:
    --------
    dfs_sim_amb_levels: dict
        Dictionary that contains a simulated ambiguity model (pd.DataFrame)
        for each ambiguity level specified in dict_ambiguity_levels.
        For each key a model is simulated.

    """

    _name, _dict_ambiguity_levels = get_remove_name(dict_ambiguity_levels)

    dfs_sim_amb_levels = {}

    for (av, ak) in zip(_dict_ambiguity_levels.values(), _dict_ambiguity_levels.keys()):
        params = df_params.copy()
        params.loc[("eta", "eta"), ("value", "comment")] = (av, "ambiguity parameter")
        simulate = rp.get_simulate_func(params, dict_options)
        print("Current ambiguity level:", params.loc[("eta", "eta"), "value"], ".")
        dfs_sim_amb_levels[ak] = simulate(params)

    pkl.dump(dfs_sim_amb_levels, open(f"sim_{_name}_ambiguity_models_kw94.pkl", "wb"))


def simulate_ambiguity_models_kw97(dict_ambiguity_levels, df_params, dict_options):
    """Simulation of KW97 models for given dictionary of ambiguity levels.

    Parameters:
    -----------
    dict_ambiguity_levels: dict
        Dictionary that contains key value pairs of ambiguity levels.

    df_params: pd.DataFrame
        Model parameters.

    dict_options: dict
        Model options.

    Returns:
    --------
    dfs_sim_amb_levels: dict
        Dictionary that contains a simulated ambiguity model (pd.DataFrame)
        for each ambiguity level specified in dict_ambiguity_levels.
        For each key a model is simulated.

    """

    _name, _dict_ambiguity_levels = get_remove_name(dict_ambiguity_levels)

    dfs_sim_amb_levels = {}

    for (av, ak) in zip(_dict_ambiguity_levels.values(), _dict_ambiguity_levels.keys()):
        params = df_params.copy()
        params.loc[("eta", "eta"), ("value", "comment")] = (av, "ambiguity parameter")
        simulate = rp.get_simulate_func(params, dict_options)
        print("Current ambiguity level:", params.loc[("eta", "eta"), "value"], ".")
        dfs_sim_amb_levels[ak] = simulate(params)

    pkl.dump(dfs_sim_amb_levels, open(f"sim_{_name}_ambiguity_models_kw97.pkl", "wb"))


def simulate_ambiguity_ts_models_kw94(
    dict_ambiguity_levels, list_ts, df_params, dict_options
):
    """Simulation of KW94 models for given dictionary of ambiguity levels
    and list of tuition subsidies.

    Parameters:
    -----------
    dict_ambiguity_levels: dict
        Dictionary that contains key value pairs of ambiguity levels.

    list_ts: list
        List of tuition subsidies under which a given model is simulated.

    df_params: pd.DataFrame
        Model parameters.

    dict_options: dict
        Model options.

    Returns:
    --------
    dfs_sim_amb_levels_ts: dict
        Dictionary that contains a simulated model (pd.DataFrame) for each
        ambiguity level and tuition subsidy specified in dict_ambiguity_levels.

    """

    # Retrieve name and ambiguity levels from passed dataframe
    _name, dict_ambiguity_levels = get_remove_name(dict_ambiguity_levels)

    # make repeated stuff
    _ambiguity_levels_rep = np.repeat(
        list(dict_ambiguity_levels.values()), len(list_ts)
    )
    _ambiguity_keys_rep = np.repeat(list(dict_ambiguity_levels.keys()), len(list_ts))
    _tuition_subsidies_rep = len(dict_ambiguity_levels) * list_ts

    # Populate the dictionary with ambiguity level keys
    dfs_sim_amblevels_ts = {}

    for ak in _ambiguity_keys_rep:
        dfs_sim_amblevels_ts[ak] = {}

    # Simulation
    for av, ak, ts in zip(
        _ambiguity_levels_rep, _ambiguity_keys_rep, _tuition_subsidies_rep
    ):

        params = df_params.copy()

        # add ambiguity level
        params.loc[("eta", "eta"), ("value", "comment")] = (av, "ambiguity parameter")
        # add tuition subsidy
        params.loc[("nonpec_edu", "at_least_twelve_exp_edu"), "value"] += ts

        print(
            "Current ambiguity level:",
            params.loc[("eta", "eta"), "value"],
            "and current tuition subsidy:",
            ts,
            ".",
        )
        simulate = rp.get_simulate_func(params, dict_options)
        dfs_sim_amblevels_ts[ak][str(ts)] = simulate(params)

    pkl.dump(
        dfs_sim_amblevels_ts, open(f"sim_{_name}_ambiguity_ts_models_kw94.pkl", "wb")
    )


def simulate_ambiguity_ts_models_kw97(
    dict_ambiguity_levels, list_ts, df_params, dict_options
):
    """Simulation of KW94 models for given dictionary of ambiguity levels
    and list of tuition subsidies.

    Parameters:
    -----------
    dict_ambiguity_levels: dict
        Dictionary that contains key value pairs of ambiguity levels.

    list_ts: list
        List of tuition subsidies under which a given model is simulated.

    df_params: pd.DataFrame
        Model parameters.

    dict_options: dict
        Model options.

    Returns:
    --------
    dfs_sim_amb_levels_ts: dict
        Dictionary that contains a simulated model (pd.DataFrame) for each
        ambiguity level and tuition subsidy specified in dict_ambiguity_levels.

    """

    # Retrieve name and ambiguity levels from passed dataframe
    _name, dict_ambiguity_levels = get_remove_name(dict_ambiguity_levels)

    # make repeated stuff
    _ambiguity_levels_rep = np.repeat(
        list(dict_ambiguity_levels.values()), len(list_ts)
    )
    _ambiguity_keys_rep = np.repeat(list(dict_ambiguity_levels.keys()), len(list_ts))
    _tuition_subsidies_rep = len(dict_ambiguity_levels) * list_ts

    # Populate the dictionary with ambiguity level keys
    dfs_sim_amblevels_ts = {}

    for ak in _ambiguity_keys_rep:
        dfs_sim_amblevels_ts[ak] = {}

    # Simulation
    for av, ak, ts in zip(
        _ambiguity_levels_rep, _ambiguity_keys_rep, _tuition_subsidies_rep
    ):

        params = df_params.copy()

        # add ambiguity level
        params.loc[("eta", "eta"), ("value", "comment")] = (av, "ambiguity parameter")
        # add tuition subsidy
        params.loc[("nonpec_school", "constant"), "value"] += ts

        print(
            "Current ambiguity level:",
            params.loc[("eta", "eta"), "value"],
            "and current tuition subsidy:",
            ts,
            ".",
        )
        simulate = rp.get_simulate_func(params, dict_options)
        dfs_sim_amblevels_ts[ak][str(ts)] = simulate(params)

    pkl.dump(
        dfs_sim_amblevels_ts, open(f"sim_{_name}_ambiguity_ts_models_kw97.pkl", "wb")
    )
