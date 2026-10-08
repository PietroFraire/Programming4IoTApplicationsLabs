import json
class ConditionRule(object):
    def __init__(self, threshold):
        self.threshold=threshold

    def evaluate(self, value):
        return value > self.threshold