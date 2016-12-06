#!/bin/bash

if [[ $# -lt 4 ]]
  then
    echo "usage: ./run_from_file.sh <model-jar-path> <model-json-path> <initial-state-json-path> <cycle-limit>"
    exit -1
  else
    java -jar $1 --delay-in-seconds 1 --config-file $2 --initial-state-file $3 --max-cycles-number $4
fi