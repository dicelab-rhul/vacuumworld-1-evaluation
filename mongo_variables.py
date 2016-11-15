class MongoVariables:
    def __init__(self):
        self.__mongo_vars_dict = {}

    def populate(self, dictionary):
        self.__mongo_vars_dict = dictionary

    def get_db_vars(self):
        return self.__mongo_vars_dict["mongo_config"]

    def get_mongodb_keys(self):
        return self.__mongo_vars_dict["mongodb_keys"]

    def get_actions_report_keys(self):
        return self.__mongo_vars_dict["mongodb_keys"]["actions_report_document_keys"]

    def get_actions_report_id_key(self):
        return self.__mongo_vars_dict["mongodb_keys"]["actions_report_document_keys"]["id_key"]

    def get_actions_report_cycle_key(self):
        return self.__mongo_vars_dict["mongodb_keys"]["actions_report_document_keys"]["cycle_key"]

    def get_actions_report_actors_number_key(self):
        return self.__mongo_vars_dict["mongodb_keys"]["actions_report_document_keys"]["actors_number_key"]

    def get_actions_report_actions_key(self):
        return self.__mongo_vars_dict["mongodb_keys"]["actions_report_document_keys"]["actions_key"]

    def get_actions_report_action_sub_keys(self):
        return self.__mongo_vars_dict["mongodb_keys"]["actions_report_document_keys"]["action_sub_keys"]

    def get_actions_report_action_actor_id_key(self):
        return self.get_actions_report_action_sub_keys()["actor_id_key"]

    def get_actions_report_action_outcome_key(self):
        return self.get_actions_report_action_sub_keys()["action_outcome_key"]

    def get_actions_report_action_name_key(self):
        return self.get_actions_report_action_sub_keys()["action_name_key"]

    def get_state_keys(self):
        return self.__mongo_vars_dict["mongodb_keys"]["state_document_keys"]

    def get_state_cycle_key(self):
        return self.__mongo_vars_dict["mongodb_keys"]["state_document_keys"]["cycle_key"]

    def get_state_location_keys(self):
        return self.__mongo_vars_dict["mongodb_keys"]["state_document_keys"]["location_sub_keys"]

    def get_state_location_agent_keys(self):
        return self.get_state_location_keys()["agent_sub_keys"]

    def get_state_location_dirt_keys(self):
        return self.get_state_location_keys()["dirt_sub_keys"]

    def get_aggregations_keys(self):
        return self.__mongo_vars_dict["mongodb_keys"]["aggregations_keys"]

    def get_aggregations_id_key(self):
        return self.__mongo_vars_dict["mongodb_keys"]["aggregations_keys"]["id_key"]

    def get_aggregations_count_key(self):
        return self.__mongo_vars_dict["mongodb_keys"]["aggregations_keys"]["count_key"]

    def get_aggregations_action_key(self):
        return self.__mongo_vars_dict["mongodb_keys"]["aggregations_keys"]["action_key"]

    def get_mongodb_values(self):
        return self.__mongo_vars_dict["mongodb_values"]

    def get_action_values(self):
        return self.__mongo_vars_dict["mongodb_values"]["action_values"]

    def get_action_names_values(self):
        return self.__mongo_vars_dict["mongodb_values"]["action_values"]["names"]

    def get_action_outcomes_values(self):
        return self.__mongo_vars_dict["mongodb_values"]["action_values"]["outcomes"]

    def get_action_success_outcome_value(self):
        return self.__mongo_vars_dict["mongodb_values"]["action_values"]["outcomes"][0]

    def get_action_impossible_outcome_value(self):
        return self.__mongo_vars_dict["mongodb_values"]["action_values"]["outcomes"][1]

    def get_action_failed_outcome_value(self):
        return self.__mongo_vars_dict["mongodb_values"]["action_values"]["outcomes"][2]

    def get_state_values(self):
        return self.__mongo_vars_dict["mongodb_values"]["state_values"]
