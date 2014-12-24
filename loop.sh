#! /bin/bash
while read line; do
    echo -n "$line" > /dev/udp/127.0.0.1/11109;
    sleep 1;
done < $1;
