from src.ConditionRule import ConditionRule
import json
class LightRule(ConditionRule):
    def __init__(self, threshold):
        super().__init__(threshold)

    def evaluate(self, light):
        return light > self.threshold