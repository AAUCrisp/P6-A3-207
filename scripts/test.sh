#!/bin/bash

mkdir -p testdata

for file in $(ls tests); do
    ./scripts/runner.sh --verbose --config=tests/"$file" --runName="$(basename "$file" .json)"
    sleep 240
done