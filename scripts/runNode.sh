#!/bin/bash

cd /tmp || exit
rm -r P6-A3-207 
git clone https://github.com/AAUCrisp/P6-A3-207 
git switch 32-bad-conditions-implementation
cd P6-A3-207 || exit
echo "$@"
screen -L -dmS node "$@"