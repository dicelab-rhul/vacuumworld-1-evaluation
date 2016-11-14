from outcomes import *

__author__ = "cloudstrife9999, A.K.A. Emanuele Uliana"


class EvaluationResult:
    def __init__(self, score, outcome, body_id):
        self.__possible_outcomes = [succeeded, impossible, failed]
        self.__set_outcome(outcome)
        self.__score = score
        self.__body_id = body_id

    def __set_outcome(self, outcome):
        if outcome not in self.__possible_outcomes:
            raise ValueError("Unsupported outcome: " + str(outcome) + ".")
        else:
            self.__outcome = outcome

    def get_score(self):
        return self.__score

    def get_outcome(self):
        return self.__outcome

    def get_body_id(self):
        return self.__body_id

    def is_failure(self):
        return self.__outcome == self.__possible_outcomes[2]

    def is_success(self):
        return self.__outcome == self.__possible_outcomes[0]

    def is_impossible(self):
        return self.__outcome == self.__possible_outcomes[1]
