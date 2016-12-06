import os
import argparse as ap
import random
import json
import shutil

from collections import OrderedDict


def main():
    agent_ids, students_dir = __check_argv()
    grid_size_values = [3, 4, 5, 6, 7, 8, 9, 10]

    if os.path.exists(students_dir):
        shutil.rmtree(students_dir)

    os.mkdir(students_dir)

    sizes_for_stage_2 = {}
    sizes_for_stage_3 = {}

    for i in range(9, 51):
        sizes_for_stage_2[i] = random.randint(grid_size_values[0], grid_size_values[-1])

    for i in range(51, 101):
        sizes_for_stage_3[i] = random.randint(grid_size_values[0], grid_size_values[-1])

    for agent_id in agent_ids:
        __generate_exploration_test_cases(grid_size_values, agent_id, students_dir)
        __generate_cleaning_test_cases_without_user(sizes_for_stage_2, agent_id, students_dir)
        __generate_cleaning_test_cases_with_user(sizes_for_stage_3, agent_id, students_dir)


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

    students = []

    for line in f.readlines():
        students.append(line.replace("\n", ""))

    f.close()

    return students


def __create_student_dir(student_dir):
    if os.path.exists(student_dir):
        shutil.rmtree(student_dir)

    os.mkdir(student_dir)
    shutil.copy2("model.json", os.path.join(student_dir, "model_1.json"))
    shutil.copy2("model.json", os.path.join(student_dir, "model_2.json"))
    shutil.copy2("model.json", os.path.join(student_dir, "model_3.json"))

    # todo modify the copied files


def __generate_exploration_test_cases(grid_size_values, agent_id, students_dir):
    student_dir = os.path.join(students_dir, agent_id)
    __create_student_dir(student_dir)

    for size in grid_size_values:
        initial_state = OrderedDict()
        initial_state.update({"width": size})
        initial_state.update({"height": size})
        initial_state.update({"user": False})
        white_agent_id = "Agent-" + agent_id + "-Test-" + str(size - 2) + "-Grid-Size-" + str(size) + "-Run-1"
        white_agent_name = "Agent-" + agent_id + "-Test-" + str(size - 2) + "-Grid-Size-" + str(size) + "-Run-1"
        location = __generate_agent_location(white_agent_id, white_agent_name, "white", "west", 2, 2)
        notable_locations = [location]
        initial_state.update({"notable_locations": notable_locations})

        output = open(os.path.join(student_dir, "test-" + str(size - 2) + ".json"), "w")
        json.dump(initial_state, output, indent=4, separators=(',', ': '))
        output.close()


def __generate_cleaning_test_cases_without_user(sizes, agent_id, students_dir):
    return __generate_cleaning_test_cases_with_or_without_user(sizes, agent_id, False, students_dir)


def __generate_cleaning_test_cases_with_user(sizes, agent_id, students_dir):
    return __generate_cleaning_test_cases_with_or_without_user(sizes, agent_id, True, students_dir)


def __generate_cleaning_test_cases_with_or_without_user(sizes, agent_id, user, students_dir):
    student_dir = os.path.join(students_dir, agent_id)

    for test_number, grid_size in sizes.iteritems():
        initial_state = OrderedDict()
        initial_state.update({"width": grid_size})
        initial_state.update({"height": grid_size})
        initial_state.update({"user": user})
        white_agent_id = "Agent-" + agent_id + "-Test-" + str(test_number) + "-Grid-Size-" + str(grid_size) + "-Run-1"
        white_agent_name = "Agent-" + agent_id + "-Test-" + str(test_number) + "-Grid-Size-" + str(grid_size) + "-Run-1"
        location = __generate_agent_location(white_agent_id, white_agent_name, "white", "west", 2, 2)
        fellow_agents_locations = __generate_fellow_agents_locations(test_number, grid_size)
        dirt_locations = __generate_random_dirts_locations(grid_size)
        notable_locations = [location]

        for loc in fellow_agents_locations:
            notable_locations.append(loc)

        counter = 0

        for loc in dirt_locations:
            if [loc["x"], loc["y"]] in [[1, 1], [1, 2], [2, 2]]:
                continue  # we do not add dirt to locations with agents on.
            else:
                counter += 1
                notable_locations.append(loc)

        initial_state.update({"dirts_number": counter})
        initial_state.update({"notable_locations": notable_locations})

        output = open(os.path.join(student_dir, "test-" + str(test_number) + ".json"), "w")
        json.dump(initial_state, output, indent=4, separators=(',', ': '))
        output.close()


def __generate_fellow_agents_locations(test_number, grid_size):
    green_id = ''.join(random.choice("0123456789abcdef") for _ in range(20))
    green_agent_id = "Agent-" + green_id + "-Test-" + str(test_number) + "-Grid-Size-" + str(grid_size) + "-Run-1"
    orange_id = ''.join(random.choice("0123456789abcdef") for _ in range(20))
    orange_agent_id = "Agent-" + orange_id + "-Test-" + str(test_number) + "-Grid-Size-" + str(grid_size) + "-Run-1"

    return [
        __generate_agent_location(green_agent_id, green_agent_id, "green", "east", 1, 1),
        __generate_agent_location(orange_agent_id, orange_agent_id, "orange", "east", 1, 2)
    ]


def __generate_agent_location(agent_id, agent_name, color, facing_direction, x, y):
    agent = OrderedDict()
    agent.update({"id": agent_id})
    agent.update({"name": agent_name})
    agent.update({"color": color})
    agent.update({"sensors": 2})
    agent.update({"actuators": 2})
    agent.update({"width": 1})
    agent.update({"height": 1})
    agent.update({"facing_direction": facing_direction})
    location = OrderedDict()
    location.update({"x": x})
    location.update({"y": y})
    location.update({"agent": agent})

    return location


def __generate_random_dirts_locations(grid_size):
    x_coords = [i for i in range(1, grid_size + 1)]
    y_coords = [j for j in range(1, grid_size + 1)]

    dirts_locations_coordinates = __generate_random_locations_coordinates(grid_size, x_coords, y_coords)
    locations = []

    for coordinates in dirts_locations_coordinates:
        locations.append(__generate_location_with_dirt(coordinates))

    return locations


def __generate_random_locations_coordinates(grid_size, x_coords, y_coords):
    number = random.randint(1, grid_size)

    coordinates = []

    for _ in range(number):
        x = x_coords[:]
        random.shuffle(x)
        y = y_coords[:]
        random.shuffle(y)

        i, j = x.pop(), y.pop()
        coordinates.append((i, j))

    return coordinates


def __add_dirt_to_existing_location(location):
    dirt_colors = ["green", "orange"]
    dirt = random.choice(dirt_colors)
    location.update({"dirt": dirt})

    return location


def __generate_location_with_dirt(coordinates):
    x = coordinates[0]
    y = coordinates[1]

    dirt_colors = ["green", "orange"]
    dirt = random.choice(dirt_colors)
    location = OrderedDict()
    location.update({"x": x})
    location.update({"y": y})
    location.update({"dirt": dirt})

    return location


if __name__ == "__main__":
    main()
