__author__ = "cloudstrife9999, A.K.A. Emanuele Uliana"


class AbstractPhysics:
    def __init__(self):
        pass

    def is_possible(self, evaluate_action, context):
        pass

    def perform(self, evaluate_action, context):
        pass

    def succeeded(self, evaluate_action, context):
        pass
