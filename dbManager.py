from pymongo import MongoClient


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
        if self.__client.server_info() is None:
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
            self.__actions_collection = Nones

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
        return self.__states_collection.find_one({"cycle": int(cycle_number)})

    def get_actions_reports_for_all_cycles(self):
        return self.__actions_collection.find()

    def get_actions_report_for_specific_cycle(self, cycle_number):
        return self.__actions_collection.find_one({"cycle": int(cycle_number)})

    def get_all_actors_actions_in_specific_cycle(self, cycle_number):
        return self.__actions_collection.find_one(filter={"cycle": int(cycle_number)})

    def get_specific_actor_action_in_specific_cycle(self, cycle_number, actor_id):
        return self.__actions_collection.find_one(
            filter={"cycle": int(cycle_number)},
            projection={"_id": 0, "actions": {"$elemMatch": {"actor_id": actor_id}}}
        )["actions"][0]

    def get_specific_actor_actions_in_all_cycles(self, actor_id):
        return self.__actions_collection.aggregate(
            pipeline=[
                {"$project": {"_id": 0, "actions": 1, "cycle": 1}},
                {"$unwind": "$actions"},
                {"$match": {"actions.actor_id": actor_id}},
                {"$group": {"_id": "$cycle", "cycle_action": {"$push": "$actions"}}},
                {"$sort": {"_id": 1}},
                {"$project": {"_id": 0, "cycle_action": 1}},
                {"$unwind": "$cycle_action"}
            ]
        )

    def get_actors_names(self):
        return [value["_id"] for value in
                self.__actions_collection.aggregate(
                    pipeline=[
                        {"$match": {"cycle": 1}},
                        {"$project": {"_id": 0, "actions.actor_id": 1}},
                        {"$unwind": "$actions"},
                        {"$group": {"_id": "$actions.actor_id"}}
                    ]
                )
                ]

    def count_specific_actor_successful_actions_in_all_cycles(self, actor_id):
        for result in self.__actions_collection.aggregate(
            pipeline=[
                {"$unwind": "$actions"},
                {"$match": {"actions.actor_id": actor_id, "actions.outcome": "ACTION_DONE"}},
                {"$group": {"_id": "$actor_id", "count": {"$sum": 1}}},
                {"$project": {"_id": 0, "count": 1}}
            ]
        ):
            return result["count"]

    def count_specific_actor_impossible_actions_in_all_cycles(self, actor_id):
        for result in self.__actions_collection.aggregate(
            pipeline=[
                {"$unwind": "$actions"},
                {"$match": {"actions.actor_id": actor_id, "actions.outcome": "ACTION_IMPOSSIBLE"}},
                {"$group": {"_id": "$actor_id", "count": {"$sum": 1}}},
                {"$project": {"_id": 0, "count": 1}}
            ]
        ):
            return result["count"]

    def count_specific_actor_failed_actions_in_all_cycles(self, actor_id):
        for result in self.__actions_collection.aggregate(
            pipeline=[
                {"$unwind": "$actions"},
                {"$match": {"actions.actor_id": actor_id, "actions.outcome": "ACTION_FAILED"}},
                {"$group": {"_id": "$actor_id", "count": {"$sum": 1}}},
                {"$project": {"_id": 0, "count": 1}}
            ]
        ):
            return result["count"]

    def count_number_of_successful_actions_in_specific_cycle(self, cycle_number):
        for result in self.__actions_collection.aggregate(
            pipeline=[
                {"$unwind": "$actions"},
                {"$match": {"cycle": cycle_number, "actions.outcome": "ACTION_DONE"}},
                {"$group": {"_id": "$cycle", "count": {"$sum": 1}}},
                {"$project": {"_id": 0, "count": 1}}
            ]
        ):
            return result["count"]

    def count_number_of_impossible_actions_in_specific_cycle(self, cycle_number):
        for result in self.__actions_collection.aggregate(
            pipeline=[
                {"$unwind": "$actions"},
                {"$match": {"cycle": cycle_number, "actions.outcome": "ACTION_IMPOSSIBLE"}},
                {"$group": {"_id": "$cycle", "count": {"$sum": 1}}},
                {"$project": {"_id": 0, "count": 1}}
            ]
        ):
            return result["count"]

    def count_number_of_failed_actions_in_specific_cycle(self, cycle_number):
        for result in self.__actions_collection.aggregate(
            pipeline=[
                {"$unwind": "$actions"},
                {"$match": {"cycle": cycle_number, "actions.outcome": "ACTION_FAILED"}},
                {"$group": {"_id": "$cycle", "count": {"$sum": 1}}},
                {"$project": {"_id": 0, "count": 1}}
            ]
        ):
            return result["count"]
