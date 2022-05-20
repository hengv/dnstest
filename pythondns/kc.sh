#!/bin/sh
while true
do
        process=$(ps -ef | grep pydns-168.py | grep -v grep);
        if [ "$process" = "" ]; then
                sleep 5;
                echo "not running";
                nohup python3 /root/pythondns/pydns-168.py & 
        else
                sleep 5;
                echo "is running";
        fi
done
