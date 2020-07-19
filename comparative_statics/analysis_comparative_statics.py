"""Analysis functions for comparative statics."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from simulate_models import get_remove_name

initial_exp_edu_kw94 = 10


def effect_ambiguity_experiences_kw94(dict_simulated_ambiguity_models):
    """Calculation effect of ambiguity on experience in KW94 framework.

    Parameters:
    -----------
    dict_simulated_ambiguity_models: dict
        Dictionary that contains a simulated ambiguity model (pd.DataFrame)
        for various ambiguity levels.

    Returns:
    --------
    df_effect_ambiguity: pd.DataFrame
        Summary effect of ambiguity on experience.

    """

    effect_ambiguity = {}

    for ak in dict_simulated_ambiguity_models.keys():

        exp_bluecol = (
            dict_simulated_ambiguity_models[ak]
            .groupby("Identifier")["Experience_A"]
            .max()
            .mean()
        )
        exp_whitecol = (
            dict_simulated_ambiguity_models[ak]
            .groupby("Identifier")["Experience_B"]
            .max()
            .mean()
        )
        exp_school = (
            dict_simulated_ambiguity_models[ak]
            .groupby("Identifier")["Experience_Edu"]
            .max()
            .mean()
        )

        effect_ambiguity[ak] = [
            exp_bluecol,
            exp_whitecol,
            exp_school,
            (initial_exp_edu_kw94 + 40) - exp_bluecol - exp_whitecol - exp_school,
        ]

    df_effect_ambiguity = pd.DataFrame.from_dict(
        effect_ambiguity, orient="index"
    ).rename(columns={0: "Blue", 1: "White", 2: "School", 3: "Home"})

    return df_effect_ambiguity


def effect_ambiguity_experiences_kw97(
    dict_simulated_ambiguity_models, initial_schooling, n_periods
):
    """Calculation effect of ambiguity on experience in KW97 framework.

    Parameters:
    -----------
    dict_simulated_ambiguity_models: dict
        Dictionary that contains a simulated ambiguity model (pd.DataFrame)
        for various ambiguity levels.

    Returns:
    --------
    df_effect_ambiguity: pd.DataFrame
        Summary effect of ambiguity on experience.

    """

    effect_ambiguity = {}

    for ak in dict_simulated_ambiguity_models.keys():

        exp_bluecol = (
            dict_simulated_ambiguity_models[ak]
            .groupby("Identifier")["Experience_Blue_Collar"]
            .max()
            .mean()
        )
        exp_whitecol = (
            dict_simulated_ambiguity_models[ak]
            .groupby("Identifier")["Experience_White_Collar"]
            .max()
            .mean()
        )
        exp_military = (
            dict_simulated_ambiguity_models[ak]
            .groupby("Identifier")["Experience_Military"]
            .max()
            .mean()
        )
        exp_school = (
            dict_simulated_ambiguity_models[ak]
            .groupby("Identifier")["Experience_School"]
            .max()
            .mean()
        )

        effect_ambiguity[ak] = [
            exp_bluecol,
            exp_whitecol,
            exp_military,
            exp_school,
            (initial_schooling + n_periods)
            - exp_bluecol
            - exp_whitecol
            - exp_military
            - exp_school,
        ]

    df_effect_ambiguity = pd.DataFrame.from_dict(
        effect_ambiguity, orient="index"
    ).rename(columns={0: "Blue", 1: "White", 2: "Military", 3: "School", 4: "Home"})

    return df_effect_ambiguity


def plot_effect_ambiguity_choiceshare_kw94(
    dict_simulated_ambiguity_models, al_selected, filename="auxiliary"
):
    """Plotting effect of ambiguity on experience for KW94 model.

    Parameters:
    -----------
    dict_simulated_ambiguity_models: dict
        Dictionary that contains a simulated ambiguity model (pd.DataFrame)
        for various ambiguity levels.

    al_selected: list
        Selection of ambiguity levels for which the effect of ambiguity on
        experience is evaluated (based on the respective model)

    filename: str
        Extension under which plot is saved.

    Returns:
    --------
    fig: Saved figure.

    """

    fig, axs = plt.subplots(
        1, len(al_selected), figsize=(20, 4), sharey=True, sharex=False
    )
    axs = axs.flatten()

    for (ak, ax) in zip(al_selected, axs):
        shares = (
            dict_simulated_ambiguity_models[ak]
            .groupby("Period")
            .Choice.value_counts(normalize=True)
            .unstack()[["edu", "a", "b", "home"]]
        )

        shares.plot.bar(stacked=True, ax=ax, width=0.9, legend=True)

        ax.set_ylim(0, 1)
        ax.set_ylabel("Share of individuals")

        handles, labels = ax.get_legend_handles_labels()
        ax.get_legend().remove()
        ax.set_title(f"Ambiguity level: {ak}")

        _legend = fig.legend(
            handles, labels, loc="lower center", bbox_to_anchor=(0.418, 1), ncol=5
        )

        ax.set_xticks(np.arange(-0.5, 40.5, 5))
        ax.set_xticklabels(range(0, 41, 5), rotation="horizontal", ha="center")

    fig.savefig(
        f"./output/figures/fig_choice_patterns_{filename}_kw94.pdf",
        bbox_extra_artists=(_legend,),
        bbox_inches="tight",
        dpi=300,
    )


# can be summarized with plot_effect_ambiguity_choiceshare_kw94 - only change
# 1) file-name extension of KW97
# 2) "unstack list" needs adjustment
# unstack_list = ["school", "home", "blue_collar", "white_collar", "military"]
def plot_effect_ambiguity_choiceshare_kw97(
    dict_simulated_ambiguity_models, al_selected, filename
):
    """Plotting effect of ambiguity on experience for the KW97 model.

    Parameters:
    -----------
    dict_simulated_ambiguity_models: dict
        Dictionary that contains a simulated ambiguity model (pd.DataFrame)
        for various ambiguity levels.

    al_selected: list
        Selection of ambiguity levels for which the effect of ambiguity on
        experience is evaluated (based on the respective model)

    filename: str
        Extension under which plot is saved.

    Returns:
    --------
    fig: Saved figure.

    """

    fig, axs = plt.subplots(
        1, len(al_selected), figsize=(20, 4), sharey=True, sharex=False
    )
    axs = axs.flatten()

    for (ak, ax) in zip(al_selected, axs):
        shares = (
            dict_simulated_ambiguity_models[ak]
            .groupby("Period")
            .Choice.value_counts(normalize=True)
            .unstack()[["school", "home", "blue_collar", "white_collar", "military"]]
        )

        shares.plot.bar(stacked=True, ax=ax, width=0.9, legend=True)

        ax.set_ylim(0, 1)
        ax.set_ylabel("Share of individuals")

        handles, labels = ax.get_legend_handles_labels()
        ax.get_legend().remove()
        ax.set_title(f"Ambiguity level: {ak}")

        _legend = fig.legend(
            handles, labels, loc="lower center", bbox_to_anchor=(0.418, 1), ncol=5
        )

        ax.set_xticks(np.arange(-0.5, 40.5, 5))
        ax.set_xticklabels(range(0, 41, 5), rotation="horizontal", ha="center")

    fig.savefig(
        f"./output/figures/fig_choice_patterns_{filename}_kw97.pdf",
        bbox_extra_artists=(_legend,),
        bbox_inches="tight",
        dpi=300,
    )


def eu_loss_ambiguity(dict_simulated_ambiguity_models, indexes_value_func):
    """Calculating expected utility loss wrt risk-only model.

    Parameters:
    -----------
    dict_simulated_ambiguity_models: dict
        Dictionary that contains a simulated ambiguity model (pd.DataFrame)
        for various ambiguity levels.

    indexes_value_func: list
        Indexes of value functions to be considered.
        Example for KW94: ["Value_Function_A", "Value_Function_B",
                           "Value_Function_Edu", "Value_Function_Home"]

    Returns:
    --------
    df_EU: pd.DataFrame
        Summary of expected utility (absolute value) and expected utility
        loss wrt. risk-only model (percentage value)

    """

    EU_agents = {}
    EU_mean = {}
    EU_loss = {}

    for ak in dict_simulated_ambiguity_models.keys():

        EU_agents[ak] = []
        EU_mean[ak] = []
        num_agents = dict_simulated_ambiguity_models[ak].index.max()[0] + 1

        for i in range(0, num_agents):
            max_value = (
                dict_simulated_ambiguity_models[ak][indexes_value_func]
                .loc[(i, 0)]
                .max()
            )
            EU_agents[ak].append(max_value)

        EU_mean[ak] = np.mean(EU_agents[ak])
        EU_loss[ak] = np.abs(EU_mean[ak] - EU_mean["0.000"]) / EU_mean["0.000"]

    df_EU = pd.DataFrame.from_dict(EU_mean, orient="index", columns=["EU"])
    df_EU["EU_loss"] = pd.Series(EU_loss)

    return df_EU


def effect_ambiguity_ts_experiences_kw94(
    dict_ambiguity_levels, list_ts, dict_simulated_ambiguity_models
):
    """Calculation effect of ambiguity and ts on experience.

    Parameters:
    -----------
    dict_ambiguity_levels: dict
        Dictionary that contains key value pairs of ambiguity levels.

    list_ts: list
        Tuition subsidies that will be considered.

    dict_simulated_ambiguity_models: dict
        Dictionary that contains a simulated ambiguity model (pd.DataFrame)
        for various ambiguity levels.

    Returns:
    --------
    df_effect_ambiguity: pd.DataFrame
        Summary effect of ambiguity on experience.

    """

    _, _dict_ambiguity_levels = get_remove_name(dict_ambiguity_levels)

    # make repeated stuff
    # _ambiguity_levels_rep = np.repeat(
    #    list(_dict_ambiguity_levels.values()), len(list_ts)
    # )
    _ambiguity_keys_rep = np.repeat(list(_dict_ambiguity_levels.keys()), len(list_ts))
    _tuition_subsidies_rep = len(_dict_ambiguity_levels) * list_ts

    effect_tuition_subsidy = {}
    for ak in _ambiguity_keys_rep:
        effect_tuition_subsidy[ak] = {}

    for ak, ts in zip(_ambiguity_keys_rep, _tuition_subsidies_rep):

        exp_bluecol = (
            dict_simulated_ambiguity_models[ak][str(ts)]
            .groupby("Identifier")["Experience_A"]
            .max()
            .mean()
        )
        exp_whitecol = (
            dict_simulated_ambiguity_models[ak][str(ts)]
            .groupby("Identifier")["Experience_B"]
            .max()
            .mean()
        )
        exp_school = (
            dict_simulated_ambiguity_models[ak][str(ts)]
            .groupby("Identifier")["Experience_Edu"]
            .max()
            .mean()
        )

        effect_tuition_subsidy[ak][str(ts)] = {
            "Blue": exp_bluecol,
            "White": exp_whitecol,
            "School": exp_school,
            "Home": (initial_exp_edu_kw94 + 40)
            - exp_bluecol
            - exp_whitecol
            - exp_school,
        }

    df_effect_tuition_subsidy = pd.DataFrame.from_dict(
        {
            (i, j): effect_tuition_subsidy[i][j]
            for i in effect_tuition_subsidy.keys()
            for j in effect_tuition_subsidy[i].keys()
        },
        orient="index",
    )

    return df_effect_tuition_subsidy


def effect_ambiguity_ts_experiences_kw97(
    dict_ambiguity_levels,
    list_ts,
    dict_simulated_ambiguity_models,
    initial_schooling,
    n_periods,
):
    """Calculation effect of ambiguity and ts on experience for KW97 framework.

    Parameters:
    -----------
    dict_ambiguity_levels: dict
        Dictionary that contains key value pairs of ambiguity levels.

    list_ts: list
        Tuition subsidies that will be considered.

    dict_simulated_ambiguity_models: dict
        Dictionary that contains a simulated ambiguity model (pd.DataFrame)
        for various ambiguity levels.

    initial_schooling: int
        Years of completed schooling the individual enters the model.

    n_periods: int
        Total number of simulated periods.

    Returns:
    --------
    df_effect_ambiguity: pd.DataFrame
        Summary effect of ambiguity on experience.

    """

    _, _dict_ambiguity_levels = get_remove_name(dict_ambiguity_levels)

    _ambiguity_keys_rep = np.repeat(list(_dict_ambiguity_levels.keys()), len(list_ts))
    _tuition_subsidies_rep = len(_dict_ambiguity_levels) * list_ts

    effect_tuition_subsidy = {}
    for ak in _ambiguity_keys_rep:
        effect_tuition_subsidy[ak] = {}

    for ak, ts in zip(_ambiguity_keys_rep, _tuition_subsidies_rep):

        exp_bluecol = (
            dict_simulated_ambiguity_models[ak][str(ts)]
            .groupby("Identifier")["Experience_Blue_Collar"]
            .max()
            .mean()
        )
        exp_whitecol = (
            dict_simulated_ambiguity_models[ak][str(ts)]
            .groupby("Identifier")["Experience_White_Collar"]
            .max()
            .mean()
        )
        exp_military = (
            dict_simulated_ambiguity_models[ak][str(ts)]
            .groupby("Identifier")["Experience_Military"]
            .max()
            .mean()
        )
        exp_school = (
            dict_simulated_ambiguity_models[ak][str(ts)]
            .groupby("Identifier")["Experience_School"]
            .max()
            .mean()
        )

        effect_tuition_subsidy[ak][str(ts)] = {
            "Blue": exp_bluecol,
            "White": exp_whitecol,
            "Military": exp_military,
            "School": exp_school,
            "Home": (initial_schooling + n_periods)
            - exp_bluecol
            - exp_whitecol
            - exp_military
            - exp_school,
        }

    df_effect_tuition_subsidy = pd.DataFrame.from_dict(
        {
            (i, j): effect_tuition_subsidy[i][j]
            for i in effect_tuition_subsidy.keys()
            for j in effect_tuition_subsidy[i].keys()
        },
        orient="index",
    )

    return df_effect_tuition_subsidy
