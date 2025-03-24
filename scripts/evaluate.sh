#!/bin/bash

VERSION_ARG=$1

cd ../docker
docker compose run --rm app python3 src/evaluate.py $VERSION_ARG
cd ../scripts
