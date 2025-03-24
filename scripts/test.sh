#!/bin/bash
cd ../docker || exit 1

source ./.env

ACTIVE_PROJECT=${1:-$ACTIVE_PROJECT}
docker compose run --rm project sh

cd ../scripts || exit 1