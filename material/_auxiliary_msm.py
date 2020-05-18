"""Auxiliary functions for the MSM notebook."""
import numpy as np
import respy as rp


def calc_choice_frequencies(df):
    """Calculation of choice frequencies"""
    return df.groupby("Period").Choice.value_counts(normalize=True).unstack()


def calc_wage_distribution(df):
    """Calculation of wage distribution"""
    return df.groupby(["Period"])["Wage"].describe()[["mean", "std"]]


def get_weighting_matrix(data, calc_moments, num_boots, num_agents_msm):
    """ Compute weighting matrix for estimation with MSM."""
    # Seed for reproducibility.
    np.random.seed(123)

    index_base = data.index.get_level_values("Identifier").unique()

    # Create bootstrapped moments.
    moments_sample = []
    for _ in range(num_boots):
        ids_boot = np.random.choice(index_base, num_agents_msm, replace=False)
        moments_boot = [
            calc_moments[key](data.loc[ids_boot, :]) for key in calc_moments.keys()
        ]

        moments_boot = rp.get_flat_moments(moments_boot)

        moments_sample.append(moments_boot)

    # Compute variance for each moment and construct diagonal weighting matrix.
    moments_var = np.array(moments_sample).var(axis=0)
    weighting_matrix = np.diag(moments_var ** (-1))

    return np.nan_to_num(weighting_matrix)
