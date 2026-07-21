#!/usr/bin/env python3
"""Scans through a set of texts in /UlyssesRedux/corpora/unsorted, attempting to
evaluate their comparative similarity to the chapters of Joyce's /Ulysses/,
which are stored in /UlyssesRedux/corpora/joyce/ulysses/. Currently (3 Feb
2016), the criterion is "percentage of words in the chapter in question of
/Ulysses/ which also appear in the other text in question." However, this is
not obviously the best method, and in fact is very probably not the best method
possible, and this methodology is still very much in flux.

FUTURE PLANS: "vocabulary overlap" should probably be replaced with "percentage
overlap in the Markov chains at a given length." After all, vocabulary words
are just Markov chains with a length of one, which is not what the UlyssesRedux
scripts actually use to generate text; vocabulary is currently just a proxy for
something more complex.

Too, rather than just looking at what percentage of words overlap with each
other, it would be better to more heavily weight words (or chains) that
appear more often, and especially those that appear often in both texts being
compared; this would provide a richer set of switchover points. At the same
time, though, it may be the case that too much weighted overlap creates a text
that's too dissonant, and so the goal might then become not maximizing the
measurement in question, but seeking the closest approximation to some ideal
value.

I'll have to play with these ideas later. One thing at a time.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this license.
"""

import glob
import sys


sys.path.append('/UlyssesRedux/scripts/')
from directory_structure import *           # Gets us the listing of file and directory locations.
import util.current_run_utils as cru


def do_compare_texts() -> None:
    print('\n\n')
    if not cru.confirm(f'Process the text files in "{unsorted_corpus_directory}"?'):
        print(f'\nSet up the texts to be ranked in {unsorted_corpus_directory} before starting this script.\n')
        sys.exit(1)

    print('\nCounting words in each text ...', end='')
    ulysses_word_counts = cru.get_all_word_counts(ulysses_chapters_base_path.glob('??.txt'))
    other_texts_word_counts = cru.get_all_word_counts(unsorted_corpus_directory.glob('*txt'))
    print(' ... done.')

    for which_chapter in ulysses_word_counts.keys():
        print("  evaluating similarity for chapter %s ..." % which_chapter, end='')
        cru.create_comparative_dictionary(which_chapter, ulysses_word_counts[which_chapter], other_texts_word_counts)
        print(" ... done.")


if __name__ == "__main__":
    do_compare_texts()
