#!/bin/bash
# Thanks to https://docs.travis-ci.com/user/job-lifecycle/
set -ev
# echo "TRAVIS_BRANCH=$TRAVIS_BRANCH TRAVIS_PULL_REQUEST=$TRAVIS_PULL_REQUEST"
echo TRAVIS_API_TOKEN: $TRAVIS_API_TOKEN
MSG="Auto test triggered by repo `basename $(git rev-parse --show-toplevel)` commit `git rev-parse HEAD`"
./travis/trigger_build.sh "lino-framework/react" "$MSG" "$TRAVIS_API_TOKEN"
./travis/trigger_build.sh "lino-framework/welfare" "$MSG" "$TRAVIS_API_TOKEN"
./travis/trigger_build.sh "lino-framework/presto" "$MSG" "$TRAVIS_API_TOKEN"
./travis/trigger_build.sh "lino-framework/book" "$MSG" "$TRAVIS_API_TOKEN"
