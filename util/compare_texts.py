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
other, it would be better to look more heavily weight words (or chains) that
appear more often, and especially those that appear often in both texts being
compared; this would provide a richer set of switchover points. At the same
time, though, it may be the case that too much weighted overlap creates a text
that's too dissonant, and so the goal might then become not maximizing the
measurement in question, but seeking the closest approximation to some ideal
value.

I'll have to play with these ideas later. One thing at a time.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""


import collections
import csv
import glob
import os
import re
import sys

from pathlib import Path
from typing import Dict, Iterable


sys.path.append('/UlyssesRedux/scripts/')
from directory_structure import *           # file and directory locations.
import util.current_run_utils as cru
import markov_sentence_generator.text_generator as tg


def count_words(f_name: Path) -> Dict[str, int]:
    """Return a dictionary: WORD -> instances of WORD in the file.

    Calling it a WORD is oversimplifying: in fact, it's a token.
    """
    assert isinstance(f_name, Path)
    ret = collections.defaultdict(int)

    with open(f_name) as the_file:
        for which_line in the_file:
            for the_word in [w for w in re.findall(r"[\w%s]+|[%s]" % (tg.word_punct, tg.token_punct), which_line)]:
                ret[the_word] += 1

    return dict(ret)


def get_all_word_counts(list_of_files: Iterable[Path]) -> Dict[Path, Dict[str, int]]:
    """Return a dictionary: FILENAME -> count_words() dictionary for FILENAME.
    """
    dict_of_dicts = dict()

    for which_file in list_of_files:
        dict_of_dicts[which_file] = count_words(which_file)

    return dict_of_dicts


def calculate_vocab_overlap(text_one: dict,
                            text_two: dict) -> float:
    """Return the fraction of the words in (dict) TEXT_ONE which are also present
    in TEXT_TWO. Note that this is not (generally) reversible:

        calculate_vocab_overlap(a, b) != calculate_vocab_overlap(b, a)

    unless A and B happen to contain vocabularly lists with the same number of items.

    Currently, this function does nothing with the frequency counts that are
    the dictionary keyphrase mappings; it looks only at the keys themselves.
    """
    overlap_count = 0

    for which_word in text_one.keys():
        if which_word in text_two: overlap_count += 1

    return overlap_count / len(text_one)


def create_comparative_dictionary(chapter_filename: Path,
                                  source_text_mappings: dict,
                                  compare_texts_mappings: dict) -> None:
    """Creates a .csv file for WHICH_CHAPTER, which contains a similarity score
    indicating how similar each text in COMPARE_TEXTS_MAPPINGS is to the text in
    SOURCE_TEXT_MAPPINGS.
    """
    assert isinstance(chapter_filename, Path)

    with open(current_run_corpus_directory / chapter_filename.with_suffix('.csv'), 'w') as the_stats_file:
        the_stats_file.write('Text name, Similarity to source text\n')      # Write a header
        the_rows = [][:]
        the_writer = csv.writer(the_stats_file)
        for which_text in compare_texts_mappings:
            text_score = calculate_vocab_overlap(source_text_mappings, compare_texts_mappings[which_text])
            the_rows.append([which_text, text_score])
        the_rows = sorted(the_rows, reverse=True, key=lambda the_row: the_row[1])     # Descending, sort by similarity
        the_writer.writerows(the_rows)


def do_compare_texts():
    print('\n\n')
    if not cru.confirm(f'Process the text files in "{unsorted_corpus_directory}"?'):
        print(f'\nSet up the texts to be ranked in {unsorted_corpus_directory} before starting this script.\n')
        sys.exit(1)

    print('\nCounting words in each text ...', end='')
    ulysses_word_counts = get_all_word_counts(ulysses_chapters_base_path.glob('??.txt'))
    other_texts_word_counts = get_all_word_counts(unsorted_corpus_directory.glob('*txt'))
    print(' ... done.')

    for which_chapter in ulysses_word_counts.keys():
        print(f"  evaluating similarity for chapter {which_chapter} ...", end='')
        create_comparative_dictionary(which_chapter, ulysses_word_counts[which_chapter], other_texts_word_counts)
        print(" ... done.")


if __name__ == "__main__":
    do_compare_texts()
