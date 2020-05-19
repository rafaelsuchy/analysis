""" Module for plotting functions of the auxiliary notebooks """
import matplotlib.pyplot as plt


def choice_patterns(df, options):
    """
    The function plots the choice patterns for a given dataframe of simulated data.

    Input:
        df: dataframe of simulated / observed data.

        options: options dataframe from loaded model.

    Output:
        Barplot of choices in each period.
    """

    fig, ax = plt.subplots()

    shares = (
        df.groupby("Period")
        .Choice.value_counts(normalize=True)
        .unstack()[["edu", "a", "b", "home"]]
    )
    labs = ["School", "White", "Blue", "Home"]

    shares.plot.bar(stacked=True, ax=ax, width=0.8)

    ax.legend(
        labels=labs, loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=len(labs)
    )

    # x-axis options
    ax.set_xticks(range(0, options["n_periods"], 5))
    ax.set_xticklabels(range(0, options["n_periods"], 5), rotation="horizontal")

    # y-axis options
    ax.set_ylim(0, 1)
    ax.set_ylabel("Share of population")
