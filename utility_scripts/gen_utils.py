#!/usr/bin/env python3
"""Miscellaneous utils for Ulysses Redux scripts"""

import sys, csv

sys.path.append('/UlyssesRedux/code/')
from directory_structure import *           # Gets us the listing of file and directory locations.

def read_current_run_parameters():
    with open(current_run_data_path) as current_run_data_file:
        reader = csv.reader(current_run_data_file)
        return {rows[0]:rows[1] for rows in reader}

if __name__ == "__main__":
    pass
