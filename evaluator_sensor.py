from custom_observer import CustomObserver
from custom_observable import CustomObservable
from evaluator_body import EvaluatorBody
from evaluation_environment import EvaluationEnvironment
from actions.result import EvaluationResult


class EvaluatorSensor(CustomObservable, CustomObserver):
    def __init__(self, body_id):
        CustomObservable.__init__(self)
        self.__body_id = body_id

    def get_body_id(self):
        return self.__body_id

    def update(self, custom_observable, payload):
        if isinstance(custom_observable, EvaluationEnvironment):
            self.__manage_environment_request(payload)
        else:
            raise ValueError("Unexpected observable type: " + str(type(custom_observable)) + ".")

    def __manage_environment_request(self, payload):
        if isinstance(payload, EvaluationResult):
            self.notify_specific_type_observers(payload, EvaluatorBody)
        else:
            raise ValueError("Unexpected payload type: " + str(type(payload)) + ".")
