class ConditionRule():

    def __init__(self, threshold, name):
        self.name = name
        self.threshold = threshold

    def evaluete(self, value):
        return self.threshold > value

class LightRule(ConditionRule):

    def __init__(self, threshold, name):
        if threshold < 0 or threshold > 100:
            raise ValueError("Light value must be between 0-100%") 
        super().__init__(threshold, name)

class TemperatureRule(ConditionRule):

    def __init__(self, threshold, name):
        if threshold < -20 or threshold > 100:
            raise ValueError("Temperature value must be between 15 and 30 °C")
        super().__init__(threshold, name)

