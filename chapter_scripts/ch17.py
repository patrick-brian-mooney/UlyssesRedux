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
version. See the file LICENSE.md for a copy of this license.
"""


import glob
import sys

sys.path.append('/UlyssesRedux/scripts/')
import directory_structure as ds                # listing of file and directory locations.
from chapter_scripts.generic_chapter import train_with_mixins
import util.current_run_utils as cru


sys.path.append(ds.markov_generator_path)
import text_generator as tg


# First, set up constants
questions_chain_length = 1
answers_chain_length = 2
mixin_texts_dir = ds.current_run_corpus_directory / '17'

cru.log_it.verbosity = 0
cru.log_it("INFO: Imports successful, moving on", 2)

# Create the necessary sets of Markov chains once, at the beginning of the script's run

questions_genny = tg.TextGenerator(name="Ithaca questions generator")
questions_genny.train([ds.ithaca_questions_path], markov_length=questions_chain_length)

answers_genny = tg.TextGenerator(name="Ithaca answers generator")
train_with_mixins(answers_genny, joyce_text_list=[ds.ithaca_answers_path],
                  mixin_texts_list=list(mixin_texts_dir.glob('*txt')), chain_length=answers_chain_length)

cru.log_it("INFO: trained generators for both questions and answers; moving on ...", 2)

# Unlike the 'Aeolus' script, this script makes no effort to enforce sticking within word-limit boundaries.
# You can see that in the next two routines, which just call sentence_generator.gen_text() directly.


def get_question(num_sents: int,
                 num_words: int):
    cru.log_it("    get_question() called", 2)
    cru.log_it(f"      num_sents: {num_sents}; num_words: {num_words}", 3)
    return questions_genny.gen_text(sentences_desired=num_sents, paragraph_break_probability=0)


def get_answer(num_sents: int,
               num_words: int):
    cru.log_it("    get_answer() called", 2)
    cru.log_it(f"      num_sents: {num_sents}; num_words: {num_words}", 3)
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
        return get_question(int(num_sents), int(num_words))
    elif structure_description[0] == " ":
        return get_answer(int(num_sents), int(num_words))
    else:
        raise LookupError(f"Cannot interpret the 'Ithaca' stats file located at {ds.ithaca_stats_path}:\n"
                          f"    line begins with unknown character {structure_description[0].encode()}s'.")


def write_story():
    chapter_paragraphs = []
    cru.log_it("INFO: about to start reading and processing the stats file", 2)
    with open(ds.ithaca_stats_path) as statsfile:     # OK, parse the coded structure line
        cru.log_it(f"INFO: successfully opened stats file {ds.ithaca_stats_path}.", 3)
        for structure_line in statsfile:
            cru.log_it(f"  processing line '{structure_line.rstrip()}'.")
            chapter_paragraphs.append(get_appropriate_paragraph(structure_line))

    return '\n'.join(chapter_paragraphs)


if __name__ == "__main__":
    cru.log_it.verbosity = 3
    print(write_story())
