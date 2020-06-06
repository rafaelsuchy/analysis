"""Caller for time evaluation with different number of threads."""
import subprocess
import sys
from pathlib import Path

from config import MAX_THREADS

if __name__ == "__main__":

    # Bulding time frames
    check = Path("./resources/times_df_threads_" + str(MAX_THREADS) + ".pickle")
    if not check.exists():

        for n_threads in range(1, MAX_THREADS + 1):
            call_ = "python exec_time_threads.py " + str(n_threads)
            subprocess.call(call_, shell=True)

    plot_ = "python plot_time_threads.py"
    if len(sys.argv) > 1 and sys.argv[1] == "save":
        plot_ = plot_ + " " + sys.argv[1]
    subprocess.call(plot_, shell=True)
