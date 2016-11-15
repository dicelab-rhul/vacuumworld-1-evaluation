from pymongo import MongoClient

__author__ = "cloudstrife9999, A.K.A. Emanuele Uliana"


class DBManager:
    def __init__(self, mongo_vars, eval_vars):
        self.__mongo_vars = mongo_vars
        self.__conf = mongo_vars.get_db_vars()
        self.__hostname = self.__conf["hostname"]
        self.__port = self.__conf["port"]
        self.__db_name = self.__conf["db_name"]
        self.__states_collection_name = self.__conf["states_collection"]
        self.__actions_collection_name = self.__conf["actions_collection"]
        self.__client = MongoClient(self.__conf["mongodb"] + "://" + self.__hostname + ":" + self.__port)
        self.__database = self.__client[self.__db_name]
        self.__states_collection = self.__database[self.__states_collection_name]
        self.__actions_collection = self.__database[self.__actions_collection_name]
        self.__eval_vars = eval_vars

    def reopen_connection(self):
        if self.__client is None:
            self.__client = MongoClient(self.__conf["mongodb"] + "://" + self.__hostname + ":" + self.__port)
            self.__database = self.__client[self.__db_name]
            self.__states_collection = self.__database[self.__states_collection_name]
            self.__actions_collection = self.__database[self.__actions_collection_name]

    def close_connection(self):
        if self.__client.server_info() is not None:
            self.__client.close()
            self.__client = None
            self.__database = None
            self.__states_collection = None
            self.__actions_collection = None

    def reset_database(self):
        self.__states_collection.remove({})
        self.__actions_collection.remove({})

    def get_hostname(self):
        return self.__hostname

    def get_port(self):
        return self.__port

    def get_db_name(self):
        return self.__db_name

    def get_states_collection_name(self):
        return self.__states_collection_name

    def get_actions_collection_name(self):
        return self.__actions_collection_name

    def get_states_for_all_cycles(self):
        return self.__states_collection.find()

    def get_state_for_specific_cycle(self, cycle_number):
        return self.__states_collection.find_one({self.__mongo_vars.get_state_cycle_key(): int(cycle_number)})

    def get_actions_reports_for_all_cycles(self):
        return self.__actions_collection.find()

    def get_all_actors_actions_in_specific_cycle(self, cycle_number):
        return self.__actions_collection.find_one(
            filter={self.__mongo_vars.get_actions_report_cycle_key(): int(cycle_number)},
            projection={
                self.__mongo_vars.get_actions_report_id_key(): 0,
                self.__mongo_vars.get_actions_report_cycle_key(): 1,
                self.__mongo_vars.get_actions_report_actors_number_key(): 1,
                self.__mongo_vars.get_actions_report_actions_key(): 1
            }
        )

    def get_specific_actor_action_in_specific_cycle(self, cycle_number, actor_id):
        return self.__actions_collection.find_one(
            filter={self.__mongo_vars.get_actions_report_cycle_key(): int(cycle_number)},
            projection={
                self.__mongo_vars.get_actions_report_id_key(): 0,
                self.__mongo_vars.get_actions_report_actions_key(): {
                    "$elemMatch": {self.__mongo_vars.get_actions_report_action_actor_id_key(): actor_id}
                }
            }
        )["actions"][0]

    def get_specific_actor_actions_in_all_cycles(self, actor_id):
        return self.__actions_collection.aggregate(
            pipeline=[
                {
                    "$project": {
                        self.__mongo_vars.get_actions_report_id_key(): 0,
                        self.__mongo_vars.get_actions_report_actions_key(): 1,
                        self.__mongo_vars.get_actions_report_cycle_key(): 1
                    }
                },
                {
                    "$unwind": "$" + self.__mongo_vars.get_actions_report_actions_key()
                },
                {
                    "$match": {
                        self.__mongo_vars.get_actions_report_actions_key() + "." +
                        self.__mongo_vars.get_actions_report_action_actor_id_key(): actor_id
                    }
                },
                {
                    "$group": {
                        self.__mongo_vars.get_aggregations_id_key(): self.__mongo_vars.get_actions_report_cycle_key(),
                        self.__mongo_vars.get_aggregations_action_key(): {
                            "$push": "$" + self.__mongo_vars.get_actions_report_actions_key()
                        }
                    }
                },
                {
                    "$sort": {
                        self.__mongo_vars.get_aggregations_id_key(): 1
                    }
                },
                {
                    "$project": {
                        self.__mongo_vars.get_aggregations_id_key(): 0,
                        self.__mongo_vars.get_aggregations_action_key(): 1
                    }
                },
                {
                    "$unwind": "$" + self.__mongo_vars.get_aggregations_action_key()
                }
            ]
        )

    def get_actors_names(self):
        return [value[self.__mongo_vars.get_aggregations_id_key()] for value in
                self.__actions_collection.aggregate(
                    pipeline=[
                        {
                            "$match": {
                                self.__mongo_vars.get_actions_report_cycle_key(): 1
                            }
                        },
                        {
                            "$project": {
                                self.__mongo_vars.get_actions_report_id_key(): 0,
                                self.__mongo_vars.get_actions_report_actions_key() + "." +
                                self.__mongo_vars.get_actions_report_action_actor_id_key(): 1
                            }
                        },
                        {
                            "$unwind": "$" + self.__mongo_vars.get_actions_report_actions_key()
                        },
                        {
                            "$group": {
                                self.__mongo_vars.get_aggregations_id_key():
                                    "$" + self.__mongo_vars.get_actions_report_actions_key() + "." +
                                    self.__mongo_vars.get_actions_report_action_actor_id_key()
                            }
                        }
                    ]
                )
                ]

    def count_specific_actor_successful_actions_in_all_cycles(self, actor_id):
        for result in self.__actions_collection.aggregate(
            pipeline=[
                {
                    "$unwind": "$" + self.__mongo_vars.get_actions_report_actions_key()
                },
                {
                    "$match": {
                        self.__mongo_vars.get_actions_report_actions_key() + "." +
                        self.__mongo_vars.get_actions_report_action_actor_id_key(): actor_id,
                        self.__mongo_vars.get_actions_report_actions_key() + "." +
                        self.__mongo_vars.get_actions_report_action_outcome_key():
                            self.__mongo_vars.get_action_success_outcome_value()
                    }
                },
                {
                    "$group": {
                        self.__mongo_vars.get_aggregations_id_key(): "$" +
                        self.__mongo_vars.get_actions_report_action_actor_id_key(),
                        self.__mongo_vars.get_aggregations_count_key(): {
                            "$sum": 1
                        }
                    }
                },
                {
                    "$project": {
                        self.__mongo_vars.get_aggregations_id_key(): 0,
                        self.__mongo_vars.get_aggregations_count_key(): 1
                    }
                }
            ]
        ):
            return result[self.__mongo_vars.get_aggregations_count_key()]

    def count_specific_actor_impossible_actions_in_all_cycles(self, actor_id):
        for result in self.__actions_collection.aggregate(
            pipeline=[
                {
                    "$unwind": "$" + self.__mongo_vars.get_actions_report_actions_key()
                },
                {
                    "$match": {
                        self.__mongo_vars.get_actions_report_actions_key() + "." +
                        self.__mongo_vars.get_actions_report_action_actor_id_key(): actor_id,
                        self.__mongo_vars.get_actions_report_actions_key() + "." +
                        self.__mongo_vars.get_actions_report_action_outcome_key():
                            self.__mongo_vars.get_action_impossible_outcome_value()
                    }
                },
                {
                    "$group": {
                        self.__mongo_vars.get_aggregations_id_key(): "$" +
                        self.__mongo_vars.get_actions_report_action_actor_id_key(),
                        self.__mongo_vars.get_aggregations_count_key(): {
                            "$sum": 1
                        }
                    }
                },
                {
                    "$project": {
                        self.__mongo_vars.get_aggregations_id_key(): 0,
                        self.__mongo_vars.get_aggregations_count_key(): 1
                    }
                }
            ]
        ):
            return result[self.__mongo_vars.get_aggregations_count_key()]

    def count_specific_actor_failed_actions_in_all_cycles(self, actor_id):
        for result in self.__actions_collection.aggregate(
            pipeline=[
                {
                    "$unwind": "$" + self.__mongo_vars.get_actions_report_actions_key()
                },
                {
                    "$match": {
                        self.__mongo_vars.get_actions_report_actions_key() + "." +
                        self.__mongo_vars.get_actions_report_action_actor_id_key(): actor_id,
                        self.__mongo_vars.get_actions_report_actions_key() + "." +
                        self.__mongo_vars.get_actions_report_action_outcome_key():
                            self.__mongo_vars.get_action_failed_outcome_value()
                    }
                },
                {
                    "$group": {
                        self.__mongo_vars.get_aggregations_id_key(): "$" +
                        self.__mongo_vars.get_actions_report_action_actor_id_key(),
                        self.__mongo_vars.get_aggregations_count_key(): {
                            "$sum": 1
                        }
                    }
                },
                {
                    "$project": {
                        self.__mongo_vars.get_aggregations_id_key(): 0,
                        self.__mongo_vars.get_aggregations_count_key(): 1
                    }
                }
            ]
        ):
            return result[self.__mongo_vars.get_aggregations_count_key()]

    def count_number_of_successful_actions_in_specific_cycle(self, cycle_number):
        for result in self.__actions_collection.aggregate(
            pipeline=[
                {
                    "$unwind": "$" + self.__mongo_vars.get_actions_report_actions_key()
                },
                {
                    "$match": {
                        self.__mongo_vars.get_actions_report_cycle_key(): cycle_number,
                        self.__mongo_vars.get_actions_report_actions_key() + "." +
                        self.__mongo_vars.get_actions_report_action_outcome_key():
                            self.__mongo_vars.get_action_success_outcome_value()
                    }
                },
                {
                    "$group": {
                        self.__mongo_vars.get_aggregations_id_key(): "$" +
                        self.__mongo_vars.get_actions_report_cycle_key(),
                        self.__mongo_vars.get_aggregations_count_key(): {
                            "$sum": 1
                        }
                    }
                },
                {
                    "$project": {
                        self.__mongo_vars.get_aggregations_id_key(): 0,
                        self.__mongo_vars.get_aggregations_count_key(): 1
                    }
                }
            ]
        ):
            return result[self.__mongo_vars.get_aggregations_count_key()]

    def count_number_of_impossible_actions_in_specific_cycle(self, cycle_number):
        for result in self.__actions_collection.aggregate(
            pipeline=[
                {
                    "$unwind": "$" + self.__mongo_vars.get_actions_report_actions_key()
                },
                {
                    "$match": {
                        self.__mongo_vars.get_actions_report_cycle_key(): cycle_number,
                        self.__mongo_vars.get_actions_report_actions_key() + "." +
                        self.__mongo_vars.get_actions_report_action_outcome_key():
                            self.__mongo_vars.get_action_impossible_outcome_value()
                    }
                },
                {
                    "$group": {
                        self.__mongo_vars.get_aggregations_id_key(): "$" +
                        self.__mongo_vars.get_actions_report_cycle_key(),
                        self.__mongo_vars.get_aggregations_count_key(): {
                            "$sum": 1
                        }
                    }
                },
                {
                    "$project": {
                        self.__mongo_vars.get_aggregations_id_key(): 0,
                        self.__mongo_vars.get_aggregations_count_key(): 1
                    }
                }
            ]
        ):
            return result[self.__mongo_vars.get_aggregations_count_key()]

    def count_number_of_failed_actions_in_specific_cycle(self, cycle_number):
        for result in self.__actions_collection.aggregate(
            pipeline=[
                {
                    "$unwind": "$" + self.__mongo_vars.get_actions_report_actions_key()
                },
                {
                    "$match": {
                        self.__mongo_vars.get_actions_report_cycle_key(): cycle_number,
                        self.__mongo_vars.get_actions_report_actions_key() + "." +
                        self.__mongo_vars.get_actions_report_action_outcome_key():
                            self.__mongo_vars.get_action_failed_outcome_value()
                    }
                },
                {
                    "$group": {
                        self.__mongo_vars.get_aggregations_id_key(): "$" +
                        self.__mongo_vars.get_actions_report_cycle_key(),
                        self.__mongo_vars.get_aggregations_count_key(): {
                            "$sum": 1
                        }
                    }
                },
                {
                    "$project": {
                        self.__mongo_vars.get_aggregations_id_key(): 0,
                        self.__mongo_vars.get_aggregations_count_key(): 1
                    }
                }
            ]
        ):
            return result[self.__mongo_vars.get_aggregations_count_key()]
