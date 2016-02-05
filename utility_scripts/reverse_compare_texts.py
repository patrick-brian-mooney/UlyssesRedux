#!/usr/bin/env python3
"""Does the same thing as compare_texts.py, but in the opposite order: for each
/UlyssesRedux/corpora/unsorted, determines similarity ranks of each chapter of
/Ulysses/ to that text under comparison.
"""

import sys, glob

sys.path.append('/UlyssesRedux/code/')
from directory_structure import *           # Gets us the listing of file and directory locations.

import compare_texts as ct

def main():
    print('\n\n')
    if (input('Process the text files in "%s"?  ' % ulysses_corpus_directory) or "no").lower()[0] != 'y':
        print('\nRemember: set up the texts to be ranked in %s before starting this script.\n' % unsorted_corpus_directory)
        sys.exit(1)
    print('\nCounting words in each text ...', end='')
    ulysses_word_counts = ct.get_all_word_counts(glob.glob('%s/??.txt' % ulysses_chapters_base_path))
    other_texts_word_counts = ct.get_all_word_counts(glob.glob('%s/*txt' % unsorted_corpus_directory))
    print(' ... done.')
    for which_chapter in other_texts_word_counts.keys():
        print("  evaluating similarity for chapter %s ..." % which_chapter, end='')
        ct.create_comparative_dictionary(which_chapter, other_texts_word_counts[which_chapter], ulysses_word_counts)
        print(" ... done.")

if __name__ == "__main__":
    main()
