
#!/usr/bin/env python3
"""Produces 18 chapters at once. Doesn't do any postprocessing (yet)."""

import subprocess

for which_chapter in range(0, 18):
    subprocess.call(['/UlyssesRedux/code/daily-script.py'], shell=True)

subprocess.call(['/UlyssesRedux/code/utility-scripts/postprocess-set.py'], shell=True)