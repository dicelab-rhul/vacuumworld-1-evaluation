import custom_observable as coe
import custom_observer as cor
import evaluate_action as eva
import evaluation_environment as ee
import evaluator_body as eb


class EvaluatorActuator(coe.CustomObservable, cor.CustomObserver):
    def __init__(self):
        coe.CustomObservable.__init__(self)

    def update(self, observable, payload):
        if isinstance(observable, eb.EvaluatorBody):
            self.__manage_body_request(payload)
        else:
            raise ValueError("Unexpected observable type: " + str(type(observable)) + ".")

    def __manage_body_request(self, payload):
        if isinstance(payload, eva.EvaluateAction):
            self.notify_specific_type_observers(payload, ee.EvaluationEnvironment)
        else:
            raise ValueError("Unexpected payload type: " + str(type(payload)) + ".")
