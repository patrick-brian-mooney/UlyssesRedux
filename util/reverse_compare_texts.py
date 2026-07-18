#!/usr/bin/env python3
"""Does the same thing as compare_texts.py, but in the opposite order: for each
/UlyssesRedux/corpora/unsorted, determines similarity ranks of each chapter of
/Ulysses/ to that text under comparison.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

import glob
import sys

import util.current_run_utils as cru

sys.path.append('/UlyssesRedux/scripts/')
from directory_structure import *           # Gets us the listing of file and directory locations.


def do_reverse_compare():
    print('\n\n')
    if not cru.confirm(f'Process the text files in "{ulysses_corpus_directory}"?'):
        print('\nRemember: set up the texts to be ranked in %s before starting this script.\n' % unsorted_corpus_directory)
        sys.exit(1)

    print('\nCounting words in each text ...', end='')
    ulysses_word_counts = cru.get_all_word_counts(ulysses_chapters_base_path.glob('??.txt'))
    other_texts_word_counts = cru.get_all_word_counts(unsorted_corpus_directory.glob('*txt'))
    print(' ... done.')

    for which_chapter in other_texts_word_counts.keys():
        print(f"  evaluating similarity for chapter {which_chapter} ...", end='')
        cru.create_comparative_dictionary(which_chapter, other_texts_word_counts[which_chapter], ulysses_word_counts)
        print(" ... done.")


if __name__ == "__main__":
    do_reverse_compare()
