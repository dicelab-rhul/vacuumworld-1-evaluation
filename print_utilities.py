def print_states_for_all_cycles(manager):
    print "##########"
    print "States for every cycle:\n"

    for state in manager.get_states_for_all_cycles():
        print state
        print "\n"

    print "##########\n"


def print_actions_reports_for_all_cycles(manager):
    print "##########"
    print "Actions in all cycles:\n"

    for actions_report in manager.get_actions_reports_for_all_cycles():
        print actions_report
        print "\n"

    print "##########\n"


def print_actors_names(manager):
    print "##########"
    print "Actors:\n"

    for actor in manager.get_actors_names():
        print actor + "\n"

    print "##########\n"


def print_state_for_specific_cycle(manager, cycle):
    print "##########"
    print "State for cycle " + str(cycle) + ":\n"

    print manager.get_state_for_specific_cycle(cycle)

    print "##########\n"


def print_specific_actor_actions_in_all_cycles(manager, actor):
    print "##########"
    print "Actor " + actor + " actions for all cycles:\n"

    for action in manager.get_specific_actor_actions_in_all_cycles(actor):
        print action
        print "\n"

    print "##########\n"


def print_specific_actor_action_in_specific_cycle(manager, actor, cycle):
    print "##########"
    print "Actor " + actor + " actions for cycle " + str(cycle) + ":\n"

    print manager.get_specific_actor_action_in_specific_cycle(cycle, actor)

    print "##########\n"


def print_all_actors_actions_in_specific_cycle(manager, cycle):
    print "##########"
    print "All actors actions for cycle " + str(cycle) + ":\n"

    print manager.get_all_actors_actions_in_specific_cycle(cycle)

    print "##########\n"


def print_number_of_successful_actions_in_specific_cycle(manager, cycle):
    print "##########"
    print "Number of successful actions for cycle " + str(cycle) + ":\n"

    print str(manager.count_number_of_successful_actions_in_specific_cycle(cycle))

    print "##########\n"


def print_number_of_impossible_actions_in_specific_cycle(manager, cycle):
    print "##########"
    print "Number of impossible actions for cycle " + str(cycle) + ":\n"

    print str(manager.count_number_of_impossible_actions_in_specific_cycle(cycle))

    print "##########\n"


def print_number_of_failed_actions_in_specific_cycle(manager, cycle):
    print "##########"
    print "Number of failed actions for cycle " + str(cycle) + ":\n"

    print str(manager.count_number_of_failed_actions_in_specific_cycle(cycle))

    print "##########\n"


def print_number_of_successful_actions_for_all_cycles(manager, cycles_number):
    for i in range(1, cycles_number + 1):
        print_number_of_successful_actions_in_specific_cycle(manager, i)


def print_number_of_impossible_actions_for_all_cycles(manager, cycles_number):
    for i in range(1, cycles_number + 1):
        print_number_of_impossible_actions_in_specific_cycle(manager, i)


def print_number_of_failed_actions_for_all_cycles(manager, cycles_number):
    for i in range(1, cycles_number + 1):
        print_number_of_failed_actions_in_specific_cycle(manager, i)


def print_number_of_successful_or_impossible_or_failed_actions_for_all_cycles(manager, cycles_number):
    for i in range(1, cycles_number + 1):
        print_number_of_successful_actions_in_specific_cycle(manager, i)
        print_number_of_impossible_actions_in_specific_cycle(manager, i)
        print_number_of_failed_actions_in_specific_cycle(manager, i)


def print_number_of_specific_actor_successful_actions_in_all_cycles(manager, actor_id):
    print "##########"
    print "Agent " + actor_id + " number of successful actions for all cycles :\n"

    print str(manager.count_specific_actor_successful_actions_in_all_cycles(actor_id))

    print "##########\n"


def print_number_of_specific_actor_impossible_actions_in_all_cycles(manager, actor_id):
    print "##########"
    print "Agent " + actor_id + " number of impossible actions for all cycles :\n"

    print str(manager.count_specific_actor_impossible_actions_in_all_cycles(actor_id))

    print "##########\n"


def print_number_of_specific_actor_failed_actions_in_all_cycles(manager, actor_id):
    print "##########"
    print "Agent " + actor_id + " number of failed actions for all cycles :\n"

    print str(manager.count_specific_actor_failed_actions_in_all_cycles(actor_id))

    print "##########\n"
