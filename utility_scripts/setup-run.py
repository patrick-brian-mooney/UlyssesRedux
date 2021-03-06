#!/usr/bin/env python3
"""Script to set up for a new run of Ulysses Redux. Performs set-up operations.

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.
"""

import os, glob, csv, subprocess

import sys
sys.path.append('/UlyssesRedux/scripts/')
from directory_structure import *           # Gets us the listing of file and directory locations.

# First, remove the old index file
if os.path.isfile(toc_fragment):
    if (input('Delete existing table of contents from last run? ') or "no").lower()[0] == 'y':
        os.remove(toc_fragment)
    else:
        print('WARNING: daily_script.py will not run, and no new chapters will be produced, until this file is removed.')

# Set up the data dictionary, using the last run's dictionary keys as a template for this one's
last_run_data = {}.copy()
with open(current_run_data_path, mode='r') as last_run_data_file:
    reader = csv.reader(last_run_data_file)
    last_run_data = {rows[0]:rows[1] for rows in reader}

is_done = False
while not is_done:
    print("\n\nOK, let's set up the parameters for the next run.")
    print("You can type (all-caps) SAME at any prompt to re-use the last run's answer to that question.\n")
    current_run_data = {}.copy()
    for which_key in sorted(last_run_data.keys()):
        answer = input('%s (previously "%s") ---|  ' % (which_key, last_run_data[which_key]))
        if answer == "SAME":
            current_run_data[which_key] = last_run_data[which_key]
        elif answer != "":
            current_run_data[which_key] = answer
    print('')
    is_done = (input("Are you satisfied with that data? ") or "yes").lower()[0] == 'y'

print('Remember, too, that you can edit %s manually. (Be careful about auto-substitution of smart quotes.)' % current_run_data_path)

# OK, write the new dictionary
with open(current_run_data_path, 'w') as current_run_data_file:
    writer = csv.writer(current_run_data_file)
    for which_key in current_run_data:
        writer.writerow([which_key, current_run_data[which_key]])

# All right. Check on status of the Git repo.
oldpath = os.getcwd()
try:
    os.chdir(git_repo_path)
    current_git_branch = subprocess.check_output(['git symbolic-ref --short HEAD'], shell=True).decode().split('\n')[0]
    if (input('Current Git branch is "%s". Commit changes, push to remote, and switch to master branch? ' % current_git_branch) or "yes").lower()[0] == 'y':
        subprocess.check_call(['git add -u'], shell=True)
        subprocess.call(['git commit'], shell=True)
        subprocess.check_call(['git push origin %s' % current_git_branch], shell=True)
        subprocess.check_call(['git checkout master'], shell=True)
        print('')
        if (input('Merge changes from branch "%s" into master branch? ' % current_git_branch) or "yes").lower()[0] == 'y':
            subprocess.check_call(['git merge %s' % current_git_branch], shell=True)
    if (input('Create and switch to new Git branch? ') or "yes").lower()[0] == 'y':
        current_episode_number =  1 + int(sorted(glob.glob('%s???.html' % webpage_contents_directory ))[-1][-8:-5])
        branch_name = "%03d%s" % (current_episode_number, ''.join([the_word.capitalize() for the_word in current_run_data['current-run-name'].split()]) )
        branch_name = ''.join([c for c in branch_name if c.isalpha() or c.isnumeric()])
        if (input('  use suggested branch name "%s"? ' % branch_name) or "yes").lower()[0] != 'y':
            branch_name = input('What branch name would you like to use? ')
        subprocess.check_call(['git checkout -b %s' % branch_name], shell=True)
finally:
    os.chdir(oldpath)

# OK, write the 'temporary tags' file
print('Temporary tags used in last run were:')
with open(temporary_tags_file) as old_tags_file:
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

with open(temporary_tags_file, 'w') as temp_tags_file:
    temp_tags_file.writelines(new_temporary_tags)

print('\n')
if (input('Remove all backup files ending in ~ from the entire "%s" directory? ' % base_directory) or "no").lower()[0] == 'y':
    subprocess.call(['find %s -iname "*~" -print0 | xargs -0 rm' % base_directory], shell=True)

print("\n\nOK, we're done!")
