import evaluation_environment as ee
import evaluation_physics as ep
import result as r

from outcomes import *


class EvaluateAction:
    def __init__(self, body_id, **kwargs):
        self.__body_id = body_id
        self.__kwargs = kwargs

    def get_body_id(self):
        return self.__body_id

    def get_kwargs(self):
        return self.__kwargs

    def __is_possible(self, physics, context):
        if isinstance(physics, ep.EvaluationPhysics) and isinstance(context, ee.EvaluationEnvironment):
            return physics.is_possible(self, context)
        else:
            return False

    def attempt(self, physics, context):
        if self.__is_possible(physics, context):
            result = self.__perform(physics, context)

            if result.is_failure():
                return result
            elif result.is_success():
                return self.__check_post_conditions(result, physics, context)
            else:
                raise ValueError("Unexpected result: " + str(result.get_outcome()) + ".")
        else:
            return r.EvaluationResult(None, impossible, self.__body_id)

    def __check_post_conditions(self, result, physics, context):
        if self.__succeeded(physics, context):
            return result
        else:
            return r.EvaluationResult(None, failed, self.__body_id)

    def __perform(self, physics, context):
        if isinstance(physics, ep.EvaluationPhysics) and isinstance(context, ee.EvaluationEnvironment):
            return physics.perform(self, context)
        else:
            return r.EvaluationResult(None, impossible, self.__body_id)

    def __succeeded(self, physics, context):
        if isinstance(physics, ep.EvaluationPhysics) and isinstance(context, ee.EvaluationEnvironment):
            return physics.succeeded(self, context)
        else:
            return False
