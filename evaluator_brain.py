from custom_observer import CustomObserver
from custom_observable import CustomObservable
from actions.evaluate_action import EvaluateAction
from evaluator_mind import EvaluatorMind
from evaluator_body import EvaluatorBody
from actions.result import EvaluationResult


class EvaluatorBrain(CustomObservable, CustomObserver):
    def __init__(self):
        CustomObservable.__init__(self)
        self.__accumulator = []
        self.__results_for_mind = []

    def update(self, custom_observable, payload):
        if isinstance(custom_observable, EvaluatorMind):
            self.__manage_mind_request(payload)
        elif isinstance(custom_observable, EvaluatorBody):
            self.__manage_body_request(payload)
        else:
            raise ValueError("Unexpected observable type: " + str(type(custom_observable)) + ".")

    def __manage_mind_request(self, payload):
        if payload is None:
            self.__notify_mind()
        elif isinstance(payload, EvaluateAction):
            self.notify_specific_type_observers(payload, EvaluatorBody)
        else:
            raise ValueError("Unexpected payload type: " + str(type(payload)) + ".")

    def __notify_mind(self):
        self.__results_for_mind = []

        for result in self.__accumulator:
            self.__results_for_mind.append(result)

        self.__accumulator = []

        self.notify_specific_type_observers(self.__results_for_mind, EvaluatorMind)

    def __manage_body_request(self, payload):
        if isinstance(payload, EvaluationResult):
            self.__accumulator.append(payload)
        else:
            raise ValueError("Unexpected payload type: " + str(type(payload)) + ".")
