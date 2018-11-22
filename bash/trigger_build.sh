#!/bin/bash

#First arg repo name, second arg commit message, last API key

#https://docs.travis-ci.com/user/triggering-builds

REPO=$1
MSG=$2
API_KEY=$3
#Replace / with %f2
URL="https://api.travis-ci.org/repo/${REPO/\//%2F}/requests"
#URL="https://api.travis-ci.org/repo/${REPO}/requests"
echo $URL
body='{
"request": {
 "message":"'"${MSG}"'",
 "branch":"master"
}}'
echo $body

curl -s -X POST \
   -H "Content-Type: application/json" \
   -H "Accept: application/json" \
   -H "Travis-API-Version: 3" \
   -H "Authorization: token ${API_KEY}" \
   -d "$body" \
   "$URL"

