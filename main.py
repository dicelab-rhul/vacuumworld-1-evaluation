#!/usr/bin/python

import evaluator_mind as em
import evaluator_brain as ebr
import evaluator_body as eb
import evaluator_sensor as es
import evaluator_actuator as ea
import evaluation_environment as ee
import evaluation_physics as ep

__author__ = "cloudstrife9999, A.K.A. Emanuele Uliana"


def main():
    body_id = "my_evaluator_agent"
    mind = em.EvaluatorMind(body_id)
    brain = ebr.EvaluatorBrain()
    sensors = [es.EvaluatorSensor(body_id)]
    actuators = [ea.EvaluatorActuator()]
    body = eb.EvaluatorBody(body_id, mind, brain, sensors, actuators)
    environment = ee.EvaluationEnvironment([body])
    physics = ep.EvaluationPhysics()

    for sensor in sensors:
        environment.add_observer(sensor)

    for actuator in actuators:
        actuator.add_observer(environment)

    environment.add_observer(physics)
    physics.add_observer(environment)

    # example
    # no perceive on first cycle

    strategy = {
        "actor_to_evaluate": 0,
        "strategy_name": "linear",
        "successful_physical_coefficient": 4,
        "impossible_physical_coefficient": 10,
        "failed_physical_coefficient": 10,
        "successful_sensing_coefficient": 0,
        "impossible_sensing_coefficient": 0,
        "failed_sensing_coefficient": 0,
        "successful_communication_coefficient": 0,
        "impossible_communication_coefficient": 0,
        "failed_communication_coefficient": 0,
    }

    action = mind.decide(**strategy)
    mind.execute(action)

    # next cycle
    mind.perceive()
    strategy["actor_to_evaluate"] += 1
    print str(mind.get_last_action_result().get_score())
    action = mind.decide(**strategy)
    mind.execute(action)

    mind.perceive()
    print str(mind.get_last_action_result().get_score())

    # and so on...

if __name__ == "__main__":
    main()
