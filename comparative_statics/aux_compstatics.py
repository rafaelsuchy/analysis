"""Auxiliary functions for the comparative statics analysis."""
import matplotlib.pyplot as plt
import pandas as pd


def ambiguity_effect_experiences(dict_model_dfs):
    """Summarizes average experience under for different models.

    Parameters:
    -----------
    dict_model_dfs: dict
        Dictionary that contains a simulated models in the format
        key = ambiguity level, value = pd.DataFrame.

    Returns:
    --------
    summarized: pd.DataFrame
        Dataframe that summarizes the experience levels for each occupation
        and each ambiguity level.

    """

    _df = dict_model_dfs
    summarized = {}

    for ak in _df.keys():

        exp_bluecol = (
            _df[ak].groupby("Identifier")["Experience_Blue_Collar"].max().mean()
        )
        exp_whitecol = (
            _df[ak].groupby("Identifier")["Experience_White_Collar"].max().mean()
        )
        exp_military = _df[ak].groupby("Identifier")["Experience_Military"].max().mean()
        exp_school = _df[ak].groupby("Identifier")["Experience_School"].max().mean()

        summarized[ak] = [
            exp_bluecol,
            exp_whitecol,
            exp_military,
            exp_school,
        ]

    summarized = pd.DataFrame.from_dict(summarized, orient="index").rename(
        columns={0: "Blue", 1: "White", 2: "Military", 3: "School"}
    )

    return summarized


def plot_ambiguity_effect_choiceshare(dict_selected, al_selected, filename):
    """Summarizes average experience under for different models.

    Parameters:
    -----------
    dict_selected: dict
        Dictionary that contains a simulated models in the format
        key = ambiguity level, value = pd.DataFrame.

    al_selected: list
        List that contains keys available in "dict_selected".

    filename: str
        String attached to the saved file.

    Returns:
    --------
    summarized: pd.DataFrame
        Dataframe that summarizes the experience levels for each occupation
        and each ambiguity level.

    """

    fig, axs = plt.subplots(
        1, len(al_selected), figsize=(20, 4), sharey=True, sharex=True
    )
    axs = axs.flatten()

    for (ak, ax) in zip(al_selected, axs):
        shares = (
            dict_selected[ak]
            .groupby("Period")
            .Choice.value_counts(normalize=True)
            .unstack()[["school", "home", "blue_collar", "white_collar", "military"]]
        )

        shares.plot.bar(stacked=True, ax=ax, width=0.9, legend=True)

        ax.set_ylim(0, 1)
        ax.set_ylabel("Share of individuals")

        ax.set_xticks(range(0, 51, 5))
        ax.set_xticklabels(range(0, 51, 5), rotation="horizontal")

        handles, labels = ax.get_legend_handles_labels()
        ax.get_legend().remove()
        ax.set_title(f"Ambiguity level: {ak}.")

        _legend = fig.legend(
            handles, labels, loc="lower center", bbox_to_anchor=(0.418, 1), ncol=5
        )

    fig.savefig(
        f"fig_choice_patterns_{filename}.pdf",
        bbox_extra_artists=(_legend,),
        bbox_inches="tight",
        dpi=300,
    )
