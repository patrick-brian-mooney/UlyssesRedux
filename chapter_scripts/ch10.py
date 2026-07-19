#!/usr/bin/env python3
"""Script to create the text generated based on the tenth chapter of Joyce's
Ulysses, 'Wandering Rocks.' Currently, it iterates over the sections of
'Wandering Rocks', producing nineteen sections, each of which has the same
number of sentences as the corresponding section of Joyce's chapter; the text
used as the basis for the Markov chains in each section is not just the
corresponding section of Joyce's chapter, but also the section before and after
(wrapping around at the beginning and end).

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""


import glob
import sys
from pprint import pformat


sys.path.append('/UlyssesRedux/scripts/')
import directory_structure as ds    # Gets us the listing of file and directory locations.

sys.path.append(ds.markov_generator_path)
import text_generator as tg

from chapter_scripts.generic_chapter import train_with_mixins


verbosity = 0

chain_length = 2
sections_in_chapter = 19
mixin_texts_dir = ds.current_run_corpus_directory / '10'


def log_it(what: str,
           minimum_verbosity: int = 1) -> None:
    if verbosity >= minimum_verbosity:
        print(what)


# First, set up constants
def write_story() -> str:
    output_text = list()

    # First, set up table of filenames
    section_filenames = list()
    for which_section in range(1, 1 + sections_in_chapter):
        section_filenames.append(str(ds.wandering_rocks_sections_path / f'{which_section:02}.txt'))

    log_it("INFO: filenames table set up")
    log_it(f"  length is {len(section_filenames)}", 2)
    log_it("\n    and the filenames table is:\n" + pformat(section_filenames), 2)

    with open(ds.wandering_rocks_stats_file) as stats_file:
        _ = stats_file.readline()                   # Read and ignore the header line
        log_it("INFO: header read from stats file, about to parse stats file and start generating text")

        for which_section in range(1, 1 + sections_in_chapter):
            the_line = stats_file.readline()        # Read another line from the stats file
            log_it(f"INFO: Parsing the line '{the_line.split()}'.", 2)

            sec, pars, sents, words = map(int, the_line.split(','))
            log_it(f"    sec: {sec}; pars: {pars}; sents: {sents}; words: {words}", 2)

            if sec != which_section:        # elementary sanity check
                raise ValueError(f"The stats file for Wandering Rocks is corrupt: section "
                                 f"number {sec} encountered out of order.")

            log_it(f"    generating based on sections {1 + (which_section + 17) % 19}, "
                   f"{which_section}, {(which_section + 1) % 19}.", 2)
            log_it(f"      asking for {sents} sentences with paragraph break probability of {(pars/sents):.5f}.")

            which_rocks_sections = [section_filenames[1 + (which_section + 17) % 19 - 1],
                                    section_filenames[which_section - 1],
                                    section_filenames[(which_section + 1) % 19 - 1]]

            section_genny = tg.TextGenerator(name="Wandering Rocks generator for section %d" % which_section)
            train_with_mixins(section_genny, chain_length, which_rocks_sections, list(mixin_texts_dir.glob('*txt')))
            output_text.append(section_genny.gen_text(sentences_desired=sents, paragraph_break_probability=(pars/sents)))

    return '\n<center>*   *   *</center>\n'.join(output_text)


if __name__ == "__main__":
    verbosity = 3
    print(write_story())
