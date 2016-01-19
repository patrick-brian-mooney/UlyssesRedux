#!/usr/bin/env python3
"""Script to create the text generated based on the seventh chapter of Joyce's
Ulysses, 'Aeolus.' It relies on a simply formatted text file that summarizes
an automated analysis of 'Aeolus' performed by the script at /UlyssesRedux/
code/utility_scripts/get-chapter-7-stats.py, which classifies the paragraphs of
this chapter into three categories: headlines, spoken phrases, and other; and
aims to replicate the structure of that chapter by reproducing the same
paragraph types, with similar lengths, in the same order.
"""

# First, set up constants
headline_chain_length = 1
nonheadline_chain_length = 2
length_tolerance = 0.4      # e.g., 0.3 means the generated text can be up to 30% over or under the length of the requested text.

import sys
sys.path.append('/UlyssesRedux/code/')
from directory_structure import *           # Gets us the listing of file and directory locations.

sys.path.append(markov_generator_path)
from sentence_generator import *

import patrick_logger    # From https://github.com/patrick-brian-mooney/personal-library
from patrick_logger import log_it

patrick_logger.verbosity_level = 0
log_it("INFO: Imports successful, moving on", 2)

# Create the necessary sets of Markov chains once, at the beginning of the script's run
headlines_starts, headlines_mapping = buildMapping(word_list(aeolus_headlines_path), markov_length=headline_chain_length)
nonheadlines_starts, nonheadlines_mapping = buildMapping(word_list(aeolus_nonheadlines_path), markov_length=nonheadline_chain_length)
log_it("INFO: built mappings from both headlines and non-headlines files, moving on", 2)

def getParagraph(num_sents, num_words, chain_length, mapping, starts):
    "Generic text-generation routine that all other text-generation routines call internally."
    minl = (1 - length_tolerance) * num_words
    maxl = (1 + length_tolerance) * num_words
    log_it("      getParagraph() called", 2)
    log_it("        num_sents: %d\n        num_words: %d\n        chain_length: %s" % (num_sents, num_words, chain_length), 3)
    log_it("        looking for a sentence of %d to %d words" % (minl, maxl), 3)
    ret = ""
    while not ( minl < len (ret.split(' ')) < maxl ):  # Keep trying until it's w/in acceptable length params
        ret = gen_text(mapping, starts, markov_length=chain_length, sentences_desired=num_sents, paragraph_break_probability=0)
        log_it("          length of generated text is %d words / %d characters" % (len(ret.split(' ')), len(ret)), 3)
        log_it("            generated sentence was '%s'." % ret, 4)
    return ret

def getHeadline(num_sents, num_words):
    log_it("    getHeadline() called", 2)
    ret = getParagraph(num_sents, num_words, headline_chain_length, headlines_mapping, headlines_starts).upper()
    return ret

def getNonQuoteParagraph(num_sents, num_words):
    log_it("    getNonQuoteParagraph() called", 2)
    return getParagraph(num_sents, num_words, nonheadline_chain_length, nonheadlines_mapping, nonheadlines_starts)

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

    This function just parses the lines and delegates to other functions.
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
    debugging = True
    print(write_story())
