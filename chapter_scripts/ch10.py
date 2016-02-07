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

from pprint import pformat
import sys, glob
sys.path.append('/UlyssesRedux/code/')

from directory_structure import *           # Gets us the listing of file and directory locations.

sys.path.append(markov_generator_path)
from sentence_generator import *
from chapter_scripts.generic_chapter import buildMapping_withMixins

import patrick_logger # From https://github.com/patrick-brian-mooney/personal-library
from patrick_logger import log_it

patrick_logger.verbosity_level = 0

# First, set up constants
chain_length = 2
sections_in_chapter = 19
mixin_texts_dir = '%s10' % current_run_corpus_directory


def write_story():
    output_text = [][:]

    # First, set up table of filenames
    section_filenames = [][:]
    for which_section in range(1, 1 + sections_in_chapter):
        section_filenames.append('%s/%02d.txt' % (wandering_rocks_sections_path, which_section))

    log_it("INFO: filenames table set up")
    log_it("  length is %d" % len(section_filenames), 2)
    log_it("\n    and the filenames table is:\n" + pformat(section_filenames))

    stats_file = open(wandering_rocks_stats_file)
    the_line = stats_file.readline()                  # Read and ignore the header line

    log_it("INFO: header read from stats file, about to parse stats file and start generating text")

    for which_section in range(1, 1 + sections_in_chapter):
        the_line = stats_file.readline()        # Read another line from the stats file
        log_it("INFO: Parsing the line '%s'." % the_line.split(), 2)
        sec, pars, sents, words = map(int, the_line.split(','))
        log_it("    sec: %d; pars: %d; sents: %d; words: %d" % (sec, pars, sents, words), 2)
        if sec != which_section:        # elementary sanity check
            raise IndexError("The stats file for Wandering Rocks is corrupt: section number %d encountered out of order." % sec)
        log_it("    generating based on sections %d, %d, %d." % (1 + (which_section + 17) % 19, which_section, (which_section + 1) % 19), 2)
        log_it("      asking for %d sentences with paragraph break probability of %f." % (sents, pars/sents))
        
        which_rocks_sections = [
                                 section_filenames[1 + (which_section + 17) % 19 - 1],
                                 section_filenames[which_section - 1],
                                 section_filenames[(which_section + 1) % 19 - 1]
                                ]
        starts, the_mapping = buildMapping_withMixins(chain_length, which_rocks_sections, glob.glob('%s/*txt' % mixin_texts_dir))

        output_text.append(gen_text(the_mapping, starts, markov_length=chain_length, sentences_desired=sents,
                paragraph_break_probability=(pars/sents)))

    return '\n*   *   *\n'.join(output_text)

if __name__ == "__main__":
    patrick_logger.verbosity_level = 3
    print(write_story())
