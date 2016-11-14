import custom_observable as coe
import custom_observer as cor
import evaluate_action as eva
import evaluator_brain as ebr
import result as r


class EvaluatorMind(coe.CustomObservable, cor.CustomObserver):
    def __init__(self, body_id):
        coe.CustomObservable.__init__(self)
        self.__body_id = body_id
        self.__last_action_result = None
        self.__additional_results = []

    def get_last_action_result(self):
        return self.__last_action_result

    def get_additional_results(self):
        return self.__additional_results

    def perceive(self):
        self.notify_specific_type_observers(None, ebr.EvaluatorBrain)

    def decide(self, **kwargs):
        kwargs["pippo"] = "pluto"  # todo

        return eva.EvaluateAction(self.__body_id, **kwargs)

    def execute(self, action):
        if isinstance(action, eva.EvaluateAction):
            self.notify_specific_type_observers(action, ebr.EvaluatorBrain)
        else:
            raise ValueError("Unexpected action type: " + str(type(action)) + ".")

    def update(self, observable, payload):
        if isinstance(observable, ebr.EvaluatorBrain):
            self.__manage_brain_request(payload)
        else:
            raise ValueError("Unexpected observable type: " + str(type(observable)) + ".")

    def __manage_brain_request(self, payload):
        if isinstance(payload, list):
            self.__manage_brain_data(payload)
        else:
            raise ValueError("Unexpected data from brain: " + str(type(payload)) + ".")

    def __manage_brain_data(self, data):
        if len(data) < 1:
            raise ValueError("Got empty results list from brain.")
        elif isinstance(data[0], r.EvaluationResult):
            self.__last_action_result = data[0]
            self.__store_other_results(data)
        else:
            raise ValueError("Unexpected data from brain: " + str(type(data[0])) + ".")

    def __store_other_results(self, data):
        if len(data) == 1:
            return
        else:
            self.__additional_results = data[1:]
