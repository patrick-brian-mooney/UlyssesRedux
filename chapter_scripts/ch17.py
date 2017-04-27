#!/usr/bin/env python3
"""Script to create the text generated based on the seventeenth chapter of
Joyce's Ulysses, 'Ithaca.' It relies on a simply formatted text file that
summarizes an automated analysis of 'Ithaca' performed by the script at
/UlyssesRedux/scripts/utility-scripts/get-chapter-17-stats.py, which classifies
the paragraphs of this chapter into two categories: questions and answers; and
aims to replicate the structure of that chapter by reproducing the same calling
separate routines that produce 'questions' and 'answers' of appropriate lengths
drawn from the separate base corpora.

This script does not simply call generic_chapter.write_generic_story(), though
it does rely on lower-level routines from that unit. Currently, mixin texts are
only mixed in to the 'answers' sections of the text, not the 'questions'
sections.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

import sys, glob
sys.path.append('/UlyssesRedux/scripts/')
from directory_structure import *           # Gets us the listing of file and directory locations.
from chapter_scripts.generic_chapter import train_with_mixins

sys.path.append(markov_generator_path)
import text_generator as tg

import patrick_logger                 # From https://github.com/patrick-brian-mooney/personal-library
from patrick_logger import log_it

# First, set up constants
questions_chain_length = 1
answers_chain_length = 2
mixin_texts_dir = '%s17' % current_run_corpus_directory

patrick_logger.verbosity_level = 0
log_it("INFO: Imports successful, moving on", 2)

# Create the necessary sets of Markov chains once, at the beginning of the script's run

questions_genny = tg.TextGenerator(name="Ithaca questions generator")
questions_genny.train([ithaca_questions_path], markov_length=questions_chain_length)

answers_genny = tg.TextGenerator(name="Ithaca answers generator")
train_with_mixins(answers_genny, joyce_text_list=[ithaca_answers_path], mixin_texts_list=glob.glob('%s/*txt' %
                  mixin_texts_dir), chain_length=answers_chain_length)




log_it("INFO: trained generators for both questions and answers; moving on ...", 2)

# Unlike the 'Aeolus' script, this script makes no effort to enforce sticking within word-limit boundaries.
# You can see that in the next two routines, which just call sentence_generator.gen_text() directly.

def getQuestion(num_sents, num_words):
    log_it("    getQuestion() called", 2)
    log_it("      num_sents: %d; num_words: %d" % (num_sents, num_words), 3)
    return questions_genny.gen_text(sentences_desired=num_sents, paragraph_break_probability=0)

def getAnswer(num_sents, num_words):
    log_it("    getAnswer() called", 2)
    log_it("      num_sents: %d; num_words: %d" % (num_sents, num_words), 3)
    return answers_genny.gen_text(sentences_desired=num_sents, paragraph_break_probability=0)

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
    patrick_logger.verbosity_level = 3
    print(write_story())
