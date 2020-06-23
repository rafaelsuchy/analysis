"""Configurationd for scalability analysis."""
from pathlib import Path

ITERATIONS = {"threads": 1_000, "processes": 1_000}

MAX_THREADS_PROCESSES = {"threads": 12, "processes": 12}

INPUT_DATA = Path("./resources/raw_input_data/kw_94_one_input_params.pickle")
# @[
#   Path("./resources/raw_input_data/kw_94_one_input_params.pickle")
#   Path("./resources/raw_input_data/kw_97_basic_one_input_params.pickle")
#   Path("./resources/raw_input_data/kw_97_basic_two_input_params.pickle")
# ]
DATA_FORMAT = "pickle"
# @["pickle", "npy"]

PERIOD = "per28"
# @["per1", "per8", "per18", "per28", "per38"] for "kw_94_one_input_params.pickle"
# for "kw_97_basic_one_input_params.pickle"
# @["per1", "per8", "per18", "per28", "per38", "per48"]
# for "kw_97_basic_two_input_params.pickle"
# @["per1", "per8", "per18", "per28", "per38", "per48"]
