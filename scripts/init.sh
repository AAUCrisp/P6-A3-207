#!/bin/bash

if [ "$1" == "help" ]; then
    printf "\033[1mUsage\033[0m:\t\t./scripts/init.sh

\033[1mCommands\033[0m:
    \033[38;2;255;75;0mhelp\033[0m:\tShows the current help message.

\033[1mDescription\033[0m:\tThis script is used to set the ip addresses of this system, it should be executed by a non-root user to ensure the naming of the device follows the correct ip address. 
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
