#!/bin/sh
while true
do
        process1=$(ps -ef | grep ksdns-168.py | grep -v grep);
        if [ "$process1" = "" ]; then
                echo "kdns-168.py not running";
                nohup python3 ksdns-168.py & 
        else
                echo "ksdns-168.py is running";
        fi
        process2=$(ps -ef | grep ksdns-8.8.py | grep -v grep);
        if [ "$process2" = "" ]; then
                echo "kdns-8.8.py not running";
                nohup python3 ksdns-8.8.py & 
        else
                echo "ksdns-8.8.py is running";
        fi
done
