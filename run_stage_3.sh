#!/bin/bash

if [[ $# -lt 3 ]]
  then
    echo "usage: ./run_stage_3.sh <model-jar-path> <model-json-path> <initial-state-jsons-folder-path>"
    exit -1
  else
    for i in `seq 51 100`
    do
        f=$3/test-${i}.json
        echo ${f}
        GRID_SIZE=$(python evaluation/get_grid_size_from_json_file.py ${f} 2>&1)
        DIRTS_NUMBER=$(python evaluation/get_dirts_number_from_json_file.py ${f} 2>&1)
        initial=${f}
        dir=$(dirname ${f})
        student_id=$(basename ${dir})

        if [[ ${GRID_SIZE} -eq "3" ]]
            then
                RUN_CYCLE_LIMIT=$((8 + ${DIRTS_NUMBER} + ${GRID_SIZE}*${DIRTS_NUMBER}/3 + ${GRID_SIZE}*${GRID_SIZE}/3))
                EVALUATION_CYCLE_LIMIT=${RUN_CYCLE_LIMIT}
        elif [[ ${GRID_SIZE} -eq "4" ]]
            then
                RUN_CYCLE_LIMIT=$((13 + ${DIRTS_NUMBER} + ${GRID_SIZE}*${DIRTS_NUMBER}/3 + ${GRID_SIZE}*${GRID_SIZE}/3))
                EVALUATION_CYCLE_LIMIT=${RUN_CYCLE_LIMIT}
        elif [[ ${GRID_SIZE} -eq "5" ]]
            then
                RUN_CYCLE_LIMIT=$((18 + ${DIRTS_NUMBER} + ${GRID_SIZE}*${DIRTS_NUMBER}/3 + ${GRID_SIZE}*${GRID_SIZE}/3))
                EVALUATION_CYCLE_LIMIT=${RUN_CYCLE_LIMIT}
        elif [[ ${GRID_SIZE} -eq "6" ]]
            then
                RUN_CYCLE_LIMIT=$((18 + ${DIRTS_NUMBER} + ${GRID_SIZE}*${DIRTS_NUMBER}/3 + ${GRID_SIZE}*${GRID_SIZE}/3))
                EVALUATION_CYCLE_LIMIT=${RUN_CYCLE_LIMIT}
        elif [[ ${GRID_SIZE} -eq "7" ]]
            then
                RUN_CYCLE_LIMIT=$((28 + ${DIRTS_NUMBER} + ${GRID_SIZE}*${DIRTS_NUMBER}/3 + ${GRID_SIZE}*${GRID_SIZE}/3))
                EVALUATION_CYCLE_LIMIT=${RUN_CYCLE_LIMIT}
        elif [[ ${GRID_SIZE} -eq "8" ]]
            then
                RUN_CYCLE_LIMIT=$((33 + ${DIRTS_NUMBER} + ${GRID_SIZE}*${DIRTS_NUMBER}/3 + ${GRID_SIZE}*${GRID_SIZE}/3))
                EVALUATION_CYCLE_LIMIT=${RUN_CYCLE_LIMIT}
        elif [[ ${GRID_SIZE} -eq "9" ]]
            then
                RUN_CYCLE_LIMIT=$((38 + ${DIRTS_NUMBER} + ${GRID_SIZE}*${DIRTS_NUMBER}/3 + ${GRID_SIZE}*${GRID_SIZE}/3))
                EVALUATION_CYCLE_LIMIT=${RUN_CYCLE_LIMIT}
        elif [[ ${GRID_SIZE} -eq "10" ]]
            then
                RUN_CYCLE_LIMIT=$((48 + ${DIRTS_NUMBER} + ${GRID_SIZE}*${DIRTS_NUMBER}/3 + ${GRID_SIZE}*${GRID_SIZE}/3))
                EVALUATION_CYCLE_LIMIT=${RUN_CYCLE_LIMIT}
        fi

        echo "launching 'java -jar $1 --delay-in-seconds 1 --config-file $2 --initial-state-file ${initial} --max-cycles-number ${RUN_CYCLE_LIMIT}'"
        java -jar $1 --delay-in-seconds 1 --config-file $2 --initial-state-file ${initial} --max-cycles-number ${RUN_CYCLE_LIMIT}
        ./evaluate_stage_3.sh ${student_id} ${EVALUATION_CYCLE_LIMIT}
        mongo < clear_db.js
    done
fi