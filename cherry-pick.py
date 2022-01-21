#!/usr/bin/python3

import os
import os.path
import subprocess
import sys
import tempfile
import urllib.request
import urllib.error

cherry_picks = [
    '5a5ebecafe',
    '2722efafe8',
    '3959bdc1a1',
    '263a57e209',
    'a4e5c0497e',
]

if len(sys.argv) < 2:
    print("Required k8s directory", file=sys.stderr)
    sys.exit(-1)

os.chdir(sys.argv[1])

with tempfile.TemporaryDirectory() as tmpdir:
    for cp in cherry_picks:
        try:
            patch = os.path.join(tmpdir, cp + ".patch")
            response = urllib.request.urlretrieve(
                "https://github.com/openshift/origin/commit/{}.patch".format(
                    cp),
                filename=patch)
            subprocess.run(["git", "am", "-p4", patch],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           check=True)
            print(cp, "applied successfully")
        except urllib.error.URLError as e:
            print("Error getting {} commit".format(cp), file=sys.stderr)
            continue
        except subprocess.CalledProcessError as e:
            print("Error applying {} commit".format(cp), file=sys.stderr)
            try:
                subprocess.run(["git", "am", "--abort"],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL,
                               check=True)
            except subprocess.CalledProcessError as e:
                pass
