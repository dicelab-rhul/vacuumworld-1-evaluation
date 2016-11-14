from custom_observer import CustomObserver
from custom_observable import CustomObservable
from evaluator_brain import EvaluatorBrain
from evaluator_actuator import EvaluatorActuator
from evaluator_sensor import EvaluatorSensor
from actions.evaluate_action import EvaluateAction
from actions.result import EvaluationResult


class EvaluatorBody(CustomObservable, CustomObserver):
    def __init__(self):
        CustomObservable.__init__(self)

    def update(self, custom_observable, payload):
        if isinstance(custom_observable, EvaluatorBrain):
            self.__manage_brain_request(payload)
        elif isinstance(custom_observable, EvaluatorSensor):
            self.__manage_sensor_request(payload)
        else:
            raise ValueError("Unexpected observable type: " + str(type(custom_observable)) + ".")

    def __manage_brain_request(self, payload):
        if isinstance(payload, EvaluateAction):
            self.notify_specific_type_observers(payload, EvaluatorActuator)
        else:
            raise ValueError("Unexpected payload type: " + str(type(payload)) + ".")

    def __manage_sensor_request(self, payload):
        if isinstance(payload, EvaluationResult):
            self.notify_specific_type_observers(payload, EvaluatorBrain)
        else:
            raise ValueError("Unexpected payload type: " + str(type(payload)) + ".")
