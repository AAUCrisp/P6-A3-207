#!/bin/bash

if [ "$1" == "help" ]; then
    orange="\033[38;2;255;75;0m"
    green="\033[38;0;255;0m"
    bold="\033[1m"
    reset="\033[0m"
    printf "${bold}Usage${reset}:\t\t./scripts/init.sh

${bold}Commands${reset}:
    ${orange}help${reset}:\tShows the current help message.

${bold}Description${reset}:\tThis script is used to set the ip addresses of this system, it should be executed by a non-root user to ensure the naming of the device follows the correct ip address. 
\t\tThis script can be extended to allow more initialization\n"
    exit 0
fi


if [ $EUID == 0 ]; then
    printf "\033[38;2;255;0;0mError\033[0m: this script shouldn't be run with root access\n"
    exit 1
fi

echo "Running init for user \"$USER\""

if [[ "$(ip addr show dev enp3s0)" == *"10.0.0."* ]]; then
    echo "interface already has an address, removing it... run again to set the ip up"
    sudo ip addr flush dev enp3s0
else
    echo "setting up the ip address..."
        case $USER in
        "up1")
            sudo ip ad add 10.0.0.10/24 dev enp3s0
            echo "set ip address of $USER to 10.0.0.10"
            ;;
        "up2")
            sudo ip ad add 10.0.0.20/24 dev enp3s0
            echo "set ip address of $USER to 10.0.0.20"
            ;;
        "up3")
            sudo ip ad add 10.0.0.30/24 dev enp3s0
            echo "set ip address of $USER to 10.0.0.30"
            ;;
        "up0")
            sudo ip ad add 10.0.0.40/24 dev enp3s0
            echo "set ip address of $USER to 10.0.0.40"
            ;;
        *)
            printf "\033[38;2;255;0;0mError\033[0m: not running on one of the UP boards...\n"
    esac
fi
