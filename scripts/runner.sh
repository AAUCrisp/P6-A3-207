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
        "ip":"192.168.1.61",
        "port":8888
    },
    "up1":{
        "ip":"192.168.1.80",
        "port":8889
    },
    "up2":{
        "ip":"192.168.1.107",
        "port":8890
    },
    "up3":{
        "ip":"192.168.1.251",
        "port":8891
    },
    "cal":{
        "ip":"192.168.1.189",
        "port":8892
    },
    "ste":{
        "ip":"192.168.1.76",
        "port":8893
    },
    "tho":{
        "ip":"192.168.1.176",
        "port":8894
    },
    "ub8":{
        "ip":"192.168.1.182",
        "port":8895
    }
}'
verbose=0
nodes=()
configPath="scripts/configuration.json"
dbName="db$(ls dbs | wc -l).db3"


# argument parsing
for arg in "$@"; do
    if [[ "$arg" == --topology* ]]; then # Node setup parsed in a json formatted string with layout: '{"up0":{"type":"backend"}, "up1":{"type":"headend", "target":"up0"}, "up2":{"type":"sensor", "target":"up1"}}'
        topology=${arg#*"="}
        nodes=("$(echo "$topology" | jq -c '.[]')")
    elif [[ "$arg" == --config* ]]; then
        configPath=${arg#*"="}
    elif [[ "$arg" == --verbose ]]; then
        verbose=1
    elif [[ "$arg" == --dbname* ]]; then
        dbName="${arg#*"="}.db3"
    fi
done

# read config file
config=$(cat "$configPath")

# parse nodes if they weren't set by arguments
if [ "$topology" == "" ]; then
    nodes=("$(echo "$config" | jq -r -c '.topology[]')")
fi

function runNode(){
    # Extract node name
    name=$(echo "$node" | jq -r -c .name)

    # Extract ip address 
    ip=$(echo "$mapping" | jq -r -c ."$name".ip)

    # Set username for ssh
    if [ "$(echo "$node" | jq -r -c .username)" != "null" ]; then
        username="$(echo "$node" | jq -r -c .username)"
    else
        username="$name"
    fi
    # extract password
    password="$(echo "$node" | jq -r -c .password)"

    # extract arguments OR return an empty variable if its null
    if [ "$(echo "$node" | jq -r -c .args)" != "null" ]; then
        args=$(echo "$node" | jq -r -c '.args | join(" ")')
    else
        args=""
    fi

    if [ "$verbose" == 1 ]; then
        echo "Running Node: $username@$ip with args [${args[*]}]"
    fi
    setupCmd="
        cd /tmp || exit
        rm -r P6-A3-207 
        git clone https://github.com/AAUCrisp/P6-A3-207.git
        cd P6-A3-207 || exit
        cp include/db_empty.db3 include/db.db3
        screen -L -dmS node " # VERY IMPORTANT: this string has to end on this line with a space otherwise the parsed command will fail

    echo "$setupCmd $cmd ${args[*]}" | sshpass -p "$password" ssh "$username@$ip" 'bash -s'
}

# Main Section
# Start by extracting each type so they can be run individually
for node in ${nodes[*]}; do
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
        *)
            printf "\033[38;2;255;0;0mError\033[0m: No such type '%s'\n" "$(echo "$node" | jq -c '.type')"
            ;;
    esac
done
if [ "$verbose" == 1 ]; then
    printf "\033[1mBackends\033[0m: %s\n" "${backends[*]}"
    printf "\033[1mHeadends\033[0m: %s\n" "${headends[*]}"
    printf "\033[1mSensors\033[0m: %s\n" "${sensors[*]}"
fi

# run a backend in a screen on each backend node
for node in ${backends[*]}; do
    inPort="$(echo "$mapping" | jq -r -c ."$(echo "$node" | jq -r -c .name)".port)"
    if [ $verbose == 1 ]; then
        echo "Backend listening on $inPort"
    fi
    cmd="python3.11 backend.py -portIn $inPort"
    runNode
done

# run a headend in a screen on each headend node
for node in ${headends[*]}; do
    target="$(echo "$node" | jq -r -c .target)"
    inPort="$(echo "$mapping" | jq -r -c ."$(echo "$node" | jq -r -c .name)".port)"
    outPort="$(echo "$mapping" | jq -r -c ."$target".port)"
    if [ $verbose == 1 ]; then
        echo "Connecting headend to -$target on port $outPort. Listening on $inPort"
    fi
    cmd="python3.11 headend.py -portIn $inPort -portOut $outPort -target $target"
    runNode
done

# run a sensor in a screen on each sensor node
for node in ${sensors[*]}; do
    target="$(echo "$node" | jq -r -c .target)"
    outPort="$(echo "$mapping" | jq -r -c ."$target".port)"
    if [ $verbose == 1 ]; then
        echo "Connecting sensor to $target on port $outPort."
    fi
    cmd="python3.11 sensor.py -portOut $outPort -target $target"
    runNode
done

# wait for a predetermined period as described in the configuration file
period="$(echo "$config" | jq -c -r .period)"
echo "Sleeping for $period seconds..."
sleep "$period"

# shutdown each node in the reverse order
for node in ${sensors[*]}; do
    name=$(echo "$node" | jq -c -r .name)
    ip=$(echo "$mapping" | jq -c -r ."$name".ip)
    if [ "$(echo "$node" | jq -c -r .username)" != "null" ]; then
        username="$(echo "$node" | jq -c -r .username)"
    else
        username="$name"
    fi
    password="$(echo "$node" | jq -c -r .password)"

    if [ "$verbose" == 1 ]; then
        printf "Shutting down sensor node \033[38;2;255;75;0m%s\033[0m\n" "$username@$ip"
    fi

    if [ "$password" == "null" ]; then
        ssh "$username@$ip" "screen -S node -X at \# stuff $'\003'"
    else
        sshpass -p "$password" ssh "$username@$ip" "screen -S node -X at \# stuff $'\003'"
        sshpass -p "$password" ssh "$username@$ip" "cat /tmp/P6-A3-207/screenlog.0 " > log/"$name".log
    fi
done

for node in ${headends[*]}; do
    name=$(echo "$node" | jq -c -r .name)
    ip=$(echo "$mapping" | jq -c -r ."$name".ip)
    if [ "$(echo "$node" | jq -c -r .username)" != "null" ]; then
        username="$(echo "$node" | jq -c -r .username)"
    else
        username="$name"
    fi
    if [ "$verbose" == 1 ]; then
        printf "Shutting down headend node \033[38;2;255;75;0m%s\033[0m\n" "$username@$ip"
    fi
    password="$(echo "$node" | jq -c -r .password)"
    if [ "$password" == "null" ]; then
        ssh "$username@$ip" "screen -S node -X at \# stuff $'\003'"
    else
        sshpass -p "$password" ssh "$username@$ip" "screen -S node -X at \# stuff $'\003'"
        sshpass -p "$password" ssh "$username@$ip" "cat /tmp/P6-A3-207/screenlog.0 " > log/"$name".log
    fi
done

for node in ${backends[*]}; do
    name=$(echo "$node" | jq -c -r .name)
    ip=$(echo "$mapping" | jq -c -r ."$name".ip)
    if [ "$(echo "$node" | jq -c -r .username)" != "null" ]; then
        username="$(echo "$node" | jq -c -r .username)"
    else
        username="$name"
    fi
    if [ "$verbose" == 1 ]; then
        printf "Shutting down backend node \033[38;2;255;75;0m%s\033[0m\n" "$username@$ip"
    fi
    password="$(echo "$node" | jq -c -r .password)"
    if [ "$password" == "null" ]; then
        ssh "$username@$ip" "screen -S node -X at \# stuff $'\003'"
    else
        sshpass -p "$password" ssh "$username@$ip" "screen -S node -X at \# stuff $'\003'"
        sshpass -p "$password" ssh "$username@$ip" "cat /tmp/P6-A3-207/screenlog.0 " > log/"$name".log
        sshpass -p "$password" ssh "$username@$ip" "cat /tmp/P6-A3-207/include/db.db3" >> dbs/"$dbName"
    fi
done

exit 0