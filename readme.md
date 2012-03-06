
auditusers generates a JSON object containing a list of users that have contributed to a github repo in its history.

You can use this to generate a list of everyone who has contributed so that you can review it and determine if they should have been able to commit.  Potentially useful for identifying unauthorized committers in light of the recently disclosed vulnerability.

python audit.py --usage

Makes use of of github v3 api.

examples:

python audit.py -u githubuser -p githubpass -w resultsfile.json -r privateRepoToAudit -o ownerOfRepo
python audit.py -w resultsfile.json -r publicRepo -o ownerOfRepo

python audit.py -r auditusers -o ygjb

usage: Builds an audit trace of the specified repo. [-h] [-o USER] [-r REPO]
                                                    [-u USER] [-p PASSWORD]
                                                    [-w FILENAME]

optional arguments:
  -h, --help            show this help message and exit
  -o USER, --owner USER
                        The github user that owns a repo
  -r REPO, --repo REPO  The github repo to audit
  -u USER, --user USER  Username
  -p PASSWORD, --pass PASSWORD
                        Password
  -w FILENAME, --write FILENAME
                        File to write results to
