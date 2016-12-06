import sys
import json


def main():
    input_file = open(sys.argv[1], "r")
    data = json.load(input_file)
    input_file.close()

    print data["dirts_number"]


if __name__ == "__main__":
    main()
