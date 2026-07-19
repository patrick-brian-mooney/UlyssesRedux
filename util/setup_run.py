#!/usr/bin/env python3
"""Script to set up for a new run of Ulysses Redux. Performs set-up operations.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""


import csv
import os
import subprocess
import sys


sys.path.append('/UlyssesRedux/scripts/')
import directory_structure as ds    # Gets us the listing of file and directory locations.
import util.current_run_utils as cru


def do_setup_run() -> None:
    # First, remove the old index file
    if ds.toc_fragment.is_file():
        if cru.confirm('Delete existing table of contents from last run? '):
            ds.toc_fragment.unlink()
        else:
            print('WARNING: daily script will not run & no new chapters will be posted until that file is removed.')

    # Set up the data dictionary, using the last run's dictionary keys as a template for this one's
    with open(ds.current_run_data_path, mode='r') as last_run_data_file:
        reader = csv.reader(last_run_data_file)
        last_run_data = {rows[0]:rows[1] for rows in reader}

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

    print(f'You can edit {ds.current_run_data_path} manually. (Be careful about auto-substitution of smart quotes.)')

    # OK, write the new dictionary
    with open(ds.current_run_data_path, 'w') as current_run_data_file:
        writer = csv.writer(current_run_data_file)
        for which_key in current_run_data:
            writer.writerow([which_key, current_run_data[which_key]])

    # All right. Check on status of the Git repo.
    oldpath = os.getcwd()   # FIXME: do we even need to monkey with the working dir when using get_current_git_branch?
    try:
        os.chdir(ds.git_repo_path)
        current_git_branch = cru.get_current_git_branch()
        if cru.confirm(f'Current Git branch is "{current_git_branch}". Commit changes, push to remote, and '
                       f'switch to master branch? '):

            subprocess.check_call(['git', 'add', '-u'])
            subprocess.call(['git', 'commit'])
            subprocess.check_call(['git', 'push', 'origin', current_git_branch])
            subprocess.check_call(['git', 'checkout', 'master'])
            print()

            if cru.confirm('Merge changes from branch "%s" into master branch? ' % current_git_branch):
                subprocess.check_call(['git', 'merge', current_git_branch])

        if cru.confirm('Create and switch to new Git branch? '):
            current_episode_number = 1 + int(str(sorted(ds.webpage_contents_directory.glob('???.html'))[-1])[-8:-5])
            branch_name = f"{current_episode_number:03}{''.join([the_word.capitalize() for the_word in current_run_data['current-run-name'].split()])}"
            branch_name = ''.join([c for c in branch_name if c.isalpha() or c.isnumeric()])
            if not cru.confirm(f'  use suggested branch name "{branch_name}"? '):
                branch_name = input('What branch name would you like to use? ')
            subprocess.check_call(['git', 'checkout', '-b', branch_name])

    finally:
        os.chdir(oldpath)

    # OK, write the 'temporary tags' file
    print('Temporary tags used in last run were:')
    with open(ds.temporary_tags_file) as old_tags_file:
        print(old_tags_file.read())

    new_temporary_tags = [][:]
    is_done = False
    while not is_done:
        print('\nEnter tags to be associated with this run, one per line. Hit ENTER on an empty line when finished.')
        empty_line = False
        while not empty_line:
            the_input = input('---| ')
            if the_input == "": empty_line = True
            else: new_temporary_tags.append(the_input + '\n')
        is_done = (input('Are you satisfied with this group of tags? ') or "yes").lower()[0] == 'y'

    ds.temporary_tags_file.write_text('\n'.join(new_temporary_tags), encoding='utf-8')

    print('\n')
    if cru.confirm(f'Remove all backup files ending in ~ from the entire "{ds.base_directory}" directory? '):
        subprocess.call([f'find {ds.base_directory} -iname "*~" -print0 | xargs -0 rm'], shell=True)

    print("\n\nOK, we're done!")


if __name__ == "__main__":
    do_setup_run()
