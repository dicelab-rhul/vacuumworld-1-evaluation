import custom_observable as coe
import custom_observer as cor
import evaluate_action as eva
import evaluation_physics as ep
import evaluator_actuator as ea
import evaluator_sensor as es
import result as r


class EvaluationEnvironment(coe.CustomObservable, cor.CustomObserver):
    def __init__(self, bodies):
        coe.CustomObservable.__init__(self)
        self.__bodies = bodies

    def get_bodies(self):
        return self.__bodies

    def update(self, observable, payload):
        if isinstance(observable, ea.EvaluatorActuator):
            self.__manage_actuator_request(payload)
        elif isinstance(observable, ep.EvaluationPhysics):
            self.__manage_physics_request(payload)
        else:
            raise ValueError("Unexpected observable type: " + str(type(observable)) + ".")

    def __manage_actuator_request(self, payload):
        if isinstance(payload, eva.EvaluateAction):
            self.notify_specific_type_observers(payload, ep.EvaluationPhysics)
        else:
            raise ValueError("Unexpected payload type: " + str(type(payload)) + ".")

    def __manage_physics_request(self, payload):
        if isinstance(payload, r.EvaluationResult):
            self.__notify_right_sensor(payload)
        else:
            raise ValueError("Unexpected payload type: " + str(type(payload)) + ".")

    def __notify_right_sensor(self, result):
        for observer in self.get_specific_type_observers(es.EvaluatorSensor):
            if observer.get_body_id() == result.get_body_id():
                observer.update(self, result)
