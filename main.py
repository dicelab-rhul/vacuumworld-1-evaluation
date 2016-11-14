#!/usr/bin/python

from db_manager import DBManager
from print_utilities import *


__author__ = "cloudstrife9999, A.K.A. Emanuele Uliana"


def main():
    manager = DBManager("127.0.0.1", "27017", "VacuumWorld", "states", "actions")

    # TODO: do whatever is needed here.

    print_number_of_successful_or_impossible_or_failed_actions_for_all_cycles(manager, 20)
    print_actors_names(manager)
    print_specific_actor_action_in_specific_cycle(manager, manager.get_actors_names()[0], 1)
    print_specific_actor_action_in_specific_cycle(manager, manager.get_actors_names()[1], 1)
    print_specific_actor_actions_in_all_cycles(manager, manager.get_actors_names()[0])
    print_specific_actor_actions_in_all_cycles(manager, manager.get_actors_names()[1])
    print_all_actors_actions_in_specific_cycle(manager, 1)

    manager.close_connection()


if __name__ == "__main__":
    main()
