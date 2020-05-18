# Analysis and Exploration Robust Human Capital Investment

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This repository contains scripts for the analysis of Robust Human Capital Analysis.

## Structure

- [`run_robustness.py`](https://github.com/structRobustness/analysis/blob/rafaelsuchy_scripts/robustness/run_robustness.py) executes the pre-defined analysis.
- [`robustness_library.py`](https://github.com/structRobustness/analysis/blob/rafaelsuchy_scripts/robustness/robustness_library.py) contains functions to evaluate the effects no, low, and high ambiguity on years of experience in a certain occupation and expected utility loss.

## Making it work

Execute the following commands (within current working directory [robustness](https://github.com/structRobustness/analysis/tree/rafaelsuchy_scripts/robustness))

- `$ mpiexec -n 1 -usize 3 python run_robustness.py`
for Ubuntu / Windows user
- `$ mpiexec.hydra -n 1 -usize 3 python run_robustness.py`
MacOS user
