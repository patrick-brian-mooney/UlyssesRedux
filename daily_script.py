#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to call modules that generate the blog's content, then posts that
content to the ulyssesredux.tumblr.com.

Each chapter is written by a different script that resides in the
chapter_scripts/ directory. Each of these scripts then draw from
texts in the corpora/ directory.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

import datetime
import html
import importlib
import math
import re

import sys
sys.path.append('/UlyssesRedux/scripts/')

from directory_structure import *           # Gets us the listing of file and directory locations.
import utility_scripts.current_run_data_utils as cr_data

import patrick_logger, introspection       # From https://github.com/patrick-brian-mooney/personal-library
from introspection import dump_str
from patrick_logger import log_it

import social_media         # From https://github.com/patrick-brian-mooney/personal-library
from social_media_auth import ulysses_client


recurring_tags = ['Ulysses (novel)', 'James Joyce', '1922', 'automatically generated text', 'Patrick Mooney']
ulysses_chapters = open(ulysses_chapter_titles_file).readlines()

patrick_logger.verbosity_level = 3

# First, set up parameters.
blog_url = 'http://ulyssesredux.tumblr.com/'

# Some utility routines
def out_of_content_warning():
    """Remind me that we're out of content."""
    log_it("WARNING: There's work to be done! You have to reset the blog state on ulyssesredux.tumblr.com to get it working again! A full Ulysses project is done and needs to be cleared!")
    log_it("    REMINDER: make this a more prominent warning!")  # FIXME
    sys.exit(2)


if __name__ == "__main__":
    current_run_data = cr_data.read_current_run_parameters()

    try:
        with open('%s/index.html' % current_run_directory, 'r') as index_file :
            the_lines = index_file.readlines()
            which_script = 1 + len(the_lines)   # If so far we've got, say, six lines in the file, we need to run script #7.
    except (FileNotFoundError,):
        which_script = 1
        the_lines = [][:]

    if which_script not in range(1,19):
        out_of_content_warning()

    # Post parameters
    the_title = ulysses_chapters[ which_script - 1 ].strip()
    recurring_tags.append(the_title)

    current_chapter_temporary_tags = current_run_data['ch%02dtags' % which_script]
    temporary_tags = [l.strip() for l in open('%s/temporary-tags' % current_run_directory).readlines()]
    the_tags = ', '.join(recurring_tags + temporary_tags) + ', ' + current_chapter_temporary_tags

    script_path = '%s.ch%02d' % (daily_scripts_directory, which_script)

    print("INFO: About to run script %s.py." % script_path)

    # OK, import the relevant chapter script as a module and write the story.
    the_script = importlib.import_module(script_path)
    the_content = the_script.write_story()
    print("content generated ...\n\n  ... postprocessing...")

    content_lines = the_content.split("\n")
    # Now, split the first paragraph into sentences, keeping the final punctuation and joining it back to the end of the sentence.
    first_sentence = ''.join(list(filter(None, re.split("([!?.]+)", content_lines[0])))[0:2])       # We'll use this as the summary in the table of contents.
    content_lines = [ "<p>" + the_line.strip() + "</p>" for the_line in content_lines if len(the_line.strip()) > 0 ]
    the_content = '\n'.join(content_lines)
    print("INFO: postprocessed content is:\n\n" + "\n".join(content_lines))

    print('INFO: Chapter title is "%s."' % the_title)
    print("INFO: tags are %s." % str(recurring_tags + temporary_tags))

    # All right, post this content
    print('\nINFO: Attempting to post the content')
    the_status, the_tumblr_data = social_media.tumblr_text_post(ulysses_client, the_tags, the_title, the_content)
    print('\nINFO: the_status is: ' + dump_str(the_status))
    print('\nINFO: the_tumblr_data is: ' + dump_str(the_tumblr_data))

    new_post_url = blog_url + "post/" + str(the_status['id'])

    # Assemble some text to write to the index file
    html_tags = ' | '.join([ '<a rel="me muse" href="%s">%s</a>' % (html.escape(blog_url + "tagged/" + the_tag), the_tag) for the_tag in the_tags.split(', ') ])

    # Avoid using a really really long first sentence as a summary (a problem sometimes in tests with "Penelope").
    while len(first_sentence) > 600 or len(first_sentence.split(' ')) > 150:
        first_sentence = ' '.join(first_sentence.split(' ')[0 : math.floor(len(first_sentence.split(' ')) * 0.75)]) + '…'   # Lop off the last quarter and try again.

    the_line = '<li><a rel="me muse" href="%s">%s</a>' % (new_post_url, the_title)
    the_line += ' (%s), ' %  datetime.date.today().strftime("%d %B %Y")
    the_line += current_run_data[ 'ch%02ddesc' % which_script ]
    the_line += ': <blockquote><p>%s</p>' % first_sentence
    the_line += '<p><small>tags: ' + html_tags + '</small></p>'
    the_line += '</blockquote></li>\n'

    # Now record the new line to the index file.
    the_lines.append(the_line)
    index_file = open('%s/index.html' % current_run_directory, 'w')
    index_file.writelines(the_lines)
    index_file.close()
