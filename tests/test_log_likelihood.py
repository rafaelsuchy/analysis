"""Assert values log-likelihood function under ambiguity"""
import numpy as np
import pandas as pd
import respy as rp
from pandas._testing import assert_frame_equal
from respy.likelihood import get_crit_func
from respy.simulate import get_simulate_func

# from respy.tests.utils import process_model_or_seed


# Test likelihood function for different values of ambiguity
# @pytest.mark.parametrize("ambiguity", [0, 0.02])
# def test_log_likelihood_func(ambiguity):
def test_log_likelihood_func():

    params, options = rp.get_example_model("kw_94_one", with_data=False)
    options["n_periods"] = 10
    options["simulation_agents"] = 200
    options["simulation_seed"] = 999
    options["solution_seed"] = 9999

    # params.loc[("eta", "eta"), "value"] = ambiguity
    params.loc[("eta", "eta"), "value"] = 0.00

    simulate_func = get_simulate_func(params, options)
    df = simulate_func(params)

    loglike_func = get_crit_func(params, options, df, return_comparison_plot_data=True)
    loglike, df = loglike_func(params)

    # Check for expected data format
    assert isinstance(loglike, float)
    assert isinstance(df, pd.DataFrame)

    # Test with reference simulation
    df_expected = pd.read_pickle("dfs_loglike_values_absent")
    assert_frame_equal(df_expected, df)

    log_like_values = pd.read_pickle("loglike_values")

    np.testing.assert_almost_equal(
        loglike,  # actual
        log_like_values.loc["absent", 0],  # desired
        decimal=7,
        err_msg="Assertion error log_like_values",
        verbose=True,
    )
