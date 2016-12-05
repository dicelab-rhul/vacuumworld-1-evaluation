import custom_observable as coe
import custom_observer as cor
import evaluate_action as eva
import evaluation_environment as ee
import physics_interface as pi
import result as r

from pymongo.errors import PyMongoError
from db_manager import DBManager

__author__ = "cloudstrife9999, A.K.A. Emanuele Uliana"


class EvaluationPhysics(coe.CustomObservable, cor.CustomObserver, pi.AbstractPhysics):
    def __init__(self, mongo_vars, eval_vars):
        coe.CustomObservable.__init__(self)
        self.__possible = {eva.EvaluateAction: True}
        self.__succeeded = {eva.EvaluateAction: True}
        self.__mongo_vars = mongo_vars
        self.__eval_vars = eval_vars
        self.__manager = DBManager(self.__mongo_vars, self.__eval_vars)

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
            return r.EvaluationResult(None, self.__mongo_vars.get_action_failed_outcome_value(),
                                      evaluate_action.get_body_id(), self.__mongo_vars.get_action_outcomes_values())
        else:
            return self.__do_evaluation(evaluate_action)

    def __do_evaluation(self, evaluate_action):
        try:
            return self.__evaluate(evaluate_action)
        except PyMongoError:
            self.__manager.close_connection()

            return r.EvaluationResult(None, self.__mongo_vars.get_action_failed_outcome_value(),
                                      evaluate_action.get_body_id(), self.__mongo_vars.get_action_outcomes_values())

    def __evaluate(self, evaluate_action):
        self.__manager.reopen_connection()

        actors = self.__manager.get_actors_names()
        actor_id = evaluate_action.get_kwargs()[self.__eval_vars.get_actor_to_evaluate_key()]

        if actor_id not in actors:
            raise ValueError()

        return self.__do_actual_evaluation(evaluate_action, actor_id)

    def __do_actual_evaluation(self, evaluate_action, actor_id):
        cycle_limit = evaluate_action.get_kwargs()["cycle_limit"]

        return self.__evaluate_by_strategy(evaluate_action, actor_id, cycle_limit)

    def __evaluate_by_strategy(self, evaluate_action, actor_id, cycle_limit):
        if evaluate_action.get_kwargs()[self.__eval_vars.get_strategy_name_key()] ==\
                self.__eval_vars.get_linear_strategy_name():

            stage = int(evaluate_action.get_kwargs()["stage"])

            return self.__evaluate_with_linear_strategy(evaluate_action, actor_id, stage, cycle_limit)
        else:  # todo: for now only the linear strategy is implemented
            self.__manager.close_connection()

            return r.EvaluationResult(None, self.__mongo_vars.get_action_failed_outcome_value(),
                                      evaluate_action.get_body_id(), self.__mongo_vars.get_action_outcomes_values())

    def __evaluate_with_linear_strategy(self, evaluate_action, actor_id, stage, cycle_limit):
        cost = 0
        cycle_limit = self.__update_cycle_limit(cycle_limit, stage)
        actions = self.__manager.get_specific_actor_actions_in_all_cycles_until_limit(actor_id, cycle_limit)

        for action in actions:
            cost += self.__increment_cost_with_linear_strategy(evaluate_action, action)

        print actor_id + ": actions cost: " + str(cost)

        if stage == 1:
            missed_locations = self.__manager.count_number_of_missed_locations(actor_id, cycle_limit)
            print actor_id + ": missed locations cost: " + str(missed_locations)
            cost += missed_locations
        elif stage == 2:
            delta = self.__manager.get_dirts_number_at_cycle(cycle_limit)

            print actor_id + ": dirts delta cost: " + str(delta)
            cost += delta

        elif stage == 3:
            delta = 0

            for counter in range(cycle_limit + 1):
                dirts_before = self.__manager.get_dirts_number_at_cycle(counter)
                dirts_after = self.__manager.get_dirts_number_at_cycle(counter + 1)
                delta += dirts_after - dirts_before

            print actor_id + ": dirts delta cost: " + str(delta)
            cost += delta

        self.__manager.close_connection()

        return r.EvaluationResult(cost, self.__mongo_vars.get_action_success_outcome_value(),
                                  evaluate_action.get_body_id(), self.__mongo_vars.get_action_outcomes_values())

    def __update_cycle_limit(self, cycle_limit, stage):
        if stage != 2:
            return cycle_limit
        else:
            for i in range(cycle_limit + 1):
                if self.__manager.get_dirts_number_at_cycle(i) == 0:
                    return i

            return cycle_limit

    def __increment_cost_with_linear_strategy(self, evaluate_action, action):
        if action[self.__mongo_vars.get_aggregations_action_key()][self.__mongo_vars.get_actions_report_action_name_key()] in self.__eval_vars.get_physical_actions():
            return self.__add_cost_for_physical_action_with_linear_strategy(evaluate_action, action)
        elif action[self.__mongo_vars.get_aggregations_action_key()][self.__mongo_vars.get_actions_report_action_name_key()] in self.__eval_vars.get_sensing_actions():
            return self.__add_cost_for_sensing_action_with_linear_strategy(evaluate_action, action)
        elif action[self.__mongo_vars.get_aggregations_action_key()][self.__mongo_vars.get_actions_report_action_name_key()] in self.__eval_vars.get_communication_actions():
            return self.__add_cost_for_communication_action_with_linear_strategy(evaluate_action, action)
        else:
            raise ValueError("Unrecognized action name: " + action[self.__mongo_vars.get_actions_report_action_outcome_key()][self.__mongo_vars.get_actions_report_action_name_key()] + ".")

    def __add_cost_for_physical_action_with_linear_strategy(self, evaluate_action, action):
        if action[self.__mongo_vars.get_aggregations_action_key()][self.__mongo_vars.get_actions_report_action_outcome_key()] == self.__mongo_vars.get_action_success_outcome_value():
            return evaluate_action.get_kwargs()[self.__eval_vars.get_successful_ph_cost_key()]
        elif action[self.__mongo_vars.get_aggregations_action_key()][self.__mongo_vars.get_actions_report_action_outcome_key()] == self.__mongo_vars.get_action_impossible_outcome_value():
            return evaluate_action.get_kwargs()[self.__eval_vars.get_impossible_ph_cost_key()]
        elif action[self.__mongo_vars.get_aggregations_action_key()][self.__mongo_vars.get_actions_report_action_outcome_key()] == self.__mongo_vars.get_action_failed_outcome_value():
            return evaluate_action.get_kwargs()[self.__eval_vars.get_failed_ph_cost_key()]
        else:
            raise ValueError("Unrecognized action outcome: " + action[self.__mongo_vars.get_aggregations_action_key()][self.__mongo_vars.get_actions_report_action_outcome_key()] + ".")

    def __add_cost_for_sensing_action_with_linear_strategy(self, evaluate_action, action):
        if action[self.__mongo_vars.get_aggregations_action_key()][self.__mongo_vars.get_actions_report_action_outcome_key()] == self.__mongo_vars.get_action_success_outcome_value():
            return evaluate_action.get_kwargs()[self.__eval_vars.get_successful_sen_cost_key()]
        elif action[self.__mongo_vars.get_aggregations_action_key()][self.__mongo_vars.get_actions_report_action_outcome_key()] == self.__mongo_vars.get_action_impossible_outcome_value():
            return evaluate_action.get_kwargs()[self.__eval_vars.get_impossible_sen_cost_key()]
        elif action[self.__mongo_vars.get_aggregations_action_key()][self.__mongo_vars.get_actions_report_action_outcome_key()] == self.__mongo_vars.get_action_failed_outcome_value():
            return evaluate_action.get_kwargs()[self.__eval_vars.get_failed_sen_cost_key()]
        else:
            raise ValueError("Unrecognized action outcome: " + action[self.__mongo_vars.get_aggregations_action_key()][self.__mongo_vars.get_actions_report_action_outcome_key()] + ".")

    def __add_cost_for_communication_action_with_linear_strategy(self, evaluate_action, action):
        if action[self.__mongo_vars.get_aggregations_action_key()][self.__mongo_vars.get_actions_report_action_outcome_key()] == self.__mongo_vars.get_action_success_outcome_value():
            return evaluate_action.get_kwargs()[self.__eval_vars.get_successful_com_cost_key()]
        elif action[self.__mongo_vars.get_aggregations_action_key()][self.__mongo_vars.get_actions_report_action_outcome_key()] == self.__mongo_vars.get_action_impossible_outcome_value():
            return evaluate_action.get_kwargs()[self.__eval_vars.get_impossible_com_cost_key()]
        elif action[self.__mongo_vars.get_aggregations_action_key()][self.__mongo_vars.get_actions_report_action_outcome_key()] == self.__mongo_vars.get_action_failed_outcome_value():
            return evaluate_action.get_kwargs()[self.__eval_vars.get_failed_com_cost_key()]
        else:
            raise ValueError("Unrecognized action outcome: " + action[self.__mongo_vars.get_aggregations_action_key()][self.__mongo_vars.get_actions_report_action_outcome_key()] + ".")

    def succeeded(self, evaluate_action, context):
        if isinstance(evaluate_action, eva.EvaluateAction) and isinstance(context, ee.EvaluationEnvironment):
            return self.__succeeded[eva.EvaluateAction]
        else:
            return False
