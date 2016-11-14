#!/usr/bin/python

import evaluator_mind as em
import evaluator_brain as ebr
import evaluator_body as eb
import evaluator_sensor as es
import evaluator_actuator as ea
import evaluation_environment as ee
import evaluation_physics as ep
import evaluation_keywords as ekw

__author__ = "cloudstrife9999, A.K.A. Emanuele Uliana"


def __add_observers(sensors, actuators, environment):
    for sensor in sensors:
        environment.add_observer(sensor)

    for actuator in actuators:
        actuator.add_observer(environment)


def __create_evaluator():
    body_id = "my_evaluator_agent"
    mind = em.EvaluatorMind(body_id)
    brain = ebr.EvaluatorBrain()
    sensors = [es.EvaluatorSensor(body_id)]
    actuators = [ea.EvaluatorActuator()]
    body = eb.EvaluatorBody(body_id, mind, brain, sensors, actuators)
    environment, physics = __create_universe([body])

    __add_observers(sensors, actuators, environment)

    return mind


def __create_universe(bodies):
    environment = ee.EvaluationEnvironment(bodies)
    physics = ep.EvaluationPhysics()

    environment.add_observer(physics)
    physics.add_observer(environment)

    return environment, physics


def __create_strategy():
    return {
        ekw.actor_to_evaluate_key: 0,
        ekw.strategy_name_key: ekw.linear_strategy,
        ekw.successful_physical_coefficient_key: 4,
        ekw.impossible_physical_coefficient_key: 10,
        ekw.failed_physical_coefficient_key: 10,
        ekw.successful_sensing_coefficient_key: 0,
        ekw.impossible_sensing_coefficient_key: 0,
        ekw.failed_sensing_coefficient_key: 0,
        ekw.successful_communication_coefficient_key: 0,
        ekw.impossible_communication_coefficient_key: 0,
        ekw.failed_communication_coefficient_key: 0,
    }


def main():
    mind = __create_evaluator()
    strategy = __create_strategy()

    # first cycle, no perceive, first actor evaluation
    action = mind.decide(**strategy)
    mind.execute(action)

    # next cycle, second actor evaluation
    mind.perceive()
    strategy[ekw.actor_to_evaluate_key] += 1
    print "First actor score: " + str(mind.get_last_action_result().get_score())
    action = mind.decide(**strategy)
    mind.execute(action)

    # next cycle, only perceive
    mind.perceive()
    print "Second actor score: " + str(mind.get_last_action_result().get_score())


if __name__ == "__main__":
    main()
