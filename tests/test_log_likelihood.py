"""Assert values log-likelihood function under ambiguity (speed-up)"""
import numpy as np
import pytest
import respy as rp
from respy.likelihood import get_crit_func
from respy.simulate import get_simulate_func


# Test likelihood function for different values of ambiguity
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
            -78.27710283833025,  # desired (w/o speedup)
            decimal=5,
            err_msg="Assertion error log_like_values",
            verbose=True,
        )

    elif ambiguity == 0.02:
        np.testing.assert_almost_equal(
            loglike,  # actual
            -79.32695775924732,  # desired (w/o speedup)
            decimal=5,
            err_msg="Assertion error log_like_values",
            verbose=True,
        )
