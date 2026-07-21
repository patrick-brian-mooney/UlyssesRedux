#!/usr/bin/env python3
"""Script to make suggestions about which texts from a set to pair with particular
chapters from Ulysses. This is a first-pass attempt at doing this.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this license.
"""


import csv
import glob
import os
import shutil
import subprocess
import sys
import zipfile

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union


sys.path.append('/UlyssesRedux/scripts/')
# import compare_texts                          # FIXME: eliminate this?
# import reverse_compare_texts                  # FIXME: eliminate this?

import text_generator as tg

from directory_structure import *               # listing of file and directory locations.
import util.current_run_utils as cru


debugging = True

joyce_list = list(ulysses_corpus_directory.glob('??.txt'))
compare_list = list(unsorted_corpus_directory.glob('*txt'))


def archive_dir(which_dir: Path,
                outfile: Path,
                compression_type: Optional[int] = zipfile.ZIP_DEFLATED) -> None:
    """Produce a zipped file of the previous run's mix-in texts.
    """
    assert isinstance(outfile, Path)
    assert isinstance(which_dir, Path)
    assert which_dir.is_dir()

    if debugging:
        print(f'DEBUGGING: archive_dir() called; OUTFILE is {outfile}; COMPRESSION_TYPE is {compression_type}')

    with zipfile.ZipFile(outfile, 'w', compression=compression_type) as zipf:
        if debugging:
            print(f'  ... the ZIPF object is: {zipf}; (type {type(zipf)})')

        for root, dirs, files in os.walk(which_dir):
            for which_file in files:
                if debugging:
                    print(f'  ... archiving {os.path.join(root, which_file)}.')
                zipf.write(os.path.join(root, which_file))


def get_mappings_dict(files_list: List[Path],
                      markov_length: int) -> Dict:
    """Get a dictionary of the Markov chains for each file in the list. The dictionary
    maps filenames to dictionaries of chains.
    """
    assert isinstance(files_list, list)     # FIXME: more specific return type annotation!
    assert all([isinstance(i, Path) for i in files_list])

    if debugging:
        print("DEBUGGING: get_mappings_dict() called")
        print(f"  files_list is:  {files_list}")
        print(f"  markov_length is:  {markov_length}")

    ret = dict()

    for which_text in sorted(files_list):
        if debugging: print("    Getting mappings for %s." % which_text)
        temp = tg.TextGenerator(training_texts=which_text)
        ret[which_text] = temp.chains.mapping

    return ret


def calculate_overlap(one: Dict[Tuple[str], Dict[str, float]],
                      two: Dict[Tuple[str], Dict[str, float]]) -> float:
    """return the ratio of chains in dictionary ONE that are also in
    dictionary TWO.
    """
    if debugging:
        print("\nDEBUGGING: calculate_overlap() called")

    overlap_count = 0
    for which_chain in one.keys():
        if which_chain in two:
            overlap_count += 1

    if debugging:
        print(f"  overlap_count is:  {overlap_count}")
        print(f"  ratio is:  {(overlap_count / len(one))}")

    return overlap_count / len(one)


def assign_matches(data: List[List[Union[str, float]]]) -> None:
    """Determine which chapters currently have the worst match percentages, and give
    those texts their preferred matches. Go through this list, assigning each text
    its preferred match from the list of remaining match texts, until each chapter
    has been assigned one companion text.
    """
    if debugging:       # FIXME! Crashes if there aren't 18 remaining texts.
        print("DEBUGGING: assign_matches() called.")

    best_matches = {}
    for which_column in range(1, len(data[0])):
        the_column= [row[which_column] for row in data ][1:]
        column_max = max(the_column)
        best_matches[which_column] = [column_max, data[1 + the_column.index(column_max)][0]]

    assignment_order = sorted(best_matches, key=lambda key:best_matches[key][0])
    for which_chapter in assignment_order:
        joyce_matches = [row[which_chapter] for row in data]
        best_match = joyce_matches.index(max(joyce_matches[1:]))
        move_loc = current_run_corpus_directory / f'{which_chapter:0>2}/'
        print(f'    Moving "{Path(data[best_match][0]).name}" to {move_loc} ...')
        shutil.move(unsorted_corpus_directory / data[best_match][0],
                    current_run_corpus_directory / f'{which_chapter:0>2}/')
        del(data[best_match])       # Eliminate that row; the text in question is no longer eligible


def give_matches(data) -> None:
    """Taking the matrix in DATA, just put each companion text in the folder of the
    chapter that it has the most in common with. Makes no attempt to distribute
    companion texts equally."""
    if debugging:           # FIXME: annotate parameter type
        print("DEBUGGING: give_matches() called")

    del(data[0])    # We're clearing the list. Start by dropping the header row.
    while len(data) > 0:
        which_joyce_chapter = data[0].index(max(data[0][1:]))
        move_dir = current_run_corpus_directory / f'{which_joyce_chapter:0>2}/'
        print(f'    Moving "{Path(data[0][0]).name}" to {move_dir} ...')
        shutil.move(unsorted_corpus_directory / data[0][0], move_dir)
        del(data[0])        # Delete this row before we move on to the next one.

    for which_row in range(len(data)):
        which_joyce_chapter = data[which_row].index(max(data[which_row]))       # FIXME: what is the point of this?


if __name__ == "__main__":
    assert len(compare_list) > 0, f"ERROR: there are no files in {unsorted_corpus_directory}"
    print(f'\nWARNING: About to clear out the "{current_run_corpus_directory}" directory.')

    if cru.confirm("Want to compress the last run's mix-in text set? "):
        oldpath = os.getcwd()
        os.chdir(git_repo_path)

        try:
            git_output = subprocess.check_output(['git', 'symbolic-ref', '--short', 'HEAD'])
            archive_set_name = git_output.decode().split('\n')[0]

            if not cru.confirm("Do you want to use the suggested name '%s.zip'? " % archive_set_name):
                archive_set_name = input("What name do you want to use for the archive? ").strip()

        except BaseException:
            archive_set_name = input("What name do you want to use for the archive? ")

        os.chdir(oldpath)
        if not archive_set_name.casefold().endswith('.zip'): archive_set_name = archive_set_name + '.zip'
        archive_dir(which_dir=current_run_corpus_directory,
                    outfile=(current_run_corpus_directory / archive_set_name))

    if input(f'\nHit ENTER when ready to delete the "{current_run_corpus_directory}" directory '):
        pass

    try:
        shutil.rmtree(current_run_corpus_directory)
    except Exception as errr:
        print(f'Unable to delete {current_run_corpus_directory}. The system said:{errr}')

    try:
        if not current_run_corpus_directory.is_dir():
            current_run_corpus_directory.mkdir(parents=True)
        for which_chap in range(1, 19):
            (current_run_corpus_directory / f"{which_chap:02}").mkdir(parents=True, exist_ok=True)
    except Exception as errr:
        print(f"Unable to create directories! The system said: {errr}")

    if debugging:
        print("Directory cleared out and structure validated, moving on ...")

    markov_length = 2

    joyce_chains = get_mappings_dict(joyce_list, markov_length)
    other_chains = get_mappings_dict(compare_list, markov_length)

    if debugging:
        print("Chains calculated for all texts, moving on ...")

    overlap_dict = dict()
    for which_joyce in sorted(joyce_list):
        overlap_dict[which_joyce] = dict()
        for which_compare in sorted(compare_list):
            if debugging: print (f"Calculating similarity for {which_joyce} and {which_compare} ...")
            fwd_pct = calculate_overlap(joyce_chains[which_joyce], other_chains[which_compare])
            rev_pct = calculate_overlap(other_chains[which_compare], joyce_chains[which_joyce])
            overlap_dict[which_joyce][which_compare] = fwd_pct * rev_pct

    with open(unsorted_corpus_directory / f'{markov_length}.csv', "w") as the_stats_file:
        data = [ [' '] ]                                # First row starts with an empty cell ...
        the_writer = csv.writer(the_stats_file)
        for which_joyce in sorted(list(joyce_list)):
            data[0].append(which_joyce.name)

        for which_compare in sorted(compare_list):
            this_row = [which_compare.name]
            for which_joyce in sorted(list(joyce_list)):
                this_row.append(overlap_dict[which_joyce][which_compare])
            data.append(this_row)

        the_writer.writerows(data)

    print("\n\nOK, let's give each chapter of Ulysses its preferred text, starting with the one"
          "having the lowest top match and working up to the one having the best top match.\n")
    assign_matches(data)

    print("OK, each chapter from Ulysses has one matched companion text.\n\n")
    answer = ""
    while len(data) > 0 and answer.upper() != "QUIT":
        print("\n\nThere are %d remaining companion texts." % len(data[1:]))
        print("Would you like to:\n ASSIGN a round of companion texts algorithmically;\n "
              "GIVE each companion text to the chapter that most wants it;\n or QUIT?\n\n")
        answer = ""
        while answer.upper() not in ['QUIT', 'ASSIGN', 'GIVE']:
            answer = input("Type ASSIGN, GIVE, or QUIT:  ")
        if answer.upper() == "ASSIGN":
            assign_matches(data)
        elif answer.upper() == "GIVE":
            give_matches(data)
        elif answer.upper() == "QUIT":
            sys.exit(0)
        else:
            print(f"Sorry, {answer.upper()} is not a valid option.")
