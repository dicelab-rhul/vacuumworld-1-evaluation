#!/bin/bash

if [[ $# -lt 2 ]]
  then
    echo "usage: ./evaluate_stage_2.sh <actor-to-evaluate-id> <cycle-limit>"
    exit -1
  else
    ./main.py -c evaluation.json -a $1 -u $2 -s 2
fi