#!/usr/bin/env python3
"""Script to create the text generated based on the fifteenth chapter of
Joyce's Ulysses, 'Circe.' It runs along the structure described in the file
/UlyssesRedux/stats/15-stats.psv, which is generated by the utility script
/UlyssesRedux/scripts/utility_scripts/analyze-chapter-15.py, drawing from multiple
corpora and building a chapter that's based on those multiple corpora in an
outwardly similar form.

A Markov length of 2 seems to work well here, according to insufficient tests
evaluated informally.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this license.
"""

import glob, os, sys, pprint

sys.path.append('/UlyssesRedux/scripts/')
from directory_structure import *           # Gets us the listing of file and directory locations.

from chapter_scripts.generic_chapter import train_with_mixins

import patrick_logger
from patrick_logger import log_it

sys.path.append(markov_generator_path)
import text_generator as tg

# First, set up constants
chain_length = 2
mixin_texts_dir = '%s15' % current_run_corpus_directory
patrick_logger.verbosity_level = 0

def write_story():
    corpora = {}.copy()

    log_it("INFO: about to start processing corpora.")

    for which_corpus in sorted(glob.glob(circe_corpora_path + '*txt')):
        log_it('  INFO: processing "%s".' % which_corpus, 2)
        corpus_name = os.path.basename(which_corpus)[:-4]
        genny = tg.TextGenerator(name="%s generator" % corpus_name)
        train_with_mixins(genny, chain_length, [which_corpus], glob.glob('%s/*txt' % mixin_texts_dir))
        corpora[corpus_name] = genny

    log_it("DEBUGGING: Corpora are: \n" + pprint.pformat(corpora), 3)

    the_chapter = [][:]

    def get_speaker_text(speaker_name, num_sentences):
        if speaker_name in corpora:
            which_index = speaker_name
        elif speaker_name == 'STAGE':
            which_index = 'STAGE DIRECTIONS'
        else:
            which_index = 'MINOR CHARACTERS'
        return corpora[which_index].gen_text(sentences_desired=num_sentences, paragraph_break_probability = 0)

    log_it("INFO: About to process stats file.")

    with open(circe_stats_path) as circe_stats_file:
        for the_encoded_paragraph in circe_stats_file:
            # Process each line, using it as a map of the corresponding paragraph in 'Circe'.
            # Structure of these lines is defined in /UlyssesRedux/scripts/utility_scripts/analyze-chapter-15.py.
            # But here's a quick reminder:
            # Two parts: first, the name of a speaker (or "STAGE" if it's a paragraph of stage directions)
            # Then, a series of codes for "chunks" of the paragraph.
            # A "chunk" is a number of sentences. If the number is preceded by opening parens, it's an intraparagraph stage direction.
            # Parts of the line, and chunk descriptions, are separated by vertical bars (pipe characters), hence the .psv extension.
            log_it('INFO: Processing coded line "%s".' % the_encoded_paragraph.strip(), 2)
            code_to_process = the_encoded_paragraph.split('|')
            speaker_name = code_to_process.pop(0)
            log_it('  speaker name is "%s".' % speaker_name, 2)
            if speaker_name != 'STAGE':                         # Unless the name is 'STAGE', add it to the beginning of this paragraph
                this_paragraph = '%s: ' % speaker_name
            else:                                               # In which case, begin with an opening parenthesis.
                this_paragraph = '('
            while len(code_to_process) > 0:
                chunk_descriptor = code_to_process.pop(0)
                log_it('    processing chunk "%s".' % chunk_descriptor.strip(), 2)
                if chunk_descriptor[0] == '(':
                    this_paragraph = this_paragraph + '(%s) ' % get_speaker_text('STAGE', int(chunk_descriptor[1:])).strip()
                else:
                    this_paragraph = this_paragraph + '%s ' % (get_speaker_text(speaker_name, int(chunk_descriptor)))
                log_it('      current paragraph length is now %d.' % len(this_paragraph), 3)
            if speaker_name == 'STAGE':
                this_paragraph = this_paragraph.strip() + ')'
            log_it('        done with this paragraph; total length is %d.' % len(this_paragraph), 2)
            the_chapter.append(this_paragraph)

    return '\n'.join(the_chapter)

if __name__ == "__main__":
    patrick_logger.verbosity_level = 3
    print(write_story())
