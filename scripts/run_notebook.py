#!/usr/bin/env python
"""This module executes all notebooks. It serves the main purpose to ensure that all can be
executed and work proper independently."""
import glob
import os
import subprocess as sp

from auxiliary import NOTEBOOKS_ROOT
from auxiliary import parse_arguments


def run_notebook(notebook):
    cmd = f" jupyter nbconvert --execute {notebook}  --ExecutePreprocessor.timeout=-1"
    sp.check_call(cmd, shell=True)


if __name__ == "__main__":

    request = parse_arguments("Execute notebook")
    os.chdir(NOTEBOOKS_ROOT)

    for fname in glob.glob("*.ipynb"):
        run_notebook(fname)
