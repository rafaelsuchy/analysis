"""Run simulation for ambiguity and tuition subsidy models."""
import pandas as pd
import respy as rp
from dicts_ambiguity_levels import vdense_ambiguity_levels
from simulate_models import simulate_ambiguity_models_kw94
from simulate_models import simulate_ambiguity_models_kw97
from simulate_models import simulate_ambiguity_ts_models_kw94
from simulate_models import simulate_ambiguity_ts_models_kw97

# from dicts_ambiguity_levels import dense_ambiguity_levels
# from dicts_ambiguity_levels import spread_ambiguity_levels

# WHICH_MODELS = ["kw_94_two", "kw_97_basic"]
WHICH_MODELS = ["kw_97_basic"]
# WHICH_AMBIGUITIES = [vdense_ambiguity_levels, dense_ambiguity_levels, spread_ambiguity_levels]
WHICH_AMBIGUITIES = [vdense_ambiguity_levels]
NUM_AGENTS = 1000
TUITION_SUBSIDIES = [0, 1000]

for model in WHICH_MODELS:
    for ambiguities in WHICH_AMBIGUITIES:

        if model.split("_")[1] == str(94):

            params, options = rp.get_example_model(model, with_data=False)
            options["simulation_agents"] = NUM_AGENTS

            simulate_ambiguity_models_kw94(ambiguities, params, options)
            simulate_ambiguity_ts_models_kw94(
                ambiguities, TUITION_SUBSIDIES, params, options
            )

        if model.split("_")[1] == str(97):

            _, options = rp.get_example_model("kw_97_basic", with_data=False)
            options["simulation_agents"] = NUM_AGENTS
            params = pd.read_pickle("params_revised_basic.pkl")

            simulate_ambiguity_models_kw97(ambiguities, params, options)
            simulate_ambiguity_ts_models_kw97(
                ambiguities, TUITION_SUBSIDIES, params, options
            )
