#!/usr/bin/env python3
"""Miscellaneous utils for Ulysses Redux scripts
"""
import collections
import csv
import os
import re
import subprocess
import sys

from pathlib import Path
from typing import Dict, Iterable

from directory_structure import current_run_corpus_directory

sys.path.append('/UlyssesRedux/scripts/')
from directory_structure import *           # Gets us the listing of file and directory locations.


def confirm(prompt: str) -> bool:
    """Asks the question in PROMPT, and returns whether the answer begins
    (case-insensitively) with a Y.
    """
    ret = input(prompt.rstrip() + ' ').strip().casefold()
    if not ret:
        return False

    return ret[0] == 'y'


def get_current_git_branch() -> str:
    oldpath = os.getcwd()
    try:
        os.chdir(git_repo_path)
        git_output = subprocess.check_output(['git', 'symbolic-ref', '--short', 'HEAD'])
        return git_output.decode().strip()
    finally:
        os.chdir(oldpath)


def read_current_run_parameters() -> dict:
    """Read the .csv file recording parameters for the current run and return it as
    a dictionary.
    """
    with open(current_run_data_path) as current_run_data_file:
        reader = csv.reader(current_run_data_file)
        return {rows[0]:rows[1] for rows in reader}


expected_keys = {   # expect keyname -> question to ask if that keyname is missing
    "current-run-name": "What is the title of the novel that has just been written?",
    "summary": "Enter a summary description for the current novel:",
    "ch01desc": "What short description should be used for chapter 1?",
    "ch02desc": "What short description should be used for chapter 2?",
    "ch03desc": "What short description should be used for chapter 3?",
    'ch04desc': "What short description should be used for chapter 4?",
    'ch05desc': "What short description should be used for chapter 5?",
    'ch06desc': "What short description should be used for chapter 6?",
    'ch07desc': "What short description should be used for chapter 7?",
    'ch08desc': "What short description should be used for chapter 8?",
    'ch09desc': "What short description should be used for chapter 9?",
    'ch10desc': "What short description should be used for chapter 10?",
    'ch11desc': "What short description should be used for chapter 11?",
    'ch12desc': "What short description should be used for chapter 12?",
    'ch13desc': "What short description should be used for chapter 13?",
    'ch14desc': "What short description should be used for chapter 14?",
    'ch15desc': "What short description should be used for chapter 15?",
    'ch16desc': "What short description should be used for chapter 16?",
    'ch17desc': "What short description should be used for chapter 17?",
    'ch18desc': "What short description should be used for chapter 18?",
    'ch01tags': "What (comma-separated list of) tags should be used for chapter 1?",
    'ch02tags': "What (comma-separated list of) tags should be used for chapter 2?",
    'ch03tags': "What (comma-separated list of) tags should be used for chapter 3?",
    'ch04tags': "What (comma-separated list of) tags should be used for chapter 4?",
    'ch05tags': "What (comma-separated list of) tags should be used for chapter 5?",
    'ch06tags': "What (comma-separated list of) tags should be used for chapter 6?",
    'ch07tags': "What (comma-separated list of) tags should be used for chapter 7?",
    'ch08tags': "What (comma-separated list of) tags should be used for chapter 8?",
    'ch09tags': "What (comma-separated list of) tags should be used for chapter 9?",
    'ch10tags': "What (comma-separated list of) tags should be used for chapter 10?",
    'ch11tags': "What (comma-separated list of) tags should be used for chapter 11?",
    'ch12tags': "What (comma-separated list of) tags should be used for chapter 12?",
    'ch13tags': "What (comma-separated list of) tags should be used for chapter 13?",
    'ch14tags': "What (comma-separated list of) tags should be used for chapter 14?",
    'ch15tags': "What (comma-separated list of) tags should be used for chapter 15?",
    'ch16tags': "What (comma-separated list of) tags should be used for chapter 16?",
    'ch17tags': "What (comma-separated list of) tags should be used for chapter 17?",
    'ch18tags': "What (comma-separated list of) tags should be used for chapter 18?"
}


def validate_data():
    """Read in the current run parameters and make sure we have the expected data.
    Prompts for missing stuff.
    """
    current_run_data = read_current_run_parameters()
    changed_keys = False
    for which_key in list(expected_keys.keys()):
        if which_key not in current_run_data.keys():
            current_run_data[which_key] = input(expected_keys[which_key] + " ")
            changed_keys = True     # Even if it's blank, the key has been added to the dictionary.
        if changed_keys:
            if confirm("Write changed dictionary back into data file? "):
                with open(current_run_data_path, 'w') as current_run_data_file:
                    writer = csv.writer(current_run_data_file)
                    for which_key in current_run_data:
                        writer.writerow([which_key, current_run_data[which_key]])


def count_words(filename: Path) -> Dict[str, int]:
    """Return a dictionary: WORD -> count of WORD occurrences in the file.

    Calling it a WORD is oversimplifying: in fact, it's a token.
    """
    assert isinstance(filename, Path)

    ret = collections.defaultdict(int)
    with open(filename) as the_file:
        for which_line in the_file:
            for the_word in [w for w in re.findall(r"[\w%s]+|[%s]" % (tg.word_punct, tg.token_punct), which_line)]:
                ret[the_word] += 1

    return dict(ret)


def get_all_word_counts(list_of_files: Iterable[Path]):
    """Return a dictionary: FILENAME -> count_words() dictionary for FILENAME.
    """
    assert isinstance(list_of_files, Iterable)
    assert all([isinstance(i, Path) for i in list_of_files])

    dict_of_dicts = {}
    for which_file in list_of_files:
        dict_of_dicts[which_file] = count_words(which_file)
    return dict_of_dicts


def calculate_vocab_overlap(text_one: dict,
                            text_two: dict) -> float:
    """Return the fraction of the words in (dict) TEXT_ONE which are also present
    in TEXT_TWO. Note that this is not (generally) reversible:

        calculate_vocab_overlap(a, b) != calculate_vocab_overlap(b, a)

    unless A and B happen to contain vocabulary lists with the same number of items.

    Currently, this function does nothing with the frequency counts in the
    dictionary (the dictionary values); it looks only at the keys themselves.
    """
    overlap_count = 0                       # FIXME: annotate function's argument types
    for which_word in text_one.keys():
        if which_word in text_two:
            overlap_count += 1
    return overlap_count / len(text_one)


def create_comparative_dictionary(chapter_filename: Path,
                                  source_text_mappings: dict,
                                  compare_texts_mappings: dict) -> None:
    """Creates a .csv file for WHICH_CHAPTER, which contains a similarity score
    indicating how similar each text in COMPARE_TEXTS_MAPPINGS is to the text in
    SOURCE_TEXT_MAPPINGS.
    """
    assert isinstance(chapter_filename, Path)

    stats_filename = current_run_corpus_directory / chapter_filename.with_suffix('.csv')
    with open(stats_filename, "w") as the_stats_file:
        the_stats_file.write('Text name, Similarity to source text\n')      # Write a header
        the_rows = [][:]
        the_writer = csv.writer(the_stats_file)
        for which_text in compare_texts_mappings:
            text_score = calculate_vocab_overlap(source_text_mappings, compare_texts_mappings[which_text])
            the_rows.append([which_text, text_score])
        the_rows = sorted(the_rows, reverse=True, key=lambda the_row: the_row[1])     # Descending sort by similarity (second column)
        the_writer.writerows(the_rows)


if __name__ == "__main__":
    pass
