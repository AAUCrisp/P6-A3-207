#!/bin/bash

datarate=1bps
HOST=localhost
PORT=10000

function limit() {
    printf "Setting datarate of the specified interface to: %s\n\trun now? (y/N): " "$datarate"
    cat > /tmp/TrafficToll.yaml << EOF
#Begin scripts/TrafficToll.yaml

download:           ${datarate}
upload:             ${datarate}
download-minimum:   ${datarate}
upload-minimum:     ${datarate}

download-priority: 0
upload-priority: 0

#End scripts/TrafficToll.yaml
EOF
    read -r in
    if [ "$in" == "y" ] || [ "$in" == "Y" ]; then
        nmcli d
        printf "Specify the interface name, a table of devices should be defined above: "
        read -r interface
        tt "$interface" /tmp/TrafficToll.yaml
    else
        printf "execute this script again with 'y' to the previous prompt or execute \033[38;2;150;150;150mtt\033[0m (installed with sudo \033[38;2;150;150;150mpip3.10 install traffictoll\033[0m or \033[38;2;150;150;150msudo pip3.10 install -r requirements\033[0m)\n"
    fi

}

function stressTest(){
    screen -dmS netcat nc --listen -p "$PORT" -c
    sleep 1
    exec 3<>/dev/tcp/"$HOST"/"$PORT"
    i=0
    while true; do
        i=$((i+1))
        echo -ne "$i\r" >&3
    done
}

############################## main section #############################
if [ $EUID != 0 ]; then
    printf "\033[38;2;255;0;0mERROR\033[0m: This script needs root access\n"
    if [ "$1" != "help" ]; then
        exit 1
    fi
fi
# Extract arguments
for arg in "$@"; do
    if [[ "$arg" == "$1" ]]; then
        continue
    elif [[ "$arg" == --datarate* ]]; then
        datarate=${arg#*"="}
    elif [[ "$arg" == --host* ]]; then
        HOST=${arg#*"="}
    elif [[ "$arg" == --port* ]]; then
        PORT=${arg#*"="}
    else
        printf "No such argument: \033[38;2;0;255;0m%s\033[0m, type './scripts/conditions.sh help' for help\n" "$arg"
        exit 1
    fi
done


if [ "$1" == "limit" ]; then
    limit
elif [ "$1" == "stress" ]; then
    stressTest
elif [ "$1" == "help" ]; then
    orange="\033[38;2;255;75;0m"
    green="\033[38;2;0;255;0m"
    bold="\033[1m"
    reset="\033[0m"
    printf "${bold}Usage${reset}:\t\t./scripts/conditions.sh <${orange}command${reset}> <${green}arg1${reset}>=<val1> <${green}arg2${reset}>=<val2> ...
${bold}Example${reset}:\t./scripts/conditions.sh stress --host=localhost --port=8888

${bold}Commands${reset}:
    ${orange}limit${reset}:\tLimit the datarate on a network interface using TrafficToll
    ${orange}stress${reset}:\tStress test the network by flooding it with UDP packets using NetCat
    ${orange}help${reset}:\tDisplay this help message

${bold}Arguments${reset}:
    ${green}--datarate${reset}:\tSpecify the datarate for the limit command
    ${green}--host${reset}:\tSpecify the host to use for the stress command
    ${green}--port${reset}:\tSpecify the port to use for the stress command
\n"
else
    printf "No such command: \033[38;2;255;75;0m%s\033[0m, type './scripts/conditions.sh help' for help\n" "$1"
    exit 1
fi
