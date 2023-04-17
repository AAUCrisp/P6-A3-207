echo "Running init for user \"$USER\""

case $USER in
    "up1")
        sudo ip ad add 10.0.0.10 dev enp3s0
        ;;
    "up2")
        sudo ip ad add 10.0.0.20 dev enp3s0
        ;;
    "up3")
        sudo ip ad add 10.0.0.30 dev enp3s0
        ;;
    "up0")
        sudo ip ad add 10.0.0.40 dev enp3s0
        ;;
    *)
        echo "Error, not running on one of the UP boards..."
esac