#!/usr/bin/env python3
"""Script to make suggestions about which texts from a set to pair with particular
chapters from Ulysses. This is a first-pass attempt at doing this.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

import csv, glob, sys

import compare_texts, reverse_compare_texts
sys.path.append('/UlyssesRedux/code/')
from directory_structure import *           # Gets us the listing of file and directory locations.


if __name__ == "__main__":
    print("\nWARNING: About to clear out the \"%s\" directory.\nPlease manual remove any files you'd like to keep." % current_run_corpus_directory)
    if input("Hit ENTER when ready ..."):
        pass
    
    print('\n')
    if (input("Run the compare_texts scripts first? ") or "no").lower().strip()[0] == "y":
        print("\nRunning compare_texts.py ...")
        compare_texts.main()
        print('\nRunning reverse_compare_texts.py ...')
        reverse_compare_texts.main()
    
    print("\n\nWe'll come back to suggest_pairings.py later. So far, all it's done is run its two subscripts.")