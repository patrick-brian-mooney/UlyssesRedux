#!/UlyssesRedux/scripts/venv/bin/python3
# cython: language_level=3
# -*- coding: utf-8 -*-
"""Script to call modules that generate the blog's content, then posts that
content to the ulyssesredux.tumblr.com.

Each chapter is written by a different script that resides in the
chapter_scripts/ directory. Each of these scripts then draw from
texts in the corpora/ directory.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this license.
"""


import datetime
import html
import importlib
import json
import math
import os
import re
import sys

from pathlib import Path


import pyximport; pyximport.install()           # https://cython.org/


sys.path.append('/UlyssesRedux/scripts/')
import directory_structure as ds    # Gets us the listing of file and directory locations.
import util.current_run_utils as cru
import util.setup_run as sr

from introspection import dump_str  # From https://github.com/patrick-brian-mooney/personal-library
import social_media                 # From https://github.com/patrick-brian-mooney/personal-library


# constants, utility functions, etc.
RECURRING_TAGS = ['Ulysses (novel)', 'James Joyce', '1922', 'automatically generated text', 'Patrick Mooney']
ULYSSES_CHAPTERS = [l.rstrip() for l in open(ds.ulysses_chapter_titles_file).readlines() if l.rstrip()]

BLOG_URL = 'http://ulyssesredux.tumblr.com/'
DAYS_TO_WAIT_BEFORE_RESETTING = 4.8


# Some utility routines
def out_of_content_warning():
    """Remind me that we're out of content."""
    msg = ("WARNING: There's work to be done! You have to reset the blog state on ulyssesredux.tumblr.com to get it "
           "working again! A full Ulysses project is done and needs to be cleared!")
    print(msg)  # in case cron is mailing output to me.
    cru.gui_dialog(msg)
    sys.exit(2)


def do_reset_blog() -> None:
    """Reset the blog parameters to get ready for the next run. Let me know that this
    was done.
    """
    sr.do_setup_run(delete_toc='auto', manually_edit_parameters='auto', manually_manage_git_branch='auto',
                    manually_manage_temp_tags='auto', delete_temp_files='auto')
    msg = (f"INFO: After {DAYS_TO_WAIT_BEFORE_RESETTING} days of not posting, automatically reset UlyssesRedux state "
           f"so we can post tomorrow. Current Git branch name is: {cru.get_current_git_branch()}")
    cru.gui_dialog(msg)
    print(msg)      # in case cron is mailing output to me.
    sys.exit(2)


def handle_out_of_content() -> None:
    """Handle being out of content. For the first few days, just display a warning.
    Once we've done that for at least DAYS_TO_WAIT_BEFORE_RESETTING, go ahead and
    auto-prepare for the next run.
    """
    date_str = cru.get_current_run_parameter('last-posted')
    date = datetime.datetime.fromisoformat(date_str)
    if (datetime.datetime.now() - date).days >= DAYS_TO_WAIT_BEFORE_RESETTING:
        do_reset_blog()
    else:
        out_of_content_warning()


@cru.only_if_not_running(pidfile_loc=Path(__file__).parent / 'daily_script.pid')
def do_write_chapter() -> None:
    with open('/social_media_auth.json', encoding='utf-8') as auth_file:
        ulysses_client = social_media.Tumblpy_from_dict(json.loads(auth_file.read())['ulysses_client'])

    current_run_data = cru.read_current_run_parameters()

    try:
        with open(ds.current_run_directory / 'index.html', 'r') as index_file :
            toc_lines = [l.strip() for l in index_file.readlines() if l.strip()]
            which_script = 1 + len(toc_lines)   # If so far we've got, say, six lines, we need to run script #7.

    except (FileNotFoundError,):
        which_script = 1
        toc_lines = list()

    if which_script not in range(1,19):
        handle_out_of_content()
        sys.exit(3)                 # we should have already quit by now, but be sure.

    # Post parameters
    the_title = ULYSSES_CHAPTERS[which_script - 1].strip()

    current_chapter_temporary_tags = current_run_data[f'ch{which_script:0>2}tags']
    temporary_tags = [l.rstrip() for l in open(ds.current_run_directory / 'temporary-tags').readlines()]
    temporary_tags.append(the_title)
    the_tags = ', '.join(RECURRING_TAGS + temporary_tags) + ', ' + current_chapter_temporary_tags

    script_path = f'{ds.daily_scripts_directory}.ch{which_script:0>2}'

    print(f"INFO: About to run script {script_path}.py.")

    # OK, import the relevant chapter script as a module and write the story.
    the_script = importlib.import_module(script_path)
    the_content = the_script.write_story()
    print("content generated ...\n\n  ... postprocessing...")

    content_lines = the_content.split("\n")
    # Now, split the 1st para into sentences, keeping final punctuation and joining it back on the end of the sentence.
    first_sent = ''.join(list(filter(None, re.split("([!?.]+)", content_lines[0])))[0:2])       # We'll use this as the summary in the table of contents.
    content_lines = [ "<p>" + the_line.strip() + "</p>" for the_line in content_lines if len(the_line.strip()) > 0 ]
    the_content = '\n'.join(content_lines)
    print("INFO: postprocessed content is:\n\n" + "\n".join(content_lines))

    print(f'INFO: Chapter title is "{the_title}."')
    print(f"INFO: tags are {(RECURRING_TAGS + temporary_tags)}.")

    # All right, post this content
    print('\nINFO: Attempting to post the content')
    the_status, the_tumblr_data = social_media.tumblr_text_post(ulysses_client, the_tags, the_title, the_content)
    print('\nINFO: the_status is: ' + dump_str(the_status))
    print('\nINFO: the_tumblr_data is: ' + dump_str(the_tumblr_data))

    # and record that we've done so.
    cru.set_current_run_parameter('last-posted', datetime.datetime.now().isoformat())

    # and track the posting we made by writing a line into our fragmentary HTML table of contents
    new_post_url = f"{BLOG_URL}post/{the_status['id']}"

    # Assemble some text to write to the index file
    html_tags = ' | '.join([f"""<a rel="me muse" href="{html.escape(BLOG_URL + "tagged/" + t)}">{t}</a>"""
                            for t in the_tags.split(', ')])

    # Avoid letting a really, really long first sentence be the summary (a problem sometimes in tests with "Penelope").
    while len(first_sent) > 600 or len(first_sent.split(' ')) > 150:
        # Lop off the last quarter and try again.
        first_sent = ' '.join(first_sent.split(' ')[0: math.floor(len(first_sent.split(' ')) * 0.75)]) + '…'

    the_line = f'<li><a rel="me muse" href="{new_post_url}">{the_title}</a>'
    the_line += f' ({datetime.date.today().strftime("%d %B %Y")}), '
    the_line += current_run_data[f'ch{which_script:0>2}desc' ]
    the_line += f': <blockquote><p>{first_sent}</p>'
    the_line += f'<p><small>tags: {html_tags}</small></p>'
    the_line += '</blockquote></li>'

    # Finally, record the new line to the index file.
    toc_lines.append(the_line.strip())
    (ds.current_run_directory / 'index.html').write_text('\n'.join([l.strip() for l in toc_lines]).strip(),
                                                         encoding='utf-8')


if __name__ == "__main__":
    os.chdir(ds.git_repo_path)
    do_write_chapter()
