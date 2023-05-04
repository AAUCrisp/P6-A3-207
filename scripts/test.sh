#!/bin/bash

sudo ip route flush default device enp3s0

for file in $(ls tests); do
./scripts/runner.sh --verbose --config=tests/"$file" --dbname="$(basename "$file" .json)"
sleep 120
done