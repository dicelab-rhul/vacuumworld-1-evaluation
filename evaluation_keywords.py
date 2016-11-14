from mongo_keywords import turn_left, turn_right, move, clean, perceive, speak, drop_dirt

__author__ = "cloudstrife9999, A.K.A. Emanuele Uliana"


physical = [turn_left, turn_right, move, clean, drop_dirt]
sensing = [perceive]
communication = [speak]

successful_physical_coefficient_key = "successful_physical_coefficient"
impossible_physical_coefficient_key = "impossible_physical_coefficient"
failed_physical_coefficient_key = "failed_physical_coefficient"
successful_sensing_coefficient_key = "successful_sensing_coefficient"
impossible_sensing_coefficient_key = "impossible_sensing_coefficient"
failed_sensing_coefficient_key = "failed_sensing_coefficient"
successful_communication_coefficient_key = "successful_communication_coefficient"
impossible_communication_coefficient_key = "impossible_communication_coefficient"
failed_communication_coefficient_key = "failed_communication_coefficient"

strategy_name_key = "strategy_name"
linear_strategy = "linear_strategy"
actor_to_evaluate_key = "actor_to_evaluate"
