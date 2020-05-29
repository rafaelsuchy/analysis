"""Assert values log-likelihood function under ambiguity (speed-up)"""
import os
from pathlib import Path

import numpy as np
import pytest
import respy as rp
from respy.likelihood import get_crit_func
from respy.simulate import get_simulate_func

subdir = Path(f"{os.environ['PROJECT_ROOT']}/tests/resources")


@pytest.fixture
def random_ambiguity():
    """Draw some random ambiguity values."""
    ambiguity_value_ = np.random.uniform(low=0.001, high=0.02)
    return ambiguity_value_


# Test: Assert likelihood value for different model specifications (options, params)
# Includes ambiguity for iteration i > len(model_spec_params)/2
# Reference data was generated under setting w/o speedup
def test_loglike_around_models():
    # Load model specifications and associated loglike values
    model_spec_params = np.load(
        f"{subdir}/model_spec_params.npy", allow_pickle="TRUE"
    ).item()
    model_spec_options = np.load(
        f"{subdir}/model_spec_options.npy", allow_pickle="TRUE"
    ).item()
    model_spec_loglike_values = np.load(
        f"{subdir}/loglike_values.npy", allow_pickle="TRUE"
    ).item()

    for i in range(len(model_spec_params)):
        # Initialize values of current iteration
        params = model_spec_params[str(i)]
        options = model_spec_options[str(i)]

        simulate_func = get_simulate_func(params, options)
        df = simulate_func(params)

        loglike_func = get_crit_func(
            params, options, df, return_comparison_plot_data=False
        )
        loglike = loglike_func(params)

        np.testing.assert_almost_equal(
            loglike,  # actual
            model_spec_loglike_values[str(i)],  # expected
            decimal=5,  # precision of assertion
            err_msg="Assertion error log_like_values",
            verbose=True,
        )


# Test: Assert likelihood value for different values of ambiguity and given model
# Reference data was generated under setting w/o speedup
@pytest.mark.parametrize("ambiguity", [0.00, 0.02])
def test_log_likelihood_func(ambiguity):

    params, options = rp.get_example_model("kw_94_two", with_data=False)
    options["n_periods"] = 10
    options["simulation_agents"] = 200
    options["simulation_seed"] = 999
    options["solution_seed"] = 9999

    params.loc[("eta", "eta"), "value"] = ambiguity

    simulate_func = get_simulate_func(params, options)
    df = simulate_func(params)

    loglike_func = get_crit_func(params, options, df, return_comparison_plot_data=False)
    loglike = loglike_func(params)

    assert isinstance(loglike, float)

    if ambiguity == 0.00:
        np.testing.assert_almost_equal(
            loglike,  # actual
            -78.27710283833025,  # expected
            decimal=5,  # precision of assertion
            err_msg="Assertion error log_like_values",
            verbose=True,
        )

    elif ambiguity == 0.02:
        np.testing.assert_almost_equal(
            loglike,  # actual
            -79.32695775924732,  # expected
            decimal=5,  # precision of assertion
            err_msg="Assertion error log_like_values",
            verbose=True,
        )
