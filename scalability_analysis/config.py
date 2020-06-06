"""Configuration for scalability analysis."""
from pathlib import Path

ITERATIONS_THREADS = 100
ITERATIONS_PROCESSES = 100_000

MAX_THREADS = 2
MAX_PROCESSES = 9

INPUT_DATA_THREADS = Path("./resources/raw_input_data/kw_94_one_input_params.npy")
INPUT_DATA_PROCESSES = Path("./resources/raw_input_data/kw_94_one_input_params.npy")
# @ [
#   Path("./resources/raw_input_data/kw_94_one_input_params.npy")
#   Path("./resources/raw_input_data/kw_97_basic_input_params.npy")
# ]

PERIOD = "per38"
# @ ["per1", "per8", "per18", "per28", "per38"] for "kw_94_one_input_params.npy"
# @ ["per1", "per8", "per18", "per28", "per38", "per48"] for "kw_97_basic_input_params.npy"
