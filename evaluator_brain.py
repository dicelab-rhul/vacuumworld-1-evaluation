import custom_observable as coe
import custom_observer as cor
import evaluate_action as eva
import evaluator_body as eb
import evaluator_mind as em
import result as r

__author__ = "cloudstrife9999, A.K.A. Emanuele Uliana"


class EvaluatorBrain(coe.CustomObservable, cor.CustomObserver):
    def __init__(self):
        coe.CustomObservable.__init__(self)
        self.__accumulator = []
        self.__results_for_mind = []

    def update(self, observable, payload):
        if isinstance(observable, em.EvaluatorMind):
            self.__manage_mind_request(payload)
        elif isinstance(observable, eb.EvaluatorBody):
            self.__manage_body_request(payload)
        else:
            raise ValueError("Unexpected observable type: " + str(type(observable)) + ".")

    def __manage_mind_request(self, payload):
        if payload is None:
            self.__notify_mind()
        elif isinstance(payload, eva.EvaluateAction):
            self.notify_specific_type_observers(payload, eb.EvaluatorBody)
        else:
            raise ValueError("Unexpected payload type: " + str(type(payload)) + ".")

    def __notify_mind(self):
        self.__results_for_mind = []

        for result in self.__accumulator:
            self.__results_for_mind.append(result)

        self.__accumulator = []

        self.notify_specific_type_observers(self.__results_for_mind, em.EvaluatorMind)

    def __manage_body_request(self, payload):
        if isinstance(payload, r.EvaluationResult):
            self.__accumulator.append(payload)
        else:
            raise ValueError("Unexpected payload type: " + str(type(payload)) + ".")
