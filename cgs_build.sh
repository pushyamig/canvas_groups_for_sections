#!/bin/sh --

# Helper script for use on build server.
# Debugging: -x to enable, +x to disable
# -e: the shell shall immediately exit in case of failure of list of commands
set -xe
timestamp=$(date +%Y%m%d%H%M%S)

## find the next Jenkins build number from environment setting: BUILD_NUMBER
## if missing, set the number to be 1
echo "shell env variable BUILD_NUMBER is ${BUILD_NUMBER}"
build_number=${BUILD_NUMBER:=1}

#GIT_BRANCH =origin/TLUNIZIN-424 or origin/master jenkins environmental variable to get git branch
branch=${GIT_BRANCH}
if [ -n "$branch" ]; then
btemp=$(basename ${branch} /)
else
btemp="local_branch"
fi

## check the artifact folder, whether it exists or not
if [ ! -d "artifact" ]; then
    ## no artifact folder
    ## create such folder first
    echo "create artifact folder"
    mkdir artifact
    chmod -R 755 artifact
fi
echo "Generating zip file for build number: ${build_number}"
## get git hex number
gitNum=`git log -n 1 --pretty="format:%h"`
printf "Build# $BUILD_NUMBER | $GIT_URL | $gitNum | $btemp | $BUILD_ID" > git_version.txt
find . -maxdepth 1 -type f \( -name "*.txt" -o -name "*.py" \) -exec tar -rf ./artifact/CGS_${gitNum}_${btemp}_${timestamp}.tar {} \;


