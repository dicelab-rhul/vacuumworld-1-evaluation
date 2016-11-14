import custom_observable as coe
import custom_observer as cor
import evaluation_environment as ee
import evaluator_body as eb
import result as r

__author__ = "cloudstrife9999, A.K.A. Emanuele Uliana"


class EvaluatorSensor(coe.CustomObservable, cor.CustomObserver):
    def __init__(self, body_id):
        coe.CustomObservable.__init__(self)
        self.__body_id = body_id

    def get_body_id(self):
        return self.__body_id

    def update(self, observable, payload):
        if isinstance(observable, ee.EvaluationEnvironment):
            self.__manage_environment_request(payload)
        else:
            raise ValueError("Unexpected observable type: " + str(type(observable)) + ".")

    def __manage_environment_request(self, payload):
        if isinstance(payload, r.EvaluationResult):
            self.notify_specific_type_observers(payload, eb.EvaluatorBody)
        else:
            raise ValueError("Unexpected payload type: " + str(type(payload)) + ".")
