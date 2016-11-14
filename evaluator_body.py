import custom_observable as coe
import custom_observer as cor
import evaluate_action as eva
import evaluator_actuator as ea
import evaluator_brain as ebr
import evaluator_sensor as es
import result as r

__author__ = "cloudstrife9999, A.K.A. Emanuele Uliana"


class EvaluatorBody(coe.CustomObservable, cor.CustomObserver):
    def __init__(self, body_id, mind, brain, sensors, actuators):
        coe.CustomObservable.__init__(self)
        self.__id = body_id
        self.__mind = mind
        self.__brain = brain
        self.__sensors = sensors
        self.__actuators = actuators

        self.__make_observers()

    def get_id(self):
        return self.__id

    def __make_observers(self):
        self.__mind.add_observer(self.__brain)
        self.__brain.add_observer(self.__mind)
        self.__brain.add_observer(self)
        self.add_observer(self.__brain)

        for actuator in self.__actuators:
            self.add_observer(actuator)

        for sensor in self.__sensors:
            sensor.add_observer(self)

    def update(self, observable, payload):
        if isinstance(observable, ebr.EvaluatorBrain):
            self.__manage_brain_request(payload)
        elif isinstance(observable, es.EvaluatorSensor):
            self.__manage_sensor_request(payload)
        else:
            raise ValueError("Unexpected observable type: " + str(type(observable)) + ".")

    def __manage_brain_request(self, payload):
        if isinstance(payload, eva.EvaluateAction):
            self.notify_specific_type_observers(payload, ea.EvaluatorActuator)
        else:
            raise ValueError("Unexpected payload type: " + str(type(payload)) + ".")

    def __manage_sensor_request(self, payload):
        if isinstance(payload, r.EvaluationResult):
            self.notify_specific_type_observers(payload, ebr.EvaluatorBrain)
        else:
            raise ValueError("Unexpected payload type: " + str(type(payload)) + ".")
