from pymongo import MongoClient
from mongo_keywords import *
from outcomes import *

__author__ = "cloudstrife9999, A.K.A. Emanuele Uliana"


class DBManager:
    def __init__(self, hostname, port, db_name, states_collection, actions_collection):
        self.__hostname = hostname
        self.__port = port
        self.__db_name = db_name
        self.__states_collection_name = states_collection
        self.__actions_collection_name = actions_collection
        self.__client = MongoClient("mongodb://" + self.__hostname + ":" + self.__port)
        self.__database = self.__client[self.__db_name]
        self.__states_collection = self.__database[self.__states_collection_name]
        self.__actions_collection = self.__database[self.__actions_collection_name]

    def reopen_connection(self):
        if self.__client is None:
            self.__client = MongoClient("mongodb://" + self.__hostname + ":" + self.__port)
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
        return self.__states_collection.find_one({cycle_key: int(cycle_number)})

    def get_actions_reports_for_all_cycles(self):
        return self.__actions_collection.find()

    def get_all_actors_actions_in_specific_cycle(self, cycle_number):
        return self.__actions_collection.find_one(
            filter={cycle_key: int(cycle_number)},
            projection={id_key: 0, cycle_key: 1, actors_number_key: 1, actions_key: 1}
        )

    def get_specific_actor_action_in_specific_cycle(self, cycle_number, actor_id):
        return self.__actions_collection.find_one(
            filter={cycle_key: int(cycle_number)},
            projection={id_key: 0, actions_key: {"$elemMatch": {actor_id_key: actor_id}}}
        )["actions"][0]

    def get_specific_actor_actions_in_all_cycles(self, actor_id):
        return self.__actions_collection.aggregate(
            pipeline=[
                {"$project": {id_key: 0, actions_key: 1, cycle_key: 1}},
                {"$unwind": "$" + actions_key},
                {"$match": {actions_key + "." + actor_id_key: actor_id}},
                {"$group": {id_key: cycle_key, action_key: {"$push": "$" + actions_key}}},
                {"$sort": {id_key: 1}},
                {"$project": {id_key: 0, action_key: 1}},
                {"$unwind": "$" + action_key}
            ]
        )

    def get_actors_names(self):
        return [value[id_key] for value in
                self.__actions_collection.aggregate(
                    pipeline=[
                        {"$match": {cycle_key: 1}},
                        {"$project": {id_key: 0, actions_key + "." + actor_id_key: 1}},
                        {"$unwind": "$" + actions_key},
                        {"$group": {id_key: "$" + actions_key + "." + actor_id_key}}
                    ]
                )
                ]

    def count_specific_actor_successful_actions_in_all_cycles(self, actor_id):
        for result in self.__actions_collection.aggregate(
            pipeline=[
                {"$unwind": "$" + actions_key},
                {"$match": {
                                    actions_key + "." + actor_id_key: actor_id,
                                    actions_key + "." + action_outcome_key: succeeded
                }
                },
                {"$group": {id_key: "$" + actor_id_key, count_key: {"$sum": 1}}},
                {"$project": {id_key: 0, count_key: 1}}
            ]
        ):
            return result[count_key]

    def count_specific_actor_impossible_actions_in_all_cycles(self, actor_id):
        for result in self.__actions_collection.aggregate(
            pipeline=[
                {"$unwind": "$" + actions_key},
                {"$match": {
                                    actions_key + "." + actor_id_key: actor_id,
                                    actions_key + "." + action_outcome_key: impossible
                }
                },
                {"$group": {id_key: "$" + actor_id_key, count_key: {"$sum": 1}}},
                {"$project": {id_key: 0, count_key: 1}}
            ]
        ):
            return result[count_key]

    def count_specific_actor_failed_actions_in_all_cycles(self, actor_id):
        for result in self.__actions_collection.aggregate(
            pipeline=[
                {"$unwind": "$" + actions_key},
                {"$match": {
                                    actions_key + "." + actor_id_key: actor_id,
                                    actions_key + "." + action_outcome_key: failed
                }
                },
                {"$group": {id_key: "$" + actor_id_key, count_key: {"$sum": 1}}},
                {"$project": {id_key: 0, count_key: 1}}
            ]
        ):
            return result[count_key]

    def count_number_of_successful_actions_in_specific_cycle(self, cycle_number):
        for result in self.__actions_collection.aggregate(
            pipeline=[
                {"$unwind": "$" + actions_key},
                {"$match": {cycle_key: cycle_number, actions_key + "." + action_outcome_key: succeeded}},
                {"$group": {id_key: "$" + cycle_key, count_key: {"$sum": 1}}},
                {"$project": {id_key: 0, count_key: 1}}
            ]
        ):
            return result[count_key]

    def count_number_of_impossible_actions_in_specific_cycle(self, cycle_number):
        for result in self.__actions_collection.aggregate(
            pipeline=[
                {"$unwind": "$" + actions_key},
                {"$match": {cycle_key: cycle_number, actions_key + "." + action_outcome_key: impossible}},
                {"$group": {id_key: "$" + cycle_key, count_key: {"$sum": 1}}},
                {"$project": {id_key: 0, count_key: 1}}
            ]
        ):
            return result[count_key]

    def count_number_of_failed_actions_in_specific_cycle(self, cycle_number):
        for result in self.__actions_collection.aggregate(
            pipeline=[
                {"$unwind": "$" + actions_key},
                {"$match": {cycle_key: cycle_number, actions_key + "." + action_outcome_key: failed}},
                {"$group": {id_key: "$" + cycle_key, count_key: {"$sum": 1}}},
                {"$project": {id_key: 0, count_key: 1}}
            ]
        ):
            return result[count_key]
