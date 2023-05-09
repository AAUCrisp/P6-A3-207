#!/bin/bash

mkdir -p testdata

for file in $(ls tests); do
    ./scripts/runner.sh --verbose --config=tests/"$file" --dbname="$(basename "$file" .json)"
    for node in up0@192.168.1.61 up1@192.168.1.80 up2@192.168.1.107 up3@192.168.1.251; do 
        ip=${node#*"@"}
        name=${node%%@*}
        #sshpass -p 123 ssh root@"$node" ip route flush dev enp3s0
        mkdir -p testdata/"$(basename "$file" .json)"

        sshpass -p 123 sftp "$name"@"$ip":/tmp/P6-A3-207/screenlog.0 testdata/"$(basename "$file" .json)"/"$name".log
    done
    cp /tmp/P6-A3-207/include/db.db3 testdata/"$(basename "$file" .json)"/db.db3
    sleep 120
done