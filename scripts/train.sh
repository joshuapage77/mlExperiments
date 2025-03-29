#!/bin/bash

if [ -n "$VIRTUAL_ENV" ]; then
   echo "Running Locally"
   cd ../projects/"$ACTIVE_PROJECT" || exit 1
   python3 -m common.script.sweep "$@"
   cd ../../scripts || exit 1
else
   GIT_COMMIT=$(git rev-parse HEAD)
   cd ../docker || exit 1
   source ./.env

   ACTIVE_PROJECT=${1:-$ACTIVE_PROJECT}

   docker compose run --rm -e GIT_COMMIT="$GIT_COMMIT" project python3 -m common.script.sweep "$@"

   cd ../scripts || exit 1
fi