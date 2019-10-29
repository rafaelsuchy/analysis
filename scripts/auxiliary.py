"""This module contains some auxiliary functions shared across the utility scripts."""
import argparse
import difflib
import glob
import os

NOTEBOOKS_ROOT = os.environ['PROJECT_ROOT'] + '/notebooks'


def parse_arguments(description):
    """This function parses the arguments for the scripts."""
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-n", "--name", type=str, help="name of notebook", default='all',
                        dest="name")

    args = parser.parse_args()

    # We can either request a single lecture or just act on all of them. We use string matching
    # to ease workflow.
    if args.name != "all":
        request = difflib.get_close_matches(args.name, get_list_of_notebooks(), n=1, cutoff=0.1)
        if not request:
            raise AssertionError("unable to match notebook")
    else:
        request = get_list_of_notebooks()

    return request


def get_list_of_notebooks():
    cwd = os.getcwd()

    os.chdir(NOTEBOOKS_ROOT)
    notebooks = [name for name in glob.glob("*.ipynb")]
    os.chdir(cwd)

    return notebooks
