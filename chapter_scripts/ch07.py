#!/usr/bin/env python3
"""Script to create the text generated based on the seventh chapter of Joyce's
Ulysses, 'Aeolus.' It relies on a simply formatted text file that summarizes
an automated analysis of 'Aeolus' performed by the script at /UlyssesRedux/
scripts/util/get-chapter-7-stats.py, which classifies the paragraphs of
this chapter into three categories: headlines, spoken phrases, and other; and
aims to replicate the structure of that chapter by reproducing the same
paragraph types, with similar lengths, in the same order.

This script does NOT simply call the generic_chapter script, though it is in
some ways very similar, and it makes me think that some refactoring of that
would be useful. Not today (6 Feb 2016), though. Currently, mixin texts are
used for non-headlines chunks only.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this license.
"""


import os
import sys

sys.path.append('/UlyssesRedux/scripts/')
import directory_structure as ds                # listing of file and directory locations.
import util.current_run_utils as cru

import pyximport; pyximport.install()           # https://cython.org/

sys.path.append(ds.markov_generator_path)
import text_generator as tg


# First, set up constants
cru.log_it.verbosity = 0
cru.log_it("INFO: Imports successful, moving on", 2)

headline_chain_length = 1
nonheadline_chain_length = 2
length_tolerance = 0.4      # e.g., 0.3 means text can be up to +/- 30% requested length.
joyce_ratio = 1.2           # Goal ratio of Joyce to non-Joyce text in the resulting chains.

# Create the necessary sets of Markov chains once, at the beginning of the script's run
headlines_genny = tg.TextGenerator(name="Aeolus headlines generator")
headlines_genny.train(the_files=[ds.aeolus_headlines_path], markov_length=headline_chain_length)

joyce_text_length = os.stat(ds.aeolus_nonheadlines_path).st_size
mixin_texts_length = 0

articles_files = list(ds.current_run_corpus_directory.glob('07/*txt'))
for which_file in articles_files:
    mixin_texts_length += os.stat(which_file).st_size
ratio = int(round( (mixin_texts_length / joyce_text_length) * joyce_ratio ))

articles_files = [ds.aeolus_nonheadlines_path] * ratio + articles_files
articles_genny = tg.TextGenerator(name="Aeolus articles generator")
articles_genny.train(the_files=articles_files, markov_length=nonheadline_chain_length)

cru.log_it("INFO: trained generators for both headlines and non-headlines files, moving on", 2)


def get_paragraph(genny, num_sents, num_words):
    "Generic text-generation routine that all other text-generation routines call internally."
    min_len = (1 - length_tolerance) * num_words
    max_len = (1 + length_tolerance) * num_words

    cru.log_it("      get_paragraph() called", 2)
    cru.log_it(f"        num_sents: {num_sents}\n"
               f"        num_words: {num_words}\n"
               f"        chain_length: {genny.chains.markov_length}", 3)
    cru.log_it(f"        looking for a paragraph of {min_len} to {max_len} words", 3)

    ret = ""
    while not ( min_len <= len (ret.split(' ')) <= max_len ):  # Keep trying until it's within acceptable length params
        ret = genny.gen_text(sentences_desired=num_sents, paragraph_break_probability=0)
        cru.log_it(f"          length of generated text is {len(ret.split(' '))} words / {len(ret)} characters", 3)
        cru.log_it(f"            generated sentence was '{ret}'.", 4)
    return ret


def get_headline(num_sents, num_words):
    cru.log_it("    get_headline() called", 2)
    ret = get_paragraph(headlines_genny, num_sents=num_sents, num_words=num_words).upper()
    return ret


def get_non_quote_paragraph(num_sents, num_words):
    cru.log_it("    get_non_quote_paragraph() called", 2)
    return get_paragraph(articles_genny, num_sents=num_sents, num_words=num_words)


def get_quote_paragraph(num_sents, num_words):
    cru.log_it("    get_quote_paragraph() called", 2)
    return "―" + get_non_quote_paragraph(num_sents, num_words)


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
        return get_headline(int(num_sents), int(num_words))
    elif structure_description[0] == "—":
        return get_quote_paragraph(int(num_sents), int(num_words))
    elif structure_description[0] == " ":
        return get_non_quote_paragraph(int(num_sents), int(num_words))
    else:
        raise LookupError(f"Cannot interpret the Aeolus stats file located at {ds.aeolus_stats_path}:\n"
                          f"    line begins with unknown character '{structure_description[0].encode()}'.")


def write_story():
    chapter_paragraphs = []
    cru.log_it("INFO: about to start reading and processing the stats file", 2)
    with open(ds.aeolus_stats_path) as statsfile:     # OK, parse the coded structure line
        cru.log_it(f"INFO: successfully opened stats file {ds.aeolus_stats_path}.", 3)
        for structure_line in statsfile:
            cru.log_it(f"  processing line '{structure_line.rstrip()}'.")
            chapter_paragraphs.append(get_appropriate_paragraph(structure_line))
    return '\n'.join(chapter_paragraphs)


if __name__ == "__main__":
    cru.log_it.verbosity = 3
    print(write_story())
