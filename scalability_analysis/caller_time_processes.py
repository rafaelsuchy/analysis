"""Caller for processing_time evaluation with different amount of processes."""
import subprocess

from config import MAX_PROCESSES

if __name__ == "__main__":

    for n_processes in range(1, MAX_PROCESSES + 1):

        mpiexec_ = (
            "mpiexec.hydra -n "
            + str(n_processes)
            + " -usize 3 python process_time_only.py "
            + str(n_processes)
        )
        subprocess.call(mpiexec_, shell=True)
