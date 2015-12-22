#!/usr/bin/env python3
"""File that serves as a central namespace listing file locations for UlyssesRedux"""

# Basic local filesystem parameters ...
base_directory                      = "/UlyssesRedux/"
current_run_directory               = "current-run/"
scripts_directory                   = "code/"
daily_scripts_directory             = "chapter-scripts/"
stats_directory                     = 'stats/'
utility_scripts_directory           = 'utility-scripts/'

markov_generator_path               = '%s%smarkov-sentence-generator' % (base_directory, scripts_directory)

daily_script_path                   = '%s%sdaily-script.py' % (base_directory, scripts_directory)
postprocessing_script               = '%s%s%spostprocess-set.py' % (base_directory, scripts_directory, utility_scripts_directory)

toc_fragment                        = "%s%sindex.html" % (base_directory, current_run_directory)
current_run_data_path               = '%s%sdata.csv' % (base_directory, current_run_directory)
temporary_tags_file                 = '%s%stemporary-tags' % (base_directory, current_run_directory)

git_repo_path                       = '/home/patrick/Documents/programming/python projects/UlyssesRedux/'

# Paths for things in the local copy of the website 
webpage_contents_directory          = '/~patrick/projects/UlyssesRedux/contents/'
meta_TOC_path                       = '%sindex.html' % webpage_contents_directory

# Paths on other systems
github_branch_base_path             = 'https://github.com/patrick-brian-mooney/UlyssesRedux/tree/'


# Now, paths related to corpora and subcorpora for individual chapter scripts.
ulysses_chapters_base_path          = '/UlyssesRedux/corpora/joyce/ulysses/'

telemachus_base_text_path           = '%s01.txt' % ulysses_chapters_base_path
nestor_base_text_path               = '%s02.txt' % ulysses_chapters_base_path
proteus_base_text_path              = '%s03.txt' % ulysses_chapters_base_path
calypso_base_text_path              = '%s04.txt' % ulysses_chapters_base_path
lotus_eaters_base_text_path         = '%s05.txt' % ulysses_chapters_base_path
hades_base_text_path                = '%s06.txt' % ulysses_chapters_base_path

aeolus_base_text_path               = '%s07.txt' % ulysses_chapters_base_path
aeolus_headlines_path               = '%s07/headlines.txt' % ulysses_chapters_base_path
aeolus_nonheadlines_path            = '%s07/non-headlines.txt' % ulysses_chapters_base_path

lestrygonians_base_text_path        = '%s08.txt' % ulysses_chapters_base_path
scylla_and_charybdis_base_text_path = '%s09.txt' % ulysses_chapters_base_path

wandering_rocks_sections_path       = '%s10/' % ulysses_chapters_base_path
wandering_rocks_whole_chapter       = '%s10.txt' % ulysses_chapters_base_path

sirens_base_text_path               = '%s11.txt' % ulysses_chapters_base_path
cyclops_base_text_path              = '%s12.txt' % ulysses_chapters_base_path
nausicaa_base_text_path             = '%s13.txt' % ulysses_chapters_base_path
oxen_base_text_path                 = '%s14.txt' % ulysses_chapters_base_path

circe_text_path                     = '%s15.txt' % ulysses_chapters_base_path
circe_corpora_path                  = '%s15/' % ulysses_chapters_base_path
circe_minor_characters_corpus       = 'MINOR CHARACTERS.txt' 
circe_stage_directions_corpus       = 'STAGE DIRECTIONS.txt'

eumaeus_base_text_path              = '%s16.txt' % ulysses_chapters_base_path

ithaca_base_text_path               = '%s17.txt' % ulysses_chapters_base_path
ithaca_questions_path               = '%s17/questions.txt' % ulysses_chapters_base_path
ithaca_answers_path                 = '%s17/answers.txt' % ulysses_chapters_base_path

penelope_base_text_path             = '%s18.txt' % ulysses_chapters_base_path


# Stats files, for those chapter scripts that use them
aeolus_stats_path                   = '/UlyssesRedux/stats/07-stats.csv'
wandering_rocks_stats_file          = '/UlyssesRedux/stats/10-stats.csv'
circe_stats_path                    = '/UlyssesRedux/stats/15-stats.psv'
ithaca_stats_path                   = '/UlyssesRedux/stats/17-stats.csv'
