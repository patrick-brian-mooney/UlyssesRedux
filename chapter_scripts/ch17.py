#!/usr/bin/env python3
"""Script to create the text generated based on the seventeenth chapter of
Joyce's Ulysses, 'Ithaca.' It relies on a simply formatted text file that summarizes
an automated analysis of 'Ithaca' performed by the script at /UlyssesRedux/
code/utility-scripts/get-chapter-17-stats.py, which classifies the paragraphs of
this chapter into two categories: questions and answers; and aims to replicate
the structure of that chapter by reproducing the same calling separate routines
that produce 'questions' and 'answers' of appropriate lengths drawn from the
separate base corpora.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

import sys
sys.path.append('/UlyssesRedux/code/')
from directory_structure import *           # Gets us the listing of file and directory locations.

sys.path.append(markov_generator_path)
from sentence_generator import *

import patrick_logger                 # From https://github.com/patrick-brian-mooney/personal-library
from patrick_logger import log_it

# First, set up constants
questions_chain_length = 1
answers_chain_length = 2

patrick_logger.verbosity_level = 0
log_it("INFO: Imports successful, moving on", 2)

# Create the necessary sets of Markov chains once, at the beginning of the script's run
questions_starts, questions_mapping = buildMapping(word_list(ithaca_questions_path), markov_length=questions_chain_length)
answers_starts, answers_mapping = buildMapping(word_list(ithaca_answers_path), markov_length=answers_chain_length)
log_it("INFO: built mappings from both question and answer files, moving on", 2)

# Unlike the 'Aeolus' script, this script makes no effort to enforce sticking within word-limit boundaries.
# You can see that in the next two routines, which just call sentence_generator.gen_text() directly.

def getQuestion(num_sents, num_words):
    log_it("    getQuestion() called", 2)
    log_it("      num_sents: %d; num_words: %d" % (num_sents, num_words), 3)
    return gen_text(questions_mapping, questions_starts, markov_length=questions_chain_length, sentences_desired=num_sents, paragraph_break_probability=0)

def getAnswer(num_sents, num_words):
    log_it("    getAnswer() called", 2)
    log_it("      num_sents: %d; num_words: %d" % (num_sents, num_words), 3)
    return gen_text(answers_mapping, answers_starts, markov_length=answers_chain_length, sentences_desired=num_sents, paragraph_break_probability=0)

def get_appropriate_paragraph(structure_description):
    """Parse the coded lines in /UlyssesRedux/stats/17-stats.csv and produce an
    appropriate paragraph in response.

    These lines have the following structure:
      * A one-character type code, one of:
        - '?', a question mark, indicating one of the questions in the
          question-and-answer pattern of 'Ithaca'; or
        - a blank space, indicating "other."
      * This is followed by a number, which is the number of sentences in the
        paragraph.
      * Then there is a comma.
      * Then there is another base-10, non-zero-padded number, which is the total
        number of words in those sentences.

    This function just parses the lines and delegates to other functions.
    """
    num_sents, num_words = tuple(structure_description[1:].split(','))
    if structure_description[0] == "?":
        return getQuestion(int(num_sents), int(num_words))
    elif structure_description[0] == " ":
        return getAnswer(int(num_sents), int(num_words))
    else:
        raise LookupError("Cannot interpret the 'Ithaca' stats file located at %s:\n    line begins with unknown character '%s'." % (ithaca_stats_path, structure_description[0].encode()))

def write_story():
    chapter_paragraphs = []
    log_it("INFO: about to start reading and processing the stats file", 2)
    with open(ithaca_stats_path) as statsfile:     # OK, parse the coded structure line
        log_it("INFO: successfully opened stats file %s." % ithaca_stats_path, 3)
        for structure_line in statsfile:
            log_it("  processing line '%s'." % structure_line.rstrip())
            chapter_paragraphs.append(get_appropriate_paragraph(structure_line))

    return'\n'.join(chapter_paragraphs)

if __name__ == "__main__":
    debugging = True
    print(write_story())
