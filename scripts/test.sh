#!/bin/bash

mkdir -p testdata

for file in $(ls tests); do
    ./scripts/runner.sh --verbose --config=tests/"$file" --dbname="$(basename "$file" .json)"
    for node in "192.168.1.61" "192.168.1.80" "192.168.1.107" "192.168.1.251" ; do
        #sshpass -p 123 ssh root@"$node" ip route flush dev enp3s0
        mkdir -p testdata/"$(basename "$file" .json)"

        sshpass -p 123 sftp root@"$node":/tmp/P6-A3-207/include/db.db3 testdata/"$(basename "$file" .json)"/db.db3
        sshpass -p 123 sftp root@"$node":/tmp/P6-A3-207/screenlog.0 testdata/"$(basename "$file" .json)"/"$node".log
    done
    sleep 120
done