"""Configuration for scalability analysis."""
from pathlib import Path

ITERATIONS = {"threads": 20, "processes": 20}

MAX_THREADS_PROCESSES = {"threads": 3, "processes": 2}

INPUT_DATA = Path("./resources/raw_input_data/kw_94_one_input_params.npy")
# @ [
#   Path("./resources/raw_input_data/kw_94_one_input_params.npy")
#   Path("./resources/raw_input_data/kw_97_basic_input_params.npy")
# ]

PERIOD = "per28"
# @ ["per1", "per8", "per18", "per28", "per38"] for "kw_94_one_input_params.npy"
# @ ["per1", "per8", "per18", "per28", "per38", "per48"] for "kw_97_basic_input_params.npy"
