class EvaluationVariables:
    def __init__(self):
        self.__eval_vars_dict = {}

    def populate(self, dictionary):
        self.__eval_vars_dict = dictionary

    def get_strategy_keys(self):
        return self.__eval_vars_dict["evaluation_strategy_keys"]

    def get_strategy_name_key(self):
        return self.__eval_vars_dict["evaluation_strategy_keys"]["strategy_name_key"]

    def get_actor_to_evaluate_key(self):
        return self.__eval_vars_dict["evaluation_strategy_keys"]["actor_to_evaluate_key"]

    def get_successful_ph_cost_key(self):
        return self.get_strategy_keys()["successful_physical_coefficient_key"]

    def get_impossible_ph_cost_key(self):
        return self.get_strategy_keys()["impossible_physical_coefficient_key"]

    def get_failed_ph_cost_key(self):
        return self.get_strategy_keys()["failed_physical_coefficient_key"]

    def get_successful_sen_cost_key(self):
        return self.get_strategy_keys()["successful_sensing_coefficient_key"]

    def get_impossible_sen_cost_key(self):
        return self.get_strategy_keys()["impossible_sensing_coefficient_key"]

    def get_failed_sen_cost_key(self):
        return self.get_strategy_keys()["failed_sensing_coefficient_key"]

    def get_successful_com_cost_key(self):
        return self.get_strategy_keys()["successful_communication_coefficient_key"]

    def get_impossible_com_cost_key(self):
        return self.get_strategy_keys()["impossible_communication_coefficient_key"]

    def get_failed_com_cost_key(self):
        return self.get_strategy_keys()["failed_communication_coefficient_key"]

    def get_strategy_values(self):
        return self.__eval_vars_dict["evaluation_strategy_values"]

    def get_physical_actions(self):
        return self.__eval_vars_dict["evaluation_strategy_values"]["physical_actions"]

    def get_sensing_actions(self):
        return self.__eval_vars_dict["evaluation_strategy_values"]["sensing_actions"]

    def get_communication_actions(self):
        return self.__eval_vars_dict["evaluation_strategy_values"]["communication_actions"]

    def get_linear_strategy(self):
        return self.__eval_vars_dict["evaluation_strategy_values"]["linear_strategy"]

    def get_linear_strategy_name(self):
        return self.__eval_vars_dict["evaluation_strategy_values"]["linear_strategy"]["strategy_name"]

    def get_successful_ph_cost(self):
        return self.get_linear_strategy()["successful_physical_coefficient"]

    def get_impossible_ph_cost(self):
        return self.get_linear_strategy()["impossible_physical_coefficient"]

    def get_failed_ph_cost(self):
        return self.get_linear_strategy()["failed_physical_coefficient"]

    def get_successful_sen_cost(self):
        return self.get_linear_strategy()["successful_sensing_coefficient"]

    def get_impossible_sen_cost(self):
        return self.get_linear_strategy()["impossible_sensing_coefficient"]

    def get_failed_sen_cost(self):
        return self.get_linear_strategy()["failed_sensing_coefficient"]

    def get_successful_com_cost(self):
        return self.get_linear_strategy()["successful_communication_coefficient"]

    def get_impossible_com_cost(self):
        return self.get_linear_strategy()["impossible_communication_coefficient"]

    def get_failed_com_cost(self):
        return self.get_linear_strategy()["failed_communication_coefficient"]
