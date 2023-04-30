#!/bin/bash

if [ "$1" == "help" ]; then
    printf "\033[1mUsage\033[0m:\t\t./scripts/runner.sh --topology=jsonFormattedString --verbose

\033[1mExample 1\033[0m:\t./scripts/runner.sh --topology='[{\"name\":\"up0\", \"type\":\"backend\"}, {\"name\":\"up1\", \"type\":\"headend\", \"target\":\"up0\"}, {\"name\":\"up2\", \"type\":\"sensor\", \"target\":\"up1\"}]'
\033[1mExample 2\033[0m:\t./scripts/runner.sh --topology=scripts/topology.json

\033[1mArguments\033[0m:
\t\033[38;2;255;75;0m--topology\033[0m\tSets the topology of the testbed, it can be a json formatted string or the path to a file containing the string
\t\033[38;2;255;75;0m--config\033[0m\tSets the configuration path
\t\033[38;2;255;75;0m--verbose\033[0m\tSets verbose output
"
    exit 0
fi


# define a table of corresponding names and ip addresses
mapping='{
    "up0":{
        "ip":"192.168.1.105"
    },
    "up1":{
        "ip":"192.168.1.80"
    },
    "up2":{
        "ip":"192.168.1.107"
    },
    "up3":{
        "ip":"192.168.1.109"
    },
    "cal":{
        "ip":"192.168.1.189"
    },
    "ste":{
        "ip":"192.168.1.76"
    },
    "tho":{
        "ip":"192.168.1.176"
    },
    "ub8":{
        "ip":"192.168.1.182"
    }
}'
verbose=0
nodes=()
configPath="scripts/configuration.json"


# argument parsing
for arg in "$@"; do
    if [[ "$arg" == --topology* ]]; then # Node setup parsed in a json formatted string with layout: '{"up0":{"type":"backend"}, "up1":{"type":"headend", "target":"up0"}, "up2":{"type":"sensor", "target":"up1"}}'
        topology=${arg#*"="}
        nodes=("$(echo "$topology" | jq -c '.[]')")
    elif [[ "$arg" == --config* ]]; then
        configPath=${arg#*"="}
    elif [[ "$arg" == --verbose ]]; then
        verbose=1
    fi
done

# read config file
config=$(cat "$configPath")

# parse nodes if they weren't set by arguments
if [ "$topology" == "" ]; then
    nodes=("$(echo "$config" | jq -r -c '.topology[]')")
fi

# Main Section
# Start by extracting each type so they can be run individually
for node in "${nodes[@]}"; do
    case "$(echo "$node" | jq -c '.type')" in
        '"backend"')
            backends+=("$node")
            ;;
        '"headend"')
            headends+=("$node")
            ;;
        '"sensor"')
            sensors+=("$node")
            ;;
    esac
done
if [ "$verbose" == 1 ]; then
    printf "\033[1mBackends\033[0m: %s\n" "${backends[@]}"
    printf "\033[1mHeadends\033[0m: %s\n" "${headends[@]}"
    printf "\033[1mSensors\033[0m: %s\n" "${sensors[@]}"
fi

# run a backend in a screen on each backend node
for backend in "${backends[@]}"; do
    name=$(echo "$backend" | jq -c -r .name)
    ip=$(echo "$mapping" | jq -c -r ."$name".ip)
    if [ "$verbose" == 1 ]; then
        printf "Running node \033[38;2;255;75;0m%s\033[0m as a backend\n" "$name@$ip"
    fi
    if [ "$(echo "$backend" | jq -c -r .args)" == "null" ]; then
        ssh "$name"@"$ip" "cd /tmp && git clone https://github.com/AAUCrisp/P6-A3-207 && cd P6-A3-207 && screen -dmS backend python3.10 backend.py"
    else
        echo "cd /tmp && git clone https://github.com/AAUCrisp/P6-A3-207 && cd P6-A3-207 && screen -dmS backend python3.10 backend.py $(echo "$backend" | jq -c -r .args[])" | ssh "$name"@"$ip" 'bash -s'
    fi
done

# run a headend in a screen on each headend node
for headend in "${headends[@]}"; do
    name=$(echo "$headend" | jq -c -r .name)
    ip=$(echo "$mapping" | jq -c -r ."$name".ip)
    if [ "$verbose" == 1 ]; then
        printf "Running node \033[38;2;255;75;0m%s\033[0m as a headend\n" "$name@$ip"
    fi
    if [ "$(echo "$headend" | jq -c -r .args)" == "null" ]; then
        ssh "$name"@"$ip" "cd /tmp && git clone https://github.com/AAUCrisp/P6-A3-207 && cd P6-A3-207 && screen -dmS headend python3.10 headend.py"
    else
        echo "cd /tmp && git clone https://github.com/AAUCrisp/P6-A3-207 && cd P6-A3-207 && screen -dmS headend python3.10 headend.py $(echo "$headend" | jq -c -r .args[])" | ssh "$name"@"$ip" 'bash -s' 
    fi
done

# run a sensor in a screen on each sensor node
for sensor in "${sensors[@]}"; do
    name=$(echo "$sensor" | jq -c -r .name)
    ip=$(echo "$mapping" | jq -c -r ."$name".ip)
    if [ "$verbose" == 1 ]; then
        printf "Running node \033[38;2;255;75;0m%s\033[0m as a sensor\n" "$name@$ip"
    fi
    if [ "$(echo "$sensor" | jq -c -r .args)" == "null" ]; then
        ssh "$name"@"$ip" "cd /tmp && git clone https://github.com/AAUCrisp/P6-A3-207 && cd P6-A3-207 && screen -dmS sensor python3.10 sensor.py"
    else
        echo "cd /tmp && git clone https://github.com/AAUCrisp/P6-A3-207 && cd P6-A3-207 && screen -dmS sensor python3.10 sensor.py $(echo "$sensor" | jq -c -r .args[])" | ssh "$name"@"$ip" 'bash -s'
    fi
done

# wait for a predetermined period as described in the configuration file
sleep "$(echo "$config" | jq -c -r .period)"

# shutdown each node in the reverse order
for sensor in "${sensors[@]}"; do
    name=$(echo "$sensor" | jq -c -r .name)
    ip=$(echo "$mapping" | jq -c -r ."$name".ip)
    if [ "$verbose" == 1 ]; then
        printf "Shutting down sensor node \033[38;2;255;75;0m%s\033[0m\n" "$name@$ip"
    fi
    ssh "$name"@"$ip" "screen -S sensor -X at \# stuff $'\003'"
done

for headend in "${headends[@]}"; do
    name=$(echo "$headend" | jq -c -r .name)
    ip=$(echo "$mapping" | jq -c -r ."$name".ip)
    if [ "$verbose" == 1 ]; then
        printf "Shutting down headend node \033[38;2;255;75;0m%s\033[0m\n" "$name@$ip"
    fi
    ssh "$name"@"$ip" "screen -S headend -X at \# stuff $'\003'"
done

for backend in "${backends[@]}"; do
    name=$(echo "$backend" | jq -c -r .name)
    ip=$(echo "$mapping" | jq -c -r ."$name".ip)
    if [ "$verbose" == 1 ]; then
        printf "Shutting down backend node \033[38;2;255;75;0m%s\033[0m\n" "$name@$ip"
    fi
    ssh "$name"@"$ip" "screen -S backend -X at \# stuff $'\003'"
done