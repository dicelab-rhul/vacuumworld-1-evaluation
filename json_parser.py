import json

from mongo_variables import MongoVariables
from evaluation_variables import EvaluationVariables


def parse(json_file):
    try:
        input_file = open(json_file, "r")

        return __parse(input_file)
    except IOError:
        return {}, {}


def __parse(input_file):
    dictionary = json.load(input_file)
    input_file.close()

    if dictionary == {}:
        raise IOError("Empty dictionary!!!")
    else:
        mongo_vars = MongoVariables()
        mongo_vars.populate(dictionary["mongodb"])

        eval_vars = EvaluationVariables()
        eval_vars.populate(dictionary["evaluation_strategy"])

        return mongo_vars, eval_vars
