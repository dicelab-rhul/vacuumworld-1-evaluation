import os
import argparse as ap
import random
import json
import shutil

from collections import OrderedDict


def main():
    students_id_to_names, students_dir = __check_argv()
    grid_size_values = [3, 4, 5, 6, 7, 8, 9, 10]

    if os.path.exists(students_dir):
        shutil.rmtree(students_dir)

    os.mkdir(students_dir)

    for number, name in students_id_to_names.iteritems():
        __generate_exploration_test_cases(grid_size_values, number, name, students_dir)
        # todo __generate_cleaning_test_cases(grid_size_values)


def __check_argv():
    parser = ap.ArgumentParser(description='VacuumWorld Test Generator')
    parser.add_argument('-s', '--students-file',
                        required=True,
                        metavar='<students-file-path>', type=str,
                        action='store',
                        help='Students IDs and names file')

    args = parser.parse_args()

    return __parse_students(args.students_file), "students"


def __parse_students(students_file):
    f = open(students_file, "r")

    students = {}

    for line in f.readlines():
        temp = line.split(",")
        students[temp[0]] = temp[1].replace("\n", "").replace(" ", "-")

    f.close()

    return students


def __generate_exploration_test_cases(grid_size_values, student_number, student_name, students_dir):
    student_dir = os.path.join(students_dir, student_number + "_" + student_name)

    if os.path.exists(student_dir):
        shutil.rmtree(student_dir)

    os.mkdir(student_dir)

    for size in grid_size_values:
        agent_id = ''.join(random.choice("0123456789abcdef") for _ in range(20))
        initial_state = OrderedDict()
        initial_state.update({"width": size})
        initial_state.update({"height": size})
        agent = OrderedDict()
        agent.update({"id": "Agent-" + agent_id + "-Test-" + str(size - 2) + "-Grid-Size-" + str(size) + "-Run-1-Student-" + student_number})
        agent.update({"name": "Agent-" + student_name + "-Test-" + str(size - 2) + "-Grid-Size-" + str(size) + "-Run-1-Student-" + student_number})
        agent.update({"color": "white"})
        agent.update({"sensors": 2})
        agent.update({"actuators": 2})
        agent.update({"width": 1})
        agent.update({"height": 1})
        agent.update({"facing_direction": "west"})
        location = OrderedDict()
        location.update({"x": 2})
        location.update({"y": 2})
        location.update({"agent": agent})
        notable_locations = [location]
        initial_state.update({"notable_locations": notable_locations})

        output = open(os.path.join(student_dir, "test-" + str(size - 2) + ".json"), "w")
        json.dump(initial_state, output, indent=4, separators=(',', ': '))
        output.close()


if __name__ == "__main__":
    main()
