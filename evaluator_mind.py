from db_manager import *
from custom_observer import CustomObserver
from custom_observable import CustomObservable
from evaluator_brain import EvaluatorBrain
from actions.evaluate_action import EvaluateAction
from actions.result import EvaluationResult


class EvaluatorMind(CustomObservable, CustomObserver):
    def __init__(self, body_id):
        CustomObservable.__init__(self)
        self.__body_id = body_id
        self.__last_action_result = None
        self.__additional_results = []

    def perceive(self):
        self.notify_specific_type_observers(None, EvaluatorBrain)

    def decide(self, **kwargs):
        kwargs["pippo"] = "pluto"  # todo

        return EvaluateAction(self.__body_id, **kwargs)

    def execute(self, action):
        if isinstance(action, EvaluateAction):
            self.notify_specific_type_observers(action, EvaluatorBrain)
        else:
            raise ValueError("Unexpected action type: " + str(type(action)) + ".")

    def update(self, custom_observable, payload):
        if isinstance(custom_observable, EvaluatorBrain):
            self.__manage_brain_request(payload)
        else:
            raise ValueError("Unexpected observable type: " + str(type(custom_observable)) + ".")

    def __manage_brain_request(self, payload):
        if isinstance(payload, list):
            self.__manage_brain_data(payload)

    def __manage_brain_data(self, data):
        if len(data) < 1:
            raise ValueError("Got empty results list from brain.")
        elif isinstance(data[0], EvaluationResult):
            self.__last_action_result = data[0]
            self.__store_other_results(data)
        else:
            raise ValueError("Unexpected data from brain: " + str(type(data[0])) + ".")

    def __store_other_results(self, data):
        if len(data) == 1:
            return
        else:
            self.__additional_results = data[1:]
