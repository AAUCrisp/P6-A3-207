#!/bin/bash



function setDatarate() {
    printf "Setting datarate of the specified interface to: %s\n\trun now? (y/N): " "$value"
    cat > scripts/TrafficToll.yaml << EOF
#Begin scripts/TrafficToll.yaml

download:           ${value}
upload:             ${value}
download-minimum:   ${value}
upload-minimum:     ${value}

download-priority: 0
upload-priority: 0

#End scripts/TrafficToll.yaml
EOF
    read -r in
    if [ "$in" == "y" ] || [ "$in" == "Y" ]; then
        nmcli d
        printf "Specify the interface name, a table of devices should be defined above: "
        read -r interface
        tt "$interface" scripts/TrafficToll.yaml
    else
        printf "execute this script again with 'y' to the previous prompt or execute \033[38;2;150;150;150mtt\033[0m (installed with sudo \033[38;2;150;150;150mpip3.10 install traffictoll\033[0m or \033[38;2;150;150;150msudo pip3.10 install -r requirements\033[0m)\n"
    fi

}

############################## main section #############################
if [ $EUID != 0 ]; then
    echo "ERROR: This script needs root access"
    exit 1
fi

cmd=$1

if [ "$cmd" == "limit" ]; then
    setDatarate
else
    printf "No such command: \033[38;2;255;100;100m%s\033[0m\n" "$cmd"
    exit 1
fi