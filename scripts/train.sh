#!/bin/bash
cd ../docker || exit 1

source ./.env

ACTIVE_PROJECT=${1:-$ACTIVE_PROJECT}
docker compose run --rm project \
  bash -c "python3 /project/src/train.py"

cd ../scripts || exit 1