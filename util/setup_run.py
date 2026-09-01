#!/usr/bin/env python3
"""Script to set up for a new run of Ulysses Redux. Performs set-up operations.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this license.
"""


import collections
import csv
import re
import subprocess
import sys
import warnings

from typing import Callable, Literal, Optional, Union

import roman                # https://github.com/zopefoundation/roman


sys.path.append('/UlyssesRedux/scripts/')
from directory_structure import *           # Gets us the listing of file and directory locations.
import util.current_run_utils as cru


def confirm_exec(prompt: str,
                 pre_prompt_func: Optional[Callable] = None,
                 conf_param: Union[bool, None] = None,
                 ) -> Union[bool, None]:
    """Convenience function to interpret the "do we change things here" parameters for
    do_setup_run(), below: True menns "yes, prompt for new parameters without
    asking"; False means "no, keep the same parameters without even prompting"; and
    None means "prompt the user in the terminal to determine whether to change the
    relevant run parameters."

    PROMPT is the question to ask. If PRE_PROMPT_FUNC is not None, it is run before
    asking the PROMPT question.
    """
    assert conf_param in {True, False, None}

    if isinstance(conf_param, bool):
        return conf_param
    else:
        if pre_prompt_func:
            pre_prompt_func()
        return cru.confirm(prompt)


def bump_novel_title(previous_title: str) -> str:
    """Given PREVIOUS_TITLE, the title of the previous Ulysses Redux novel, generate
    and return the title of the next novel. If the previous novel's title ends with
    a Roman numeral in parentheses, the generated title will replace it with the
    next higher Roman numeral. Otherwise, tries to make reasonable
    """
    suffixes = list(re.finditer(r'\([IVXLCDM]+\)', previous_title))
    if not suffixes:
        ret = f"{previous_title} (II)"
        warnings.warn(f"Unable to break down previous title; using {ret} ...")

    if len(suffixes) > 1:
        warnings.warn("Found multiple possible matches for Roman numerals in {previous_title}. Using the last ...")
    suffix = suffixes[-1]

    try:
        rom = roman.fromRoman(previous_title[suffix.start():suffix.end()].lstrip('(').rstrip(')').strip())
        return f"{previous_title[:suffix.start()].strip()} ({roman.toRoman(1 + rom)})"
    except (IndexError, roman.RomanError,) as errrr:
        ret = f"{previous_title[:suffix.start()].strip()}"
        warnings.warn(f"Unable to formulate new title: using {ret}")
        return ret


def do_setup_run(delete_toc: Union[bool, None, Literal["auto"]] = None,
                 manually_edit_parameters: Union[bool, None, Literal["auto"]] = None,
                 manually_manage_git_branch: Union[bool, None, Literal["auto"]] = None,
                 manually_manage_temp_tags: Union[bool, None, Literal["auto"]] = None,
                 delete_temp_files: Union[bool, None, Literal["auto"]] = None,
                 ) -> None:
    """Set up the file system and relevant data files to generate the next iteration
    of Ulysses Redux. All the parameters to this function can be True, False, or
    None: True means "do the thing"; false means "don't do the thing"; None
    means "prompt the user in the terminal to see whether the thing should be done;
    and the literal string "auto" means "do what we do when auto-resetting."
    Historically, the None behavior (ask the user in the terminal whether to do the
    thing or not) has been the default behavior; these parameters let that choice be
    made by other code that can call this function to schedule a new run so I don't
    have to babysit the blog every 18 days.

    DELETE_TOC indicates whether the table of contents for the previous iteration
      should be deleted (if this is not done new chapters will not be written when
      daily_script.py is invoked by cron). "auto" means True here.
    MANUALLY_EDIT_PARAMETERS: if True, offer to let the user change the by-novel and
      by-chapter data (currently 38 items) describing the previous run. If False,
      leaves that data alone, except it attempts to automatically generate a new
      title for the novel being written. "auto" means False here
    MANUALLY_MANAGE_GIT_BRANCH: if True, commits the changes made to code in the
      current Git branch, which should be for the specific iteration being written;
      then merges those changes into the master branch and commits that change,
      then pushes the master branch to the remote GitHub repository. "auto" means
      "do all the committing stuff I normally do, and automatically generate a name
      for the new branch in the way I would do so" here.
    MANUALLY_MaNAGE_TEMP_TAGS: If True, prompts the user to enter a new set of
      temporary tags to be applied to each Tumblr post in this series. If False,
      re-uses the same tags as the last run. "auto" means False here.
    DELETE_TEMP_FILES: If True, all files whose names end with a tilde in the entire
      project directory (not just the code-related subfolder) are deleted. "auto"
      means False here.
    """
    # First, remove the old index file
    if toc_fragment.is_file():
        if (delete_toc == "auto") or confirm_exec(conf_param=delete_toc,
                                                  prompt='Delete existing table of contents from last run? '):
            toc_fragment.unlink(missing_ok=True)    # don't complain if it's already been done
        else:
            warnings.warn('daily script will not run & no new chapters will be posted until that file is removed.')

    # Set up the data dictionary, using the last run's dictionary keys as a template for this one's
    with open(current_run_data_path, mode='r') as last_run_data_file:
        reader = csv.reader(last_run_data_file)
        last_run_data = {rows[0]:rows[1] for rows in reader}

    manually_edit_parameters = ((manually_edit_parameters != "auto") and
                                confirm_exec(conf_param=manually_edit_parameters,
                                             prompt="Change the run data for the next run right now in the terminal?"))
    if manually_edit_parameters:
        is_done = False
        while not is_done:
            current_run_data = dict()

            print("\n\nOK, let's set up the parameters for the next run.")
            print("You can type (all-caps) SAME at any prompt to re-use the last run's answer to that question.\n")

            for which_key in sorted(last_run_data.keys()):
                answer = input(f'{which_key} (previously "{last_run_data[which_key]}") ---|  ')
                if answer == "SAME":
                    current_run_data[which_key] = last_run_data[which_key]
                elif answer != "":
                    current_run_data[which_key] = answer

            print()
            is_done = cru.confirm("Are you satisfied with that data? ")

    elif manually_edit_parameters is False:
        new_name = bump_novel_title(last_run_data['current-run-name'])
        print(f"Updated title for this run to {new_name}")
        current_run_data = dict(collections.ChainMap({'current-run-name': new_name}, last_run_data))

    else:
        print("Leaving run data the same as for the last run. (You probably at least want to edit the title.)")
        current_run_data = last_run_data.copy()

    try:
        del current_run_data['last-posted']     # This only gets set for a run when we post something for that run
    except KeyError:            # is that not in the current run parameters? No need to delete it, then
        pass

    cru.write_current_run_data(current_run_data)
    print(f'You can edit {current_run_data_path} manually. (Be careful about auto-substitution of smart quotes.)')

    current_git_branch = cru.get_current_git_branch()

    # FIXME: detect and handle the case that we already are on the master branch.
    if (manually_manage_git_branch == "auto" or
            confirm_exec(f'Current Git branch is "{current_git_branch}". Commit changes, push to remote, and '
                         f'switch to master branch?', conf_param=manually_manage_git_branch)):

        subprocess.check_call(['git', 'add', '-u'])

        commit_msg = f"setting up for next run after {current_git_branch}"      #FIXME: this winds up being "setting up for next run after master" often, which is suboptimal
        if manually_manage_git_branch != "auto" and not cru.confirm(f'  use "{commit_msg}" as commit message?'):
            commit_msg = input("  enter commit message to use --| ").strip()

        subprocess.call(['git', 'commit', '-m', commit_msg])
        subprocess.check_call(['git', 'push', 'origin', current_git_branch])
        subprocess.check_call(['git', 'checkout', 'master'])
        print()

        if ((manually_manage_git_branch == "auto") or
                confirm_exec(f'Merge changes from branch "{current_git_branch}" into master branch? ',
                             conf_param=manually_manage_git_branch)):
            subprocess.check_call(['git', 'merge', current_git_branch])

    if (manually_manage_git_branch == "auto" or
            confirm_exec('Create and switch to new Git branch?', conf_param=manually_manage_git_branch)):
        current_episode_number = 1 + int(str(sorted(webpage_contents_directory.glob('???.html'))[-1])[-8:-5])       # FIXME:Watch for why this isn't working well
        ep_title = ''.join([the_word.capitalize() for the_word in current_run_data['current-run-name'].split()])

        rom_nums = list(re.finditer(r'\([IVXLCDM]+\)', ep_title, flags=re.IGNORECASE))
        if rom_nums:
            if len(rom_nums) > 1:
                warnings.warn("Found multiple possible Roman numerals in {previous_title}. Using the last ...")
            suffix = rom_nums[-1]

            try:
                rom = roman.fromRoman(ep_title[suffix.start():suffix.end()].strip().lstrip('(').rstrip(')').strip())
                ep_title = ep_title[:suffix.start()]
                suffix = roman.toRoman(rom)
            except (IndexError, roman.RomanError,) as errrr:
                warnings.warn(f"Unable to formulate new title: using no Roman numeral suffix ...")
                suffix = ""
        else:
            suffix = "II"
            warnings.warn(f"Unable to break down previous title; using II for suffix ...")

        branch_name = f"{current_episode_number:03}{ep_title}{suffix.upper()}"
        branch_name = ''.join([c for c in branch_name if c.isalpha() or c.isnumeric()])

        if (manually_manage_git_branch != "auto") and not cru.confirm(f'  use suggested branch name "{branch_name}"? '):
            branch_name = input('What branch name would you like to use? ')
        subprocess.check_call(['git', 'checkout', '-b', branch_name])

    with open(temporary_tags_file) as old_tags_file:
        old_tags = [l.strip() for l in old_tags_file.readlines() if l.strip()]

    if ((manually_manage_temp_tags != "auto") and
            confirm_exec("Do you want to enter a new set of temporary tags now in the terminal?",
                         pre_prompt_func=lambda: print(f'Temporary tags used in last run were:\n{old_tags}'),
                         conf_param=manually_manage_temp_tags)):
        new_temporary_tags = list()
        is_done = False
        while not is_done:
            print('\nEnter tags to be associated with this run, one per line. Hit ENTER on empty line when finished.')
            empty_line = False
            while not empty_line:
                the_input = input('---| ')
                if the_input == "":
                    empty_line = True
                else: new_temporary_tags.append(the_input + '\n')
            is_done = (input('Are you satisfied with this group of tags? ') or "yes").lower()[0] == 'y'

        temporary_tags_file.write_text('\n'.join(new_temporary_tags), encoding='utf-8')

    print('\n')
    if ((delete_temp_files == "auto") or
            confirm_exec(f'Remove all backup files ending in ~ from the entire "{base_directory}" directory?',
                         conf_param = delete_temp_files)):
        count, failed = 0, 0
        for f in base_directory.glob('*~'):
            if f.is_file():
                try:
                    f.unlink()
                    count += 1
                except (IOError,) as errrr:
                    print(f"  ... unable to delete {f}; the system said: {errrr}")
                    failed += 1
        print(f"{('%d' % count if count else 'No')} file{'s' if count != 1 else ''} deleted; "
              f"unable to delete {failed} file{'s' if failed != 1 else ''}.")

    print("\n\nOK, we're done!")


if __name__ == "__main__":
    do_setup_run()
