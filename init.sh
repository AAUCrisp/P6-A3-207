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
            echo "Error, not running on one of the UP boards..."
    esac
fi




fucking shit fuck... this work?