"""Core functions for template

"""
import multiprocessing as mp
import os


def distribute_tasks(func_task, tasks, num_proc=1, is_distributed=False):
    """Distribute workload.

    This function distributes the workload using the ``multiprocessing`` or ``mpi4py`` library.
    It simply creates a pool of processes that allow to work on the tasks using shared or
    distributed memory.

    Notes
    -----

    We need to ensure that the number of processes is never larger as the number of tasks as
    otherwise the MPI implementation does not terminate properly.

    * MP Pool, see `here <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool>`_ for details
    * MPI Pool, see `here <https://mpi4py.readthedocs.io/en/stable/mpi4py.futures.html#mpipoolexecutor>`_ for details

    """
    num_proc_intern = min(len(tasks), num_proc)

    if is_distributed:
        assert "PMI_SIZE" in os.environ.keys(), "MPI environment not available."
        from mpi4py.futures import MPIPoolExecutor

        executor = MPIPoolExecutor(num_proc_intern)

    else:
        executor = mp.Pool(num_proc_intern)

    with executor as e:
        rslt = list(e.map(func_task, tasks))

    return rslt
