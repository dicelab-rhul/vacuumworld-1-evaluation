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

    sizes = {}

    for i in range(13, 101):
        sizes[i] = random.randint(grid_size_values[0], grid_size_values[-1])

    for number, name in students_id_to_names.iteritems():
        __generate_exploration_test_cases(grid_size_values, number, name, students_dir)
        __generate_cleaning_test_cases(sizes, number, name, students_dir)


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
        initial_state.update({"user": False})
        agent = OrderedDict()
        agent.update(
            {
                "id": "Agent-" + agent_id
                      + "-Test-" + str(size - 2)
                      + "-Grid-Size-" + str(size)
                      + "-Run-1-Student-" + student_number
            }
        )
        agent.update(
            {
                "name": "Agent-" + student_name
                        + "-Test-" + str(size - 2)
                        + "-Grid-Size-" + str(size)
                        + "-Run-1-Student-" + student_number
            }
        )
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


def __generate_cleaning_test_cases(sizes, student_number, student_name, students_dir):
    student_dir = os.path.join(students_dir, student_number + "_" + student_name)

    for test_number, grid_size in sizes.iteritems():
        agent_id = ''.join(random.choice("0123456789abcdef") for _ in range(20))
        initial_state = OrderedDict()
        initial_state.update({"width": grid_size})
        initial_state.update({"height": grid_size})
        initial_state.update({"user": random.choice([True, False])})
        agent = OrderedDict()
        agent.update(
            {
                "id": "Agent-" + agent_id
                      + "-Test-" + str(test_number)
                      + "-Grid-Size-" + str(grid_size)
                      + "-Run-1-Student-" + student_number
            }
        )
        agent.update(
            {
                "name": "Agent-" + student_name
                        + "-Test-" + str(test_number)
                        + "-Grid-Size-" + str(grid_size)
                        + "-Run-1-Student-" + student_number
            }
        )
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

        other_notable_locations = __generate_random_notable_locations(grid_size)
        notable_locations = [location]

        for loc in other_notable_locations:
            notable_locations.append(loc)

        initial_state.update({"notable_locations": notable_locations})

        output = open(os.path.join(student_dir, "test-" + str(test_number) + ".json"), "w")
        json.dump(initial_state, output, indent=4, separators=(',', ': '))
        output.close()


def __generate_random_notable_locations(grid_size):
    x_coords = [i for i in range(1, grid_size + 1)]
    y_coords = [j for j in range(1, grid_size + 1)]

    agents_locations_coordinates = __generate_random_locations_coordinates(grid_size, x_coords, y_coords)
    dirts_locations_coordinates = __generate_random_locations_coordinates(grid_size, x_coords, y_coords)

    locations = []

    for c in agents_locations_coordinates:
        if c not in dirts_locations_coordinates:
            locations.append(__generate_location_with_agent(c))
        else:
            locations.append(__generate_mixed_location(c))

    for c in dirts_locations_coordinates:
        if c not in agents_locations_coordinates:
            locations.append(__generate_location_with_dirt(c))

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

        if i == 2 and j == 2:
            continue
        else:
            coordinates.append((i, j))

    return coordinates


def __generate_location_with_agent(coordinates):
    x = coordinates[0]
    y = coordinates[1]

    if x == 2 and y == 2:
        raise ValueError

    facing_directions = ["north", "south", "west", "east"]
    agent_colors = ["white", "green", "orange"]
    agent_id = ''.join(random.choice("0123456789abcdef") for _ in range(20))
    agent = OrderedDict()
    agent.update({"id": "Agent-" + agent_id})
    agent.update({"name": "Agent-" + agent_id})
    agent.update({"color": random.choice(agent_colors)})
    agent.update({"sensors": 2})
    agent.update({"actuators": 2})
    agent.update({"width": 1})
    agent.update({"height": 1})
    agent.update({"facing_direction": random.choice(facing_directions)})
    location = OrderedDict()
    location.update({"x": x})
    location.update({"y": y})
    location.update({"agent": agent})

    return location


def __generate_location_with_dirt(coordinates):
    x = coordinates[0]
    y = coordinates[1]

    if x == 2 and y == 2:
        raise ValueError

    dirt_colors = ["green", "orange"]
    dirt = random.choice(dirt_colors)
    location = OrderedDict()
    location.update({"x": x})
    location.update({"y": y})
    location.update({"dirt": dirt})

    return location


def __generate_mixed_location(coordinates):
    x = coordinates[0]
    y = coordinates[1]

    if x == 2 and y == 2:
        raise ValueError

    facing_directions = ["north", "south", "west", "east"]
    agent_colors = ["white", "green", "orange"]
    dirt_colors = agent_colors[1:]
    agent_id = ''.join(random.choice("0123456789abcdef") for _ in range(20))
    agent = OrderedDict()
    agent.update({"id": "Agent-" + agent_id})
    agent.update({"name": "Agent-" + agent_id})
    agent.update({"color": random.choice(agent_colors)})
    agent.update({"sensors": 2})
    agent.update({"actuators": 2})
    agent.update({"width": 1})
    agent.update({"height": 1})
    agent.update({"facing_direction": random.choice(facing_directions)})
    dirt = random.choice(dirt_colors)
    location = OrderedDict()
    location.update({"x": x})
    location.update({"y": y})
    location.update({"agent": agent})
    location.update({"dirt": dirt})

    return location


if __name__ == "__main__":
    main()
