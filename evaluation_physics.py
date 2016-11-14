from custom_observer import CustomObserver
from custom_observable import CustomObservable
from evaluation_environment import EvaluationEnvironment
from physics_interface import AbstractPhysics
from actions.evaluate_action import EvaluateAction
from actions.result import EvaluationResult
from actions.outcomes import *


class EvaluationPhysics(CustomObservable, CustomObserver, AbstractPhysics):
    def __init__(self):
        CustomObservable.__init__(self)
        self.__possible = {EvaluateAction: True}
        self.__succeeded = {EvaluateAction: True}

    def update(self, custom_observable, payload):
        if isinstance(custom_observable, EvaluationEnvironment):
            self.__manage_environment_request(custom_observable, payload)
        else:
            raise ValueError("Unexpected observable type: " + str(type(custom_observable)) + ".")

    def __manage_environment_request(self, context, payload):
        if isinstance(payload, EvaluateAction):
            result = payload.attempt(self, context)
            self.notify_specific_type_observers(result, EvaluationEnvironment)
        else:
            raise ValueError("Unexpected payload type: " + str(type(payload)) + ".")

    def is_possible(self, evaluate_action, context):
        if isinstance(evaluate_action, EvaluateAction) and isinstance(context, EvaluationEnvironment):
            return True
        else:
            return evaluate_action.get_kwargs() is not None \
                   and evaluate_action.get_kwargs() != [] \
                   and self.__possible[EvaluateAction]

    def perform(self, evaluate_action, context):
        if not isinstance(evaluate_action, EvaluateAction) or not isinstance(context, EvaluationEnvironment):
            return EvaluationResult(None, failed, evaluate_action.get_body_id())
        else:
            return self.__do_evaluation(evaluate_action)

    def __do_evaluation(self, evaluate_action):
        if self.__succeeded[EvaluateAction]:
            # todo
            return EvaluationResult(10, succeeded, evaluate_action.get_body_id())
        else:
            return EvaluationResult(None, failed, evaluate_action.get_body_id())

    def succeeded(self, evaluate_action, context):
        if isinstance(evaluate_action, EvaluateAction) and isinstance(context, EvaluationEnvironment):
            return self.__succeeded[EvaluateAction]
        else:
            return False
