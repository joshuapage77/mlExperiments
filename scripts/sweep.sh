#!/bin/bash

if [ -n "$VIRTUAL_ENV" ]; then
echo Running Locally
cd ../projects/$ACTIVE_PROJECT
python3 /project/src/common/script/sweep.py -m
cd ../../scripts
else
cd ../docker || exit 1

source ./.env

ACTIVE_PROJECT=${1:-$ACTIVE_PROJECT}
docker compose run --rm project \
  bash -c "python3 /project/src/common/script/sweep.py -m"

cd ../scripts || exit 1
fi
