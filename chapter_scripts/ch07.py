#!/usr/bin/env python3
"""Script to create the text generated based on the seventh chapter of Joyce's
Ulysses, 'Aeolus.' It relies on a simply formatted text file that summarizes
an automated analysis of 'Aeolus' performed by the script at /UlyssesRedux/
scripts/utility_scripts/get-chapter-7-stats.py, which classifies the paragraphs of
this chapter into three categories: headlines, spoken phrases, and other; and
aims to replicate the structure of that chapter by reproducing the same
paragraph types, with similar lengths, in the same order.

This script does NOT simply call the generic_chapter script, though it is in
some ways very similar, and it makes me think that some refactoring of that
would be useful. Not today (6 Feb 2016), though. Currently, mixin texts are
used for non-headlines chunks only.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

# First, set up constants
headline_chain_length = 1
nonheadline_chain_length = 2
length_tolerance = 0.4      # e.g., 0.3 means the generated text can be up to 30% over or under the length of the requested text.
joyce_ratio = 1.2           # Goal ratio of Joyce to non-Joyce text in the resulting chains.

import os, glob, sys
sys.path.append('/UlyssesRedux/scripts/')
from directory_structure import *           # Gets us the listing of file and directory locations.

sys.path.append(markov_generator_path)
import text_generator as tg

import patrick_logger    # From https://github.com/patrick-brian-mooney/personal-library
from patrick_logger import log_it

patrick_logger.verbosity_level = 0
log_it("INFO: Imports successful, moving on", 2)

# Create the necessary sets of Markov chains once, at the beginning of the script's run
headlines_genny = tg.TextGenerator(name="Aeolus headlines generator")
headlines_genny.train(the_files=[aeolus_headlines_path], markov_length=headline_chain_length)

joyce_text_length = os.stat(aeolus_nonheadlines_path).st_size
mixin_texts_length = 0
articles_files = glob.glob('%s/07/*txt' % current_run_corpus_directory)
for which_file in articles_files:
    mixin_texts_length += os.stat(which_file).st_size
ratio = int(round( (mixin_texts_length / joyce_text_length) * joyce_ratio ))
articles_files = [aeolus_nonheadlines_path] * ratio + articles_files
articles_genny = tg.TextGenerator(name="Aeolus articles generator")
articles_genny.train(the_files=articles_files, markov_length=nonheadline_chain_length)

log_it("INFO: trained generators for both headlines and non-headlines files, moving on", 2)

def getParagraph(genny, num_sents, num_words):
    "Generic text-generation routine that all other text-generation routines call internally."
    minl = (1 - length_tolerance) * num_words
    maxl = (1 + length_tolerance) * num_words
    log_it("      getParagraph() called", 2)
    log_it("        num_sents: %d\n        num_words: %d\n        chain_length: %s" % (num_sents, num_words, genny.chains.markov_length), 3)
    log_it("        looking for a paragraph of %d to %d words" % (minl, maxl), 3)
    ret = ""
    while not ( minl <= len (ret.split(' ')) <= maxl ):  # Keep trying until it's within acceptable length params
        ret = genny.gen_text(sentences_desired=num_sents, paragraph_break_probability=0)
        log_it("          length of generated text is %d words / %d characters" % (len(ret.split(' ')), len(ret)), 3)
        log_it("            generated sentence was '%s'." % ret, 4)
    return ret

def getHeadline(num_sents, num_words):
    log_it("    getHeadline() called", 2)
    ret = getParagraph(headlines_genny, num_sents=num_sents, num_words=num_words).upper()
    return ret

def getNonQuoteParagraph(num_sents, num_words):
    log_it("    getNonQuoteParagraph() called", 2)
    return getParagraph(articles_genny, num_sents=num_sents, num_words=num_words)

def getQuoteParagraph(num_sents, num_words):
    log_it("    getQuoteParagraph() called", 2)
    return "―" + getNonQuoteParagraph(num_sents, num_words)

def get_appropriate_paragraph(structure_description):
    """Parse the coded lines in /UlyssesRedux/stats/07-stats.csv and produce an
    appropriate paragraph in response.

    Currently, these lines have the following structure:
      * A one-character type code, one of:
        - 'H', capitalized, indicating one of the 'headlines' common in the Aeolus
           episode;
        - an em dash, indicating the paragraph begins with a quote; or
        - a blank space, indicating "other."
      * This is followed by a number, which is the number of sentences in the
        paragraph.
      * Then there is a comma.
      * Then there is another base-10, non-zero-padded number, which is the total
        number of words in those sentences.

    This function just parses the lines in the stats file and delegates the actual
    processing to other functions.
    """
    num_sents, num_words = tuple(structure_description[1:].split(','))
    if structure_description[0] == "H":
        return getHeadline(int(num_sents), int(num_words))
    elif structure_description[0] == "—":
        return getQuoteParagraph(int(num_sents), int(num_words))
    elif structure_description[0] == " ":
        return getNonQuoteParagraph(int(num_sents), int(num_words))
    else:
        raise LookupError("Cannot interpret the Aeolus stats file located at %s:\n    line begins with unknown character '%s'." % (aeolus_stats_path, structure_description[0].encode()))

def write_story():
    chapter_paragraphs = []
    log_it("INFO: about to start reading and processing the stats file", 2)
    with open(aeolus_stats_path) as statsfile:     # OK, parse the coded structure line
        log_it("INFO: successfully opened stats file %s." % aeolus_stats_path, 3)
        for structure_line in statsfile:
            log_it("  processing line '%s'." % structure_line.rstrip())
            chapter_paragraphs.append(get_appropriate_paragraph(structure_line))
    return '\n'.join(chapter_paragraphs)

if __name__ == "__main__":
    patrick_logger.verbosity_level = 3
    print(write_story())
