from src.ConditionRule import ConditionRule
import json
class TemperatureRule(ConditionRule):
    def __init__(self, threshold):
        super().__init__(threshold)

    def evaluate(self, temperature):
        return temperature > self.threshold