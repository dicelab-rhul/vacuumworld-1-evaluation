from custom_observer import CustomObserver
from custom_observable import CustomObservable
from evaluator_body import EvaluatorBody
from evaluation_environment import EvaluationEnvironment
from actions.evaluate_action import EvaluateAction


class EvaluatorActuator(CustomObservable, CustomObserver):
    def __init__(self):
        CustomObservable.__init__(self)

    def update(self, custom_observable, payload):
        if isinstance(custom_observable, EvaluatorBody):
            self.__manage_body_request(payload)
        else:
            raise ValueError("Unexpected observable type: " + str(type(custom_observable)) + ".")

    def __manage_body_request(self, payload):
        if isinstance(payload, EvaluateAction):
            self.notify_specific_type_observers(payload, EvaluationEnvironment)
        else:
            raise ValueError("Unexpected payload type: " + str(type(payload)) + ".")
