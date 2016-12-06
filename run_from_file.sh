#!/bin/bash

java -jar model.jar --delay-in-seconds 1 --config-file model.json --initial-state-file states_examples/initial_state.json --max-cycles-number 20
