Servers and Release
===================

We use a gitflow based automatic deployment setup so that branches are pushed to  relevant servers.

![Gitflow Setup 1](https://raw.githubusercontent.com/CentreForResearchInAppliedLinguistics/clic/095c9e3066f0b7890d9a8c0f2eb3e14a119987d2/docs/handover/images/deploy1.png)

The bamboo build task checks out the code (would then run tests) and finally runs a bash script that is responsible for finding the server to push to:

```
/home/bamboo/scripts/git-deploy-gitflow.sh -d ${bamboo.build.working.directory} -r ${bamboo.repository.revision.number} -b ${bamboo.repository.branch.name} clic.nottingham.ac.uk/usr/local/lib/clic.git
```

The bash script:

```
#!/bin/bash
# Script checks to see if Git commit comment(s) contain "#release" anywhere in the text
#  - if so, then complete list of servers passed as arguments (see $SERVERS below) is passed through to $SCRIPT
#  - if not, then any servers containing the text "dev" are passed through to $SCRIPT
# Shaun Hare amd Ian White - Mar 2012

# Version 1.1
#  - amended Ben Bennett 15/01/13
#  - debug flag (-d) is not currently used, no debug mode available, all messages are currently logged
# Version 1.2
# amended by Shaun Hare
# - changed to do git push develop and release
# Version 1.3
# - amended Adam Cooper 25/03/13

ERRORCOUNT=0
# Set the exec directory
EXECDIR="/home/bamboo/scripts"

# Get the script arguments
# BUILDDIR - from Bamboo build.working.directory
### DEBUG - flag indicating in debug mode
# DIRECTORY - directory into which to place the deployed script (see contents of SCRIPT for usage)
# SCRIPT - shell (.sh) script to call for deployment (and chmod etc)
# GITREV - from Bamboo repository.revision.number

while getopts d:r:b: option
do
    case $option in
        d) BUILDDIR="$OPTARG";;
        r) GITREV="$OPTARG";;
        b) BRANCH="$OPTARG";;
    esac
done

# Check that non-empty arguments have been passed in
#  - http://serverfault.com/questions/7503/how-to-determine-if-a-bash-variable-is-empty
if [ -z "$BUILDDIR" ]; then let ERRORCOUNT+=1; fi
if [ -z "$GITREV" ]; then let ERRORCOUNT+=1; fi
if [ -z "$BRANCH" ]; then let ERRORCOUNT+=1; fi

# Exit if missing arguments or empty arguments have been passed
if [ $ERRORCOUNT != "0" ]
then
    echo "usage $0 -d BUILDDIR -r GITREV -b BRANCH SERVER"
    exit 1
fi

# Get the servers to deploy to e.g dev.imat test.imat
shift `expr $OPTIND - 1`
SERVER=$*

DEVSERVER="ssh://bamboo@dev.$SERVER"
TESTSERVER="ssh://bamboo@test.$SERVER"
LIVESERVER="ssh://bamboo@$SERVER"

echo -e "\nEXECDIR = $EXECDIR"
echo "BUILDDIR = $BUILDDIR"
echo "BRANCH = $BRANCH"
echo "GITREV = $GITREV"
echo "SERVER = $SERVER"

# If the build directory exists, cd to it
if [ -d $BUILDDIR ]
then
    cd $BUILDDIR
    GITLOG=`git log --format=%B -n 1 $GITREV `
    echo "GITLOG = $GITLOG"
else
    echo "Could not find $BUILDDIR"
    exit 1
fi

#MASTERCMD="git push liveserver $BRANCH" #Not forcing because... well... live.
MASTERCMD=""
RELEASECMD="git push --force testserver $BRANCH"
DEVCMD="git push --force devserver $BRANCH"

cd $BUILDDIR

echo "Adding dev and test server remote repositories"
git remote add devserver $DEVSERVER
git remote add testserver $TESTSERVER
#git remote add liveserver $LIVESERVER

if [[ "$BRANCH" == "develop" ]]; then
    echo -e "Pushing to dev:\n$DEVCMD"
    $DEVCMD
elif [[ "$BRANCH" == "release"* ]]; then
    echo -e "Pushing to test:\n$RELEASECMD"
    $RELEASECMD
elif [[ "$BRANCH" == "master" ]]; then
    echo -e "Pushing to live:\n$MASTERCMD"
    $MASTERCMD
fi
```

The servers each contain two folders that have the site code in. One is a bare git repository. This is the one that gets pushed to by the above script. The other is a normal respository (and the one that gets served by the uwsgi). The bare repository contains a post-update hook that ensures changes pushed to the bare repository are pushed onwards to the served repository. We rely on the emperor process to detect file changes and restart the application.

The above setup requires that we have 3 servers so that files get put in the right places. The script requires a path to the bare repository as well as the live server hostname (which it prefixes dev or test based on the branch name)

You'll notice we do not push to live via this technique though it should be possible and is probably the way we should do it because...

We use the alternative which ssh'ing onto the live server and doing a git pull in the website directory. This should pull doing any changes to the master branch which is just fine because we use git-flow and only tested and approved changes occur in that branch.
