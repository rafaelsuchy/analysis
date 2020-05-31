"""Assert values log-likelihood function under ambiguity (speed-up)"""
import os
from pathlib import Path

import numpy as np
import pytest
import respy as rp
from respy.likelihood import get_crit_func
from respy.simulate import get_simulate_func

SUBDIR = Path(f"{os.environ['PROJECT_ROOT']}/tests/resources")


def test_loglike_around_models():
    """Asserts likelihood values for randomly chosen model specifications.

    Ambiguity included in model specifications for i > (number_models/2).
    Reference data: no speed-up implementation.

    """
    # Load model specifications and associated loglike values
    model_spec_params = np.load(
        f"{SUBDIR}/model_spec_params.npy", allow_pickle="TRUE"
    ).item()
    model_spec_options = np.load(
        f"{SUBDIR}/model_spec_options.npy", allow_pickle="TRUE"
    ).item()
    model_spec_loglike_values = np.load(
        f"{SUBDIR}/loglike_values.npy", allow_pickle="TRUE"
    ).item()

    for i in range(len(model_spec_params)):
        params = model_spec_params[str(i)]
        options = model_spec_options[str(i)]

        simulate_func = get_simulate_func(params, options)
        df = simulate_func(params)

        loglike_func = get_crit_func(
            params, options, df, return_comparison_plot_data=False
        )
        loglike = loglike_func(params)

        np.testing.assert_almost_equal(
            loglike,
            model_spec_loglike_values[str(i)],
            decimal=5,
            err_msg="Assertion error log_like_values",
            verbose=True,
        )


@pytest.mark.parametrize("ambiguity", [0.00, 0.02])
def test_log_likelihood_func(ambiguity):
    """Asserts likelihood values for different ambiguity-levels at given model.

    Reference data: no speed-up implementation.

    """

    params, options = rp.get_example_model("kw_94_two", with_data=False)
    options["n_periods"] = 10
    options["simulation_agents"] = 200
    options["simulation_seed"] = 999
    options["solution_seed"] = 9999

    params.loc[("eta", "eta"), "value"] = ambiguity

    expected = {}
    expected[0.00] = -78.27710283833025
    expected[0.02] = -79.32695775924732

    simulate_func = get_simulate_func(params, options)
    df = simulate_func(params)

    loglike_func = get_crit_func(params, options, df, return_comparison_plot_data=False)
    loglike = loglike_func(params)

    np.testing.assert_almost_equal(
        loglike,
        expected[ambiguity],
        decimal=5,
        err_msg="Assertion error log_like_values",
        verbose=True,
    )
