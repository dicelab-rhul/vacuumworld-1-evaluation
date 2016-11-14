import custom_observable as coe
import custom_observer as cor
import evaluate_action as eva
import evaluation_environment as ee
import physics_interface as pi
import result as r
import mongo_keywords as mkw
import evaluation_keywords as ekw

from pymongo.errors import PyMongoError
from db_manager import DBManager
from outcomes import *

__author__ = "cloudstrife9999, A.K.A. Emanuele Uliana"


class EvaluationPhysics(coe.CustomObservable, cor.CustomObserver, pi.AbstractPhysics):
    def __init__(self):
        coe.CustomObservable.__init__(self)
        self.__possible = {eva.EvaluateAction: True}
        self.__succeeded = {eva.EvaluateAction: True}
        self.__manager = DBManager("127.0.0.1", "27017", "VacuumWorld", "states", "actions")

    def update(self, observable, payload):
        if isinstance(observable, ee.EvaluationEnvironment):
            self.__manage_environment_request(observable, payload)
        else:
            raise ValueError("Unexpected observable type: " + str(type(observable)) + ".")

    def __manage_environment_request(self, context, payload):
        if isinstance(payload, eva.EvaluateAction):
            result = payload.attempt(self, context)
            self.notify_specific_type_observers(result, ee.EvaluationEnvironment)
        else:
            raise ValueError("Unexpected payload type: " + str(type(payload)) + ".")

    def is_possible(self, evaluate_action, context):
        if isinstance(evaluate_action, eva.EvaluateAction) and isinstance(context, ee.EvaluationEnvironment):
            return True
        else:
            return evaluate_action.get_kwargs() is not None \
                   and evaluate_action.get_kwargs() != [] \
                   and self.__possible[eva.EvaluateAction]

    def perform(self, evaluate_action, context):
        if not isinstance(evaluate_action, eva.EvaluateAction) or not isinstance(context, ee.EvaluationEnvironment):
            return r.EvaluationResult(None, failed, evaluate_action.get_body_id())
        else:
            return self.__do_evaluation(evaluate_action)

    def __do_evaluation(self, evaluate_action):
        try:
            return self.__evaluate(evaluate_action)
        except PyMongoError:
            self.__manager.close_connection()

            return r.EvaluationResult(None, failed, evaluate_action.get_body_id())

    def __evaluate(self, action):
        self.__manager.reopen_connection()

        actors = self.__manager.get_actors_names()
        actor_to_evaluate_index = action.get_kwargs()[ekw.actor_to_evaluate_key]

        return self.__evaluate_helper(action, actors, actor_to_evaluate_index)

    def __evaluate_helper(self, action, actors, actor_to_evaluate_index):
        if len(actors) > actor_to_evaluate_index:
            return self.__do_actual_evaluation(action, actors, actor_to_evaluate_index)
        else:
            self.__manager.close_connection()

            return r.EvaluationResult(None, failed, action.get_body_id())

    def __do_actual_evaluation(self, action, actors, actor_to_evaluate_index):
        actions = self.__manager.get_specific_actor_actions_in_all_cycles(actors[actor_to_evaluate_index])

        return self.__evaluate_by_strategy(action, actions)

    def __evaluate_by_strategy(self, action, actions):
        if action.get_kwargs()[ekw.strategy_name_key] == ekw.linear_strategy:
            return self.__evaluate_with_linear_strategy(action, actions)
        else:  # todo: for now only the linear strategy is implemented
            self.__manager.close_connection()

            return r.EvaluationResult(None, failed, action.get_body_id())

    def __evaluate_with_linear_strategy(self, action, actions):
        cost = 0

        for a in actions:
            cost += _update_cost(action, a)

        self.__manager.close_connection()

        return r.EvaluationResult(cost, succeeded, action.get_body_id())

    def succeeded(self, evaluate_action, context):
        if isinstance(evaluate_action, eva.EvaluateAction) and isinstance(context, ee.EvaluationEnvironment):
            return self.__succeeded[eva.EvaluateAction]
        else:
            return False


def _update_cost(action, a):
    if a[mkw.action_key][mkw.action_name_key] in ekw.physical:
        return __add_cost_for_physical_action_with_linear_strategy(action, a)
    elif a[mkw.action_key][mkw.action_name_key] in ekw.sensing:
        return __add_cost_for_sensing_action_with_linear_strategy(action, a)
    elif a[mkw.action_key][mkw.action_name_key] in ekw.communication:
        return __add_cost_for_communication_action_with_linear_strategy(action, a)
    else:
        raise ValueError("Unrecognized action name: " + a[mkw.action_key][mkw.action_name_key] + ".")


def __add_cost_for_physical_action_with_linear_strategy(action, a):
    if a[mkw.action_key][mkw.action_outcome_key] == succeeded:
        return action.get_kwargs()[ekw.successful_physical_coefficient_key]
    elif a[mkw.action_key][mkw.action_outcome_key] == impossible:
        return action.get_kwargs()[ekw.impossible_physical_coefficient_key]
    elif a[mkw.action_key][mkw.action_outcome_key] == failed:
        return action.get_kwargs()[ekw.failed_physical_coefficient_key]
    else:
        raise ValueError("Unrecognized action outcome: " + a[mkw.action_key][mkw.action_outcome_key] + ".")


def __add_cost_for_sensing_action_with_linear_strategy(action, a):
    if a[mkw.action_key][mkw.action_outcome_key] == succeeded:
        return action.get_kwargs()[ekw.successful_sensing_coefficient_key]
    elif a[mkw.action_key][mkw.action_outcome_key] == impossible:
        return action.get_kwargs()[ekw.impossible_sensing_coefficient_key]
    elif a[mkw.action_key][mkw.action_outcome_key] == failed:
        return action.get_kwargs()[ekw.failed_sensing_coefficient_key]
    else:
        raise ValueError("Unrecognized action outcome: " + a[mkw.action_key][mkw.action_outcome_key] + ".")


def __add_cost_for_communication_action_with_linear_strategy(action, a):
    if a[mkw.action_key][mkw.action_outcome_key] == succeeded:
        return action.get_kwargs()[ekw.successful_communication_coefficient_key]
    elif a[mkw.action_key][mkw.action_outcome_key] == impossible:
        return action.get_kwargs()[ekw.impossible_communication_coefficient_key]
    elif a[mkw.action_key][mkw.action_outcome_key] == failed:
        return action.get_kwargs()[ekw.failed_communication_coefficient_key]
    else:
        raise ValueError("Unrecognized action outcome: " + a[mkw.action_key][mkw.action_outcome_key] + ".")
