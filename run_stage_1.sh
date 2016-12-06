#!/bin/bash

if [[ $# -lt 3 ]]
  then
    echo "usage: ./run_stage_1.sh <model-jar-path> <model-json-path> <initial-state-jsons-folder-path>"
    exit -1
  else
    FILES=$3/test-[12345678].json
    for f in ${FILES}
    do
        initial=${f}
        dir=$(dirname ${f})
        student_id=$(basename ${dir})
        f=$(basename ${f})
        f=${f%.*}
        f=${f:5}

        if [[ ${f} -eq "1" ]]
            then
                RUN_CYCLE_LIMIT="8"
                EVALUATION_CYCLE_LIMIT="3"
        elif [[ ${f} -eq "2" ]]
            then
                RUN_CYCLE_LIMIT="13"
                EVALUATION_CYCLE_LIMIT="8"
        elif [[ ${f} -eq "3" ]]
            then
                RUN_CYCLE_LIMIT="18"
                EVALUATION_CYCLE_LIMIT="11"
        elif [[ ${f} -eq "4" ]]
            then
                RUN_CYCLE_LIMIT="18"
                EVALUATION_CYCLE_LIMIT="14"
        elif [[ ${f} -eq "5" ]]
            then
                RUN_CYCLE_LIMIT="28"
                EVALUATION_CYCLE_LIMIT="21"
        elif [[ ${f} -eq "6" ]]
            then
                RUN_CYCLE_LIMIT="33"
                EVALUATION_CYCLE_LIMIT="26"
        elif [[ ${f} -eq "7" ]]
            then
                RUN_CYCLE_LIMIT="38"
                EVALUATION_CYCLE_LIMIT="31"
        elif [[ ${f} -eq "8" ]]
            then
                RUN_CYCLE_LIMIT="48"
                EVALUATION_CYCLE_LIMIT="43"
        fi

        echo "launching 'java -jar $1 --delay-in-seconds 1 --config-file $2 --initial-state-file ${initial} --max-cycles-number ${RUN_CYCLE_LIMIT}'"
        java -jar $1 --delay-in-seconds 1 --config-file $2 --initial-state-file ${initial} --max-cycles-number ${RUN_CYCLE_LIMIT}
        ./evaluate_stage_1.sh ${student_id} ${EVALUATION_CYCLE_LIMIT}
        mongo < clear_db.js
    done
fi