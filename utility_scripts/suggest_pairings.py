#!/usr/bin/env python3
"""Script to make suggestions about which texts from a set to pair with particular
chapters from Ulysses. This is a first-pass attempt at doing this.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

import glob, sys, csv, os, shutil, zipfile

import compare_texts, reverse_compare_texts
sys.path.append('/UlyssesRedux/scripts/')

from directory_structure import *                           # Gets us the listing of file and directory locations.
import markov_sentence_generator.text_generator as tg

debugging = True

joyce_list = glob.glob('%s/%s/%s/??.txt' % (base_directory, corpora_directory, ulysses_corpus_directory))
compare_list = glob.glob('%s/*txt' % unsorted_corpus_directory)

def zip_folder(path, outfile):
    """Produce a zipped file of the previous run's mix-in texts.
    """
    if debugging:
        print('DEBUGGING: zip_folder() called')
        print('Outfile is %s' % outfile)
    with zipfile.ZipFile(outfile, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        if debugging: print('zipf is %s' % zipf)
        for root, dirs, files in os.walk(path):
            for which_file in files:
                if debugging: print('   archiving %s.' % os.path.join(root, which_file))
                zipf.write(os.path.join(root, which_file))

def get_mappings_dict(files_list, markov_length):
    """Get a dictionary of the Markov chains for each file in the list. The dictionary
    maps filenames to dictionaries of chains."""
    if debugging:
        print("DEBUGGING: get_mappings_dict() called")
        print("  files_list is:  %s" % files_list)
        print("  markov_length is:  %d" % markov_length)
    ret={}
    for which_text in sorted(files_list):
        if debugging: print("    Getting mappings for %s." % which_text)
        temp = tg.TextGenerator(training_texts=which_text)
        ret[which_text] = temp.chains.the_mapping
    return ret

def calculate_overlap(one, two):
    """return the percentage of chains in dictionary ONE that are also in
    dictionary TWO."""
    if debugging:
        print("DEBUGGING: calculate_overlap() called")
    overlap_count = 0
    for which_chain in one.keys():
        if which_chain in two: overlap_count += 1
    if debugging:
        print("  overlap_count is:  %d" % overlap_count)
        print("  ratio is:  %s" % (overlap_count / len(one)))
    return overlap_count / len(one)

def assign_matches(data):
    """Determine which chapters currently have the worst match percentages, and give
    those texts their preferred matches. Go through this list, assigning each text
    its preferred match from the list of remaining match texts, until each chapter
    has been assigned one companion text.
    """
    if debugging:
        print("DEBUGGING: assign_matches() called.")
    best_matches = {}
    for which_column in range(1, len(data[0])):
        the_column= [ row[which_column] for row in data ][1:]
        column_max = max(the_column)
        best_matches[which_column] = [column_max, data[1 + the_column.index(column_max)][0]]

    assignment_order = sorted(best_matches, key=lambda key:best_matches[key][0])
    for which_chapter in assignment_order:
        joyce_matches = [ row[which_chapter] for row in data ]
        best_match = joyce_matches.index(max(joyce_matches[1:]))
        print('    Moving "%s" to %s ...' % (os.path.basename(data[best_match][0]), '%s%02d/' % (current_run_corpus_directory, which_chapter)))
        shutil.move('%s%s' % (unsorted_corpus_directory, data[best_match][0]), '%s%02d/' % (current_run_corpus_directory, which_chapter))
        del(data[best_match])       # Eliminate that row; the text in question is no longer eligible

def give_matches(data):
    """Taking the matrix in DATA, just put each companion text in the folder of the
    chapter that it has the most in common with. Makes no attempt to distribute
    companion texts equally."""
    if debugging: print("DEBUGGING: give_matches() called")
    del(data[0])    # We're clearing the list. Start by dropping the header row.
    while len(data) > 0:
        which_joyce_chapter = data[0].index(max(data[0][1:]))
        print('    Moving "%s" to %s ...' % (os.path.basename(data[0][0]), '%s%02d/' % (current_run_corpus_directory, which_joyce_chapter)))
        shutil.move('%s%s' % (unsorted_corpus_directory, data[0][0]), '%s%02d/' % (current_run_corpus_directory, which_joyce_chapter))
        del(data[0])        # Delete this row before we move on to the next one.
    for which_row in range(len(data)):
        which_joyce_chapter = data[which_row].index(max(data[which_row]))

if __name__ == "__main__":
    assert len(compare_list) > 0, "ERROR: there are no files in %s" % unsorted_corpus_directory
    print("\nWARNING: About to clear out the \"%s\" directory." % current_run_corpus_directory)
    if input("Want to compress the last run's mix-in text set? ").lower().strip()[0] == 'y':
        oldpath = os.getcwd()
        os.chdir(git_repo_path)
        try:
            archive_set_name = subprocess.check_output(['git symbolic-ref --short HEAD'], shell=True).decode().split('\n')[0]
            if input ("Do you want to use the suggested name '%s.zip'? " % archive_set_name).lower()[0] != 'y':
                archive_set_name = input("What name do you want to use for the archive? ")
        except:
            archive_set_name = input("What name do you want to use for the archive? ")
        os.chdir(oldpath)
        if not archive_set_name.lower().endswith('.zip'): archive_set_name = archive_set_name + '.zip'
        zip_folder(current_run_corpus_directory, current_run_corpus_directory + archive_set_name)

    if input('\nHit ENTER when ready to delete the "%s" directory ' % current_run_corpus_directory): pass
    try:
        shutil.rmtree(current_run_corpus_directory)
    except: pass
    try:
        if not os.path.exists(current_run_corpus_directory):
            os.makedirs(current_run_corpus_directory)
        for which_chap in range(1, 19): os.mkdir('%s%02d' % (current_run_corpus_directory, which_chap))
    except Exception: pass

    if debugging: print("Directory cleared out, moving on ...")

    markov_length = 2

    ulysses_chains = get_mappings_dict(joyce_list, markov_length)
    compare_texts_chains = get_mappings_dict(compare_list, markov_length)

    if debugging: print("Chains calculated for all texts, moving on ...")

    overlap_dict = {}
    for which_joyce in joyce_list:
        overlap_dict[which_joyce] = {}
        for which_compare in compare_list:
            if debugging: print ("Calculating similarity for %s and %s ..." % (which_joyce, which_compare))
            overlap_dict[which_joyce][which_compare] = calculate_overlap(ulysses_chains[which_joyce], compare_texts_chains[which_compare]) * \
                calculate_overlap(compare_texts_chains[which_compare], ulysses_chains[which_joyce])

    with open('%s%d.csv' % (unsorted_corpus_directory, markov_length), "w") as the_stats_file:
        data = [ [' '] ]                                # First row starts with an empty cell ...
        the_writer = csv.writer(the_stats_file)
        for which_joyce in sorted(list(joyce_list)):
            data[0].append(os.path.basename(which_joyce))

        for which_compare in compare_list:
            this_row = [ os.path.basename(which_compare) ]
            for which_joyce in sorted(list(joyce_list)):
                this_row.append(overlap_dict[which_joyce][which_compare])
            data.append(this_row)

        the_writer.writerows(data)

    print("\n\nOK, let's give each chapter of Ulysses its preferred text, starting with the one")
    print("having the lowest top match and working up to the one having the best top match.\n")
    assign_matches(data)

    print("OK, each chapter from Ulysses has one matched companion text.\n\n")
    answer = ""
    while len(data) > 0 and answer.upper() != "QUIT":
        print("\n\nThere are %d remaining companion texts." % len(data[1:]))
        print("Would you like to:\n ASSIGN a round of companion texts algorithmically;\n GIVE each companion text to the chapter that most wants it;\n or QUIT?\n\n")
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
            print("Sorry, %s is not a valid option." % answer.upper())

    if debugging: print(ulysses_chains is compare_texts_chains)
