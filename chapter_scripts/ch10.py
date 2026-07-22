#!/usr/bin/env python3
"""Script to create the text generated based on the tenth chapter of Joyce's
Ulysses, 'Wandering Rocks.' Currently, it iterates over the sections of
'Wandering Rocks', producing nineteen sections, each of which has the same
number of sentences as the corresponding section of Joyce's chapter; the text
used as the basis for the Markov chains in each section is not just the
corresponding section of Joyce's chapter, but also the section before and after
(wrapping around at the beginning and end).

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this license.
"""


import glob
import sys

from pprint import pformat


sys.path.append('/UlyssesRedux/scripts/')
import directory_structure as ds                # listing of file and directory locations.
import util.current_run_utils as cru

sys.path.append(ds.markov_generator_path)

import text_generator as tg
from chapter_scripts.generic_chapter import train_with_mixins


cru.log_it.verbosity = 0

# First, set up constants
chain_length = 2
sections_in_chapter = 19
mixin_texts_dir = ds.current_run_corpus_directory / '10'


def write_story():
    output_text = [][:]

    # First, set up table of filenames
    section_filenames = [][:]
    for which_section in range(1, 1 + sections_in_chapter):
        section_filenames.append(ds.wandering_rocks_sections_path / f'{which_section:0>2}.txt')

    cru.log_it("INFO: filenames table set up")
    cru.log_it(f"  length is {len(section_filenames)}", 2)
    cru.log_it(f"    and the filenames table is:\n{pformat(section_filenames)}")

    stats_file = open(ds.wandering_rocks_stats_file)
    the_line = stats_file.readline()                  # Read and ignore the header line

    cru.log_it("INFO: header read from stats file, about to parse stats file and start generating text")

    for which_section in range(1, 1 + sections_in_chapter):
        the_line = stats_file.readline()        # Read another line from the stats file
        cru.log_it(f"INFO: Parsing the line '{the_line.split()}'.", 2)
        sec, pars, sents, words = map(int, the_line.split(','))
        cru.log_it(f"    sec: {sec}; pars: {pars}; sents: {sents}; words: {words}", 2)
        if sec != which_section:        # elementary sanity check
            raise IndexError(f"The Wandering Rocks stats file is corrupt: section {sec} encountered out of order.")
        cru.log_it(f"    generating based on sections {1 + (which_section + 17) % 19},"
                   f" {which_section}, {(which_section + 1) % 19}.", 2)
        cru.log_it(f"      asking for {sents} sentences with paragraph break probability of {pars/sents}.")

        which_rocks_sections = [section_filenames[1 + (which_section + 17) % 19 - 1],
                                section_filenames[which_section - 1],
                                section_filenames[(which_section + 1) % 19 - 1]]

        section_genny = tg.TextGenerator(name=f"Wandering Rocks generator for section {which_section}")
        train_with_mixins(section_genny, chain_length, which_rocks_sections, list(mixin_texts_dir.glob('*txt')))
        output_text.append(section_genny.gen_text(sentences_desired=sents, paragraph_break_probability=(pars/sents)))

    return '\n<center>*   *   *</center>\n'.join(output_text)


if __name__ == "__main__":
    cru.log_it.verbosity = 3
    print(write_story())
