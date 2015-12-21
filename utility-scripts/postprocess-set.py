#!/usr/bin/env python3
"""When all 18 chapters of a Ulysses Redux set have been written, run this script
to postprocess the index.html file that's been created.

Currently, this script performs the following actions:
    * transforms the HTML fragment index.html, which is generated by the
      multiple runs of daily-script.py, into a full-fledged table of contents
      file, then puts that file with an appropriate name in the directory
      /~patrick/projects/UlyssesRedux/contents, which is the local directory
      from which it will be synced to my actual web site.
      * In order to do so, it reads the file /UlyssesRedux/current-run/data.csv
        and looks for data about the current run there. What it can't find, it
        prompts for.
    * It does not add an index line to the meta- (master) table of contents at
      /~patrick/projects/UlyssesRedux/contents/index.html, although it probably
      should do so (and probably will in the future).
    * Offers to perform this sync. Note that "this sync" syncs the entire local
      copy of my website to the server, not just the Ulysses Redux content (and
      so I sometimes say 'no' if there are other, incomplete changes in process).
      * Currently, it's probably wise to delay answering this question "yes"
        until the line in /~patrick/projects/UlyssesRedux/contents/index.html
        has been manually added.
"""

debugging_flag = True

import csv
import time
import glob
import subprocess
import os

if debugging_flag: print("INFO: imports successful.")

# Set up some constants
# Paths on local file system.
toc_fragment                = "/UlyssesRedux/current-run/index.html"
current_run_data_path       = '/UlyssesRedux/current-run/data.csv'
webpage_contents_directory  = '/~patrick/projects/UlyssesRedux/contents/'
git_repo_path               = '/home/patrick/Documents/programming/python projects/UlyssesRedux/'
meta_TOC_path               = '/~patrick/projects/UlyssesRedux/contents/index.html'

# Paths on Internet
github_branch_base_path = 'https://github.com/patrick-brian-mooney/UlyssesRedux/tree/'

# Other constants
current_episode_number =  1 + int(sorted(glob.glob('%s???.html' % webpage_contents_directory ))[-1][-8:-5])

# All right, let's read the expected data from the data file
with open(current_run_data_path, mode='r') as current_run_data_file:
    reader = csv.reader(current_run_data_file)
    current_run_data = {rows[0]:rows[1] for rows in reader}

# Now let's make sure that the expected data actually IS in the dictionary we've read. Prompt for missing stuff.
# Format of this dictionary is: keyname that should be in current_run_data -> question to ask if that keyname is missing
expected_keys =    {"current-run-name": "What is the title of the novel that has just been written?",
                    "summary": "Enter a summary description for the current novel:"}

for which_key in list(expected_keys.keys()):
    if which_key not in current_run_data.keys():
        current_run_data[which_key] = input(expected_keys[which_key] + " ")

if debugging_flag: print("INFO: constants set up; .csv dictionary has been read.")

# All right, let's sync the code to the folder that actually maintains the Git repository. If desired

# First, though, let's get basic info about the current git branch that we'll need later even if not syncing.
oldpath = os.getcwd()
try:
    os.chdir(git_repo_path)
    current_git_branch = subprocess.check_output(['git symbolic-ref --short HEAD'], shell=True).decode().split('\n')[0]
    print("\n\nCurrent git branch is:\n   " + current_git_branch)
    if input('Sync code to Git-watched repository? ').lower()[0] == 'y':
        # This next call syncs the code to git_repo_path, patching it to remove authentication tokens
        subprocess.check_call(['/UlyssesRedux/code/utility-scripts/sync-code.sh'], shell=True)
        print('\n\nINFO: OK, synced.')
        # Assume that syncing the code may also mean we want to commit and push it.
        print("\n\nReminder: current git branch is:\n   " + current_git_branch)
        if input('update Git repo with changed code files in this branch? ').lower()[0] == 'y':
            subprocess.check_call(['git add -u'], shell=True)
            current_git_status = subprocess.check_output(['git status'], shell=True)
            print("Current git status is\n  " + current_git_status.decode())
            if input('GIVEN THIS STATUS, do you want to commit? ').lower()[0] == 'y':
                subprocess.check_call(['git commit'], shell=True)
                if input('Push branch %s to remote server? ' % current_git_branch).lower()[0] == 'y':
                    subprocess.check_call(['git push origin %s' % current_git_branch], shell=True)
                    if input('Switch to master branch and merge these changes? ').lower()[0] == 'y':
                        subprocess.check_call(['git checkout master'], shell=True)
                        subprocess.check_call(['git merge %s' % current_git_branch], shell=True)
                        print("WARNING: THE MASTER BRANCH IS NOW THE CURRENT BRANCH")
                        if input('Push master branch to remote server? ').lower()[0] == 'y':
                            subprocess.check_call(['git push origin master'], shell=True)
finally:
    os.chdir(oldpath)

if debugging_flag: print("\n\nINFO: Git work done, beginning to generate HTML table of contents")

html_header = """<!doctype html>
<html prefix="og: http://ogp.me/ns#" xml:lang="en" lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="/~patrick/css/skeleton-normalize.css" />
  <link rel="stylesheet" type="text/css" href="/~patrick/css/skeleton.css" />
  <link rel="stylesheet" type="text/css" href="/~patrick/css/content-skel.css" />
  <link rel="meta" type="application/rdf+xml" title="FOAF" href="/~patrick/foaf.rdf" />
  <meta name="foaf:maker" content="foaf:mbox_sha1sum '48a3091d919c5e75a5b21d2f18164eb4d38ef2cd'" />
  <link rel="profile" href="http://microformats.org/profile/hcard" />
  <link rel="profile" href="http://microformats.org/profile/hcalendar" />
  <link rel="profile" href="http://gmpg.org/xfn/11" />
  <link rel="pgpkey" type="application/pgp-keys" href="/~patrick/505AB18E-public.asc" />
  <link rel="author" href="http://plus.google.com/109251121115002208129?rel=author" />
  <link rel="home" href="/~patrick/" title="Home page" />
  <link href="/~patrick/feeds/updates.xml" type="application/atom+xml" rel="alternate" title="Sitewide ATOM Feed" />
  <link rel="home" href="/~patrick/projects/UlyssesRedux/" title="Home page" />
  <link rel="icon" type="image/x-icon" href="/~patrick/icons/favicon.ico" />
  <link rel="contents" href="/~patrick/projects/UlyssesRedux/contents/" />
"""

html_header = html_header + """  <link rel="start" href="001.html" />
  <link rel="prev" href="%03d.html" />
  <link rel="next" href="%03d.html" />

  <title>Ulysses Redux #%03d</title>
  <meta name="generator" content="Bluefish 2.2.7" />
  <meta name="author" content="Patrick Mooney" />
  <meta name="dcterms.rights" content="Copyright © 2015 Patrick Mooney" />
  <meta name="description" content="Table of contents for Ulysses Redux #%03d" />
  <meta name="rating" content="general" />
  <meta name="revisit-after" content="10 days" />
""" % ((current_episode_number - 1), (current_episode_number + 1), current_episode_number, current_episode_number )

html_header = html_header + '''  <meta name="date" '''

html_header = html_header + """content="%s" />
  <meta property="fb:admins" content="100006098197123" />
  <meta property="og:url" content="http://patrickbrianmooney.nfshost.com/~patrick/projects/UlyssesRedux/contents/%03d.html" />
  <meta property="og:title" content="Ulysses Redux #%03d" />
  <meta property="og:description" content="Table of contents for Ulysses Redux #%03d" />
  <meta property="og:locale" content="en_US" />
  <meta property="og:site_name" content="Patrick Mooney's web site" />
  <meta property="og:image" content="http://patrickbrianmooney.nfshost.com/~patrick/icons/gear-large.png" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:site" content="@patrick_mooney" />
  <meta name="twitter:creator" content="@patrick_mooney" />
  <meta name="twitter:title" content="Ulysses Redux #%03d" />
  <meta name="twitter:description" content="Table of contents for Ulysses Redux #%03d" />
  <meta name="twitter:image:src" content="http://patrickbrianmooney.nfshost.com/~patrick/icons/gear-large.png" />
</head>
""" % (time.strftime("%Y-%m-%dT%H:%M:%S"), current_episode_number, current_episode_number, current_episode_number, current_episode_number, current_episode_number)

html_file = html_header + """<body lang="en-US" xml:lang="en-US">

<!--Begin navigation and tracking code-->
<header id="main-nav">
  <script type="text/javascript" src="/~patrick/nav.js"></script>
  <noscript>
    <p class="simpleNav"><a rel="me home" href="index.html">Go home</a></p>
    <p class="simpleNav">If you had JavaScript turned on, you'd have more navigation options.</p>
  </noscript>

  <script type="text/javascript">

     var _gaq = _gaq || [];
     _gaq.push(['_setAccount', 'UA-37778547-1']);
     gaq.push(['_setDomainName', 'nfshost.com']);
     gaq.push(['_setAllowLinker', true]);
     gaq.push(['_trackPageview']);

     (function() {
       var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
       ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
       var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
     })();

  </script>
</header>
<!--end navigation and tracking code -->

<div class="body-wrapper container main-content">
<h1>Ulysses Redux #%03d: %s</h1>
""" % (current_episode_number, current_run_data['current-run-name'])

# OK, get a summary fragment and turn it into valid HTML, if it isn't already. Assumption: if the fragment as a whole is bracketed <p> ... </p>,
# then assume that it's a pre-formatted HTML fragment; otherwise, split it into lines and bracket those lines <p> ... </p>.

if current_run_data['summary'].startswith('<p>') and current_run_data['summary'].endswith('</p>'):
    summary_text = current_run_data['summary']
else:
    summary_text = '\n'.join(['<p>' + the_line.strip() + '</p>' for the_line in current_run_data['summary'].split('\n')])

html_file = html_file + """
<h2 id="summary">Summary</h2>

%s
""" % summary_text

html_file = html_file + """

<h2 id="toc">Contents</h2>

<ol>
"""

html_file = html_file + open(toc_fragment).read()

html_file = html_file + """</ol>

<h2 id="scripts">Scripts</h2>

<p>The scripts used to generate this edition of <cite class="book-title">Ulysses Redux</cite> are available <a rel="me" href="%s">here</a>.</p>

""" % (github_branch_base_path + current_git_branch)

html_file = html_file + """<footer class="status vevent vcard"><a class="url location" href="#">This web page</a> is copyright © %s by <a rel="me" href="/~patrick/" class="fn url">Patrick Mooney</a>. <abbr class="summary description" title="Last update to table of contents for Ulysses Redux #%03d">Last update to <a class="url" href="#">this HTML file</a></abbr>: <abbr class="dtstart" title="%s">%s</abbr>.</footer>

</div>
</body>
</html>
""" % (time.strftime("%Y"), current_episode_number, time.strftime("%Y-%m-%dT%H:%M:%S"), time.strftime("%d %B %Y"))

if debugging_flag: print("INFO Generated HTML file is:\n" + html_file + "\n")

the_output_file = open('%s%03d.html' % (webpage_contents_directory, current_episode_number), 'w')
the_output_file.write(html_file)
the_output_file.close

if debugging_flag: print("INFO: HTML file written; tidying ...")

subprocess.call(['tidy -m -i -w 0 -utf8 --doctype html5 --fix-uri true --new-blocklevel-tags footer --quote-nbsp true --preserve-entities yes %s%03d.html' % (webpage_contents_directory, current_episode_number)], shell=True)

if debugging_flag: print("\n\nINFO: Tidying done.")

print('\n')
if input('Update coding journal on website? ').lower()[0] == 'y':
    subprocess.call(["pandoc -f markdown -s -t html5 -o '/~patrick/projects/UlyssesRedux/coding.html' '/UlyssesRedux/coding thoughts.md'"], shell=True)
    subprocess.call(['patch /~patrick/projects/UlyssesRedux/coding.html /UlyssesRedux/coding\ thoughts.patch'], shell=True)
    subprocess.call(['rm /~patrick/projects/UlyssesRedux/coding.html.bak'], shell=True)
    subprocess.call(['tidy -m -i -w 0 -utf8 --doctype html5 --fix-uri true --new-blocklevel-tags footer --quote-nbsp true --preserve-entities yes /~patrick/projects/UlyssesRedux/coding.html'], shell=True)

if input('Update meta-TOC on local copy of website? ').lower()[0] == 'y':
    with open(meta_TOC_path) as TOC_file:
        TOC_text = TOC_file.read()
    TOC_split = TOC_text.split('</ol>')     # Works as long as there's only one ordered list in the document
    TOC_text = TOC_split[0] + '<li class="vevent"><a class="url location" rel="me muse" href="%03d.html"><cite class="book-title">%s</cite></a> (<span class="dtstart">%s</span>): <span class="summary description">%s</span>.</li>' % () + '  </ol>\n</section>\n</div>\n</body>\n</html>' %(current_episode_number, current_run_data['current-run-name'], time.strftime("%Y-%m-%dT%H:%M:%S"), current_run_data['summary'])
    with open(meta_TOC_path, 'w') as TOC_file:
        TOC_file.write(TOC_text)


print('\n\n\nWARNING: new table of contents NOT LINKED from meta-table of contents.') 
if input('Sync web page to main site? ').lower()[0] == 'y':
    # This script lives on my hard drive at ~/.scripts/sync-website.sh
    subprocess.check_call(['sync-website.sh'], shell=True)

print('\n\n')
if input("We're done here. Want to set up the next run? ").lower()[0] == 'y':
    subprocess.check_call(['/UlyssesRedux/code/utility-scripts/setup-run.py'], shell=True)
