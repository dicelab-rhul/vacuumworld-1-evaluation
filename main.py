#!/usr/bin/python

import evaluator_mind as em
import evaluator_brain as ebr
import evaluator_body as eb
import evaluator_sensor as es
import evaluator_actuator as ea
import evaluation_environment as ee
import evaluation_physics as ep
import argparse as ap
import json_parser as jp

__author__ = "cloudstrife9999, A.K.A. Emanuele Uliana"


def __add_observers(sensors, actuators, environment):
    for sensor in sensors:
        environment.add_observer(sensor)

    for actuator in actuators:
        actuator.add_observer(environment)


def __create_evaluator(mongo_vars, eval_vars):
    body_id = "my_evaluator_agent"
    mind = em.EvaluatorMind(body_id, mongo_vars)
    brain = ebr.EvaluatorBrain()
    sensors = [es.EvaluatorSensor(body_id)]
    actuators = [ea.EvaluatorActuator()]
    body = eb.EvaluatorBody(body_id, mind, brain, sensors, actuators)
    environment, physics = __create_universe([body], mongo_vars, eval_vars)

    __add_observers(sensors, actuators, environment)

    return mind


def __create_universe(bodies, mongo_vars, eval_vars):
    environment = ee.EvaluationEnvironment(bodies)
    physics = ep.EvaluationPhysics(mongo_vars, eval_vars)

    environment.add_observer(physics)
    physics.add_observer(environment)

    return environment, physics


def __create_strategy(eval_vars):
    return {
        eval_vars.get_actor_to_evaluate_key(): 0,
        eval_vars.get_strategy_name_key(): eval_vars.get_linear_strategy_name(),
        eval_vars.get_successful_ph_cost_key(): eval_vars.get_successful_ph_cost(),
        eval_vars.get_impossible_ph_cost_key(): eval_vars.get_impossible_ph_cost(),
        eval_vars.get_failed_ph_cost_key(): eval_vars.get_failed_ph_cost(),
        eval_vars.get_successful_sen_cost_key(): eval_vars.get_successful_sen_cost(),
        eval_vars.get_impossible_sen_cost_key(): eval_vars.get_impossible_sen_cost(),
        eval_vars.get_failed_sen_cost_key(): eval_vars.get_failed_sen_cost(),
        eval_vars.get_successful_com_cost_key(): eval_vars.get_successful_com_cost(),
        eval_vars.get_impossible_com_cost_key(): eval_vars.get_impossible_com_cost(),
        eval_vars.get_failed_com_cost_key(): eval_vars.get_failed_com_cost()
    }


def __parse_arguments():
    parser = ap.ArgumentParser(description='VacuumWorld Evaluator')
    parser.add_argument('-c', '--config-file',
                        required=True,
                        metavar='<config-file-path>', type=str,
                        action='store',
                        help='JSON configuration file')

    return parser.parse_args()


def __start_system(mongo_vars, eval_vars):
    mind = __create_evaluator(mongo_vars, eval_vars)
    strategy = __create_strategy(eval_vars)

    # first cycle, no perceive, first actor evaluation
    action = mind.decide(**strategy)
    mind.execute(action)

    # next cycle, second actor evaluation
    mind.perceive()
    strategy[eval_vars.get_actor_to_evaluate_key()] += 1
    print "First actor score: " + str(mind.get_last_action_result().get_score())
    action = mind.decide(**strategy)
    mind.execute(action)

    # next cycle, only perceive
    mind.perceive()
    print "Second actor score: " + str(mind.get_last_action_result().get_score())


def __run_system(config_file):
    mongo_vars, eval_vars = jp.parse(config_file)

    if mongo_vars == {} or eval_vars == {}:
        print "Error in parsing configuration from JSON file!"
        print "Bye!!!"
    else:
        __start_system(mongo_vars, eval_vars)


def main():
    args = __parse_arguments()
    config_file = args.config_file

    __run_system(config_file)


if __name__ == "__main__":
    main()
