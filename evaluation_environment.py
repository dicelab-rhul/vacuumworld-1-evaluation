from custom_observer import CustomObserver
from custom_observable import CustomObservable
from evaluator_actuator import EvaluatorActuator
from evaluator_sensor import EvaluatorSensor
from evaluation_physics import EvaluationPhysics
from actions.evaluate_action import EvaluateAction
from actions.result import EvaluationResult


class EvaluationEnvironment(CustomObservable, CustomObserver):
    def __init__(self):
        CustomObservable.__init__(self)

    def update(self, custom_observable, payload):
        if isinstance(custom_observable, EvaluatorActuator):
            self.__manage_actuator_request(payload)
        elif isinstance(custom_observable, EvaluationPhysics):
            self.__manage_physics_request(payload)
        else:
            raise ValueError("Unexpected observable type: " + str(type(custom_observable)) + ".")

    def __manage_actuator_request(self, payload):
        if isinstance(payload, EvaluateAction):
            self.notify_specific_type_observers(payload, EvaluationPhysics)
        else:
            raise ValueError("Unexpected payload type: " + str(type(payload)) + ".")

    def __manage_physics_request(self, payload):
        if isinstance(payload, EvaluationResult):
            self.__notify_right_sensor(payload)
        else:
            raise ValueError("Unexpected payload type: " + str(type(payload)) + ".")

    def __notify_right_sensor(self, result):
        for observer in self.get_specific_type_observers(EvaluatorSensor):
            if observer.get_body_id() == result.get_body_id():
                observer.update(self, result)
