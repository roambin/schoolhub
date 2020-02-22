#!/bin/bash
command=$1
if [ -z "$command" ] || [ $command == "y" ];then
    cd ~/backend
    source venv/bin/activate
    nohup python3 run.py &
    echo 'started'
elif [ $command == "n" ];then
    pkill python3
    echo 'stopped'
else
    cd ~/backend
    source venv/bin/activate
    pkill python3
    nohup python3 run.py &
    echo "restarted"
fi

