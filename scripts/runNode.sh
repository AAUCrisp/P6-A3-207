#!/bin/bash

cd /tmp || exit
rm -r P6-A3-207 
git clone https://github.com/AAUCrisp/P6-A3-207.git
cd P6-A3-207 || exit
screen -L -dmS node