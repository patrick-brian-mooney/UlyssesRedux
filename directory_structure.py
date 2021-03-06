#!/usr/bin/env python3
"""File that serves as a central namespace listing file locations for UlyssesRedux.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

# Basic local filesystem parameters ...
base_directory                      = "/UlyssesRedux"

current_run_directory               = '%s/current-run' % base_directory

stats_directory                     = 'stats'

scripts_directory                   = "%s/scripts" % base_directory
daily_scripts_directory             = "chapter_scripts"            # Note: NOT an absolute path. Intentionally so.
utility_scripts_directory           = '%s/utility_scripts' % scripts_directory

ulysses_chapter_titles_file         = '%s/chapter-titles.txt' % scripts_directory

corpora_directory                   = 'corpora'
ulysses_corpus_directory            = 'joyce/ulysses'

markov_generator_path               = '%s/markov_sentence_generator' % scripts_directory

daily_script_path                   = '%s/daily_script.py' % scripts_directory
postprocessing_script               = '%s/postprocess-set.py' % utility_scripts_directory

toc_fragment                        = "%s/index.html" % current_run_directory
current_run_data_path               = '%s/data.csv' % current_run_directory
temporary_tags_file                 = '%s/temporary-tags' % current_run_directory

git_repo_path                       = scripts_directory

# Paths for things in the local copy of the website
webpage_contents_directory          = '/~patrick/projects/UlyssesRedux/contents/'
meta_TOC_path                       = '%s/index.html' % webpage_contents_directory
remote_webpage_contents             = 'http://patrickbrianmooney.nfshost.com%s' % webpage_contents_directory

# Paths on other systems
github_branch_base_path             = 'https://github.com/patrick-brian-mooney/UlyssesRedux/tree/'


# Now, paths related to corpora and subcorpora for individual chapter scripts.
current_run_corpus_directory        = '%s/%s/current-run/' % (base_directory, corpora_directory)    # Files in folders named 01/, 02/, etc.
unsorted_corpus_directory           = '%s/%s/unsorted/' % (base_directory, corpora_directory)       # Files named whatever, for evaluation.

ulysses_chapters_base_path          = '%s/%s/%s' % (base_directory, corpora_directory, ulysses_corpus_directory)
telemachus_base_text_path           = '%s/01.txt' % ulysses_chapters_base_path
nestor_base_text_path               = '%s/02.txt' % ulysses_chapters_base_path
proteus_base_text_path              = '%s/03.txt' % ulysses_chapters_base_path
calypso_base_text_path              = '%s/04.txt' % ulysses_chapters_base_path
lotus_eaters_base_text_path         = '%s/05.txt' % ulysses_chapters_base_path
hades_base_text_path                = '%s/06.txt' % ulysses_chapters_base_path

aeolus_base_text_path               = '%s/07.txt' % ulysses_chapters_base_path
aeolus_headlines_path               = '%s/07/headlines.txt' % ulysses_chapters_base_path
aeolus_nonheadlines_path            = '%s/07/non-headlines.txt' % ulysses_chapters_base_path

lestrygonians_base_text_path        = '%s/08.txt' % ulysses_chapters_base_path
scylla_and_charybdis_base_text_path = '%s/09.txt' % ulysses_chapters_base_path

wandering_rocks_sections_path       = '%s/10' % ulysses_chapters_base_path
wandering_rocks_whole_chapter       = '%s/10.txt' % ulysses_chapters_base_path

sirens_base_text_path               = '%s/11.txt' % ulysses_chapters_base_path
cyclops_base_text_path              = '%s/12.txt' % ulysses_chapters_base_path
nausicaa_base_text_path             = '%s/13.txt' % ulysses_chapters_base_path
oxen_base_text_path                 = '%s/14.txt' % ulysses_chapters_base_path

circe_text_path                     = '%s/15.txt' % ulysses_chapters_base_path
circe_corpora_path                  = '%s/15/' % ulysses_chapters_base_path
circe_minor_characters_corpus       = 'MINOR CHARACTERS.txt'
circe_stage_directions_corpus       = 'STAGE DIRECTIONS.txt'

eumaeus_base_text_path              = '%s/16.txt' % ulysses_chapters_base_path

ithaca_base_text_path               = '%s/17.txt' % ulysses_chapters_base_path
ithaca_questions_path               = '%s/17/questions.txt' % ulysses_chapters_base_path
ithaca_answers_path                 = '%s/17/answers.txt' % ulysses_chapters_base_path

penelope_base_text_path             = '%s/18.txt' % ulysses_chapters_base_path


# Stats files, for those chapter scripts that use them
aeolus_stats_path                   = '%s/%s/07-stats.csv' % (base_directory, stats_directory)
wandering_rocks_stats_file          = '%s/%s/10-stats.csv' % (base_directory, stats_directory)
circe_stats_path                    = '%s/%s/15-stats.psv' % (base_directory, stats_directory)
ithaca_stats_path                   = '%s/%s/17-stats.csv' % (base_directory, stats_directory)
