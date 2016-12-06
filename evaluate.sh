#!/bin/bash

if [[ $# -lt 2 ]]
  then
    echo "usage: ./evaluate.sh <actor-to-evaluate-id> <cycle-limit-for-stage-1>"
    exit -1
  else
    ./main.py -c evaluation.json -a $1 -u $2 -s 2
fi