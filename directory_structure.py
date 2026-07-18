#!/usr/bin/env python3
"""File that serves as a central namespace listing file locations for UlyssesRedux.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""
from pathlib import Path

# Basic local filesystem parameters ...
base_directory                      = Path("/UlyssesRedux")

current_run_directory               = base_directory / "current-run"

stats_directory                     = base_directory / 'stats'

scripts_directory                   = base_directory / "scripts"
daily_scripts_directory             = "chapter_scripts"        # Note: NOT an absolute path. Intentionally so.  #FIXME
utility_scripts_directory           = scripts_directory / 'util'

ulysses_chapter_titles_file         = scripts_directory / 'chapter-titles.txt'

corpora_directory                   = base_directory / 'corpora'
ulysses_corpus_directory            = corpora_directory / 'joyce/ulysses'

markov_generator_path               = scripts_directory / 'markov_sentence_generator'

daily_script_path                   = scripts_directory / 'daily_script.py'
postprocessing_script               = utility_scripts_directory / 'postprocess-set.py'

toc_fragment                        = current_run_directory / "index.html"
current_run_data_path               = current_run_directory / 'data.csv'
temporary_tags_file                 = current_run_directory / 'temporary-tags'

git_repo_path                       = scripts_directory

# Paths for things in the local copy of the website
webpage_contents_directory          = Path('/~patrick/projects/UlyssesRedux/contents/')
meta_TOC_path                       = webpage_contents_directory / 'index.html'
remote_webpage_contents             = f'http://patrickbrianmooney.nfshost.com{webpage_contents_directory}'

# Paths on other systems
github_branch_base_path             = 'https://github.com/patrick-brian-mooney/UlyssesRedux/tree/'


# Now, paths related to corpora and subcorpora for individual chapter scripts.
current_run_corpus_directory        = corpora_directory / 'current-run'     # Files in folders named 01/, 02/, etc.
unsorted_corpus_directory           = corpora_directory / 'unsorted'        # Files named whatever, for evaluation.

ulysses_chapters_base_path          = ulysses_corpus_directory
telemachus_base_text_path           = ulysses_chapters_base_path / '01.txt'
nestor_base_text_path               = ulysses_chapters_base_path / '02.txt'
proteus_base_text_path              = ulysses_chapters_base_path / '03.txt'
calypso_base_text_path              = ulysses_chapters_base_path / '04.txt'
lotus_eaters_base_text_path         = ulysses_chapters_base_path / '05.txt'
hades_base_text_path                = ulysses_chapters_base_path / '06.txt'

aeolus_base_text_path               = ulysses_chapters_base_path / '07.txt'
aeolus_headlines_path               = ulysses_chapters_base_path / '07/headlines.txt'
aeolus_nonheadlines_path            = ulysses_chapters_base_path / '07/non-headlines.txt'

lestrygonians_base_text_path        = ulysses_chapters_base_path / '08.txt'
scylla_and_charybdis_base_text_path = ulysses_chapters_base_path / '09.txt'

wandering_rocks_sections_path       = ulysses_chapters_base_path / '10'
wandering_rocks_whole_chapter       = ulysses_chapters_base_path / '10.txt'

sirens_base_text_path               = ulysses_chapters_base_path / '11.txt'
cyclops_base_text_path              = ulysses_chapters_base_path / '12.txt'
nausicaa_base_text_path             = ulysses_chapters_base_path / '13.txt'
oxen_base_text_path                 = ulysses_chapters_base_path / '14.txt'

circe_corpora_path                  = ulysses_chapters_base_path / '15'
circe_text_path                     = ulysses_chapters_base_path / '15.txt'
circe_minor_characters_corpus       = circe_corpora_path / 'MINOR CHARACTERS.txt'
circe_stage_directions_corpus       = circe_corpora_path / 'STAGE DIRECTIONS.txt'

eumaeus_base_text_path              = ulysses_chapters_base_path / '16.txt'

ithaca_base_text_path               = ulysses_chapters_base_path / '17.txt'
ithaca_questions_path               = ulysses_chapters_base_path / '17/questions.txt'
ithaca_answers_path                 = ulysses_chapters_base_path / '17/answers.txt'

penelope_base_text_path             = ulysses_chapters_base_path / '18.txt'


# Stats files, for those chapter scripts that use them
aeolus_stats_path                   = stats_directory / '07-stats.csv'
wandering_rocks_stats_file          = stats_directory / '10-stats.csv'
circe_stats_path                    = stats_directory / '15-stats.psv'
ithaca_stats_path                   = stats_directory / '17-stats.csv'


# Other file locations outside of the project directory
sync_to_website_script              = Path("""/home/patrick/.scripts/sync-to-nfs.sh""")
