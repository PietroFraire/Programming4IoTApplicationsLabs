class ConditionRule():

    def __init__(self, name, threshold):
        self.name = name
        self.threshold = threshold

    def evaluete(self, value):
        return self.threshold > value

    def updateThreshold(self, threshold):

        if self.checkThreshold(threshold):
            self.threshold = threshold
        else:
            raise ValueError("Invalid threshold value")

        return self

    def checkThreshold(self, threshold):
        return True

    def __str__(self):
        return f"Name: {self.name}\tThreshold: {self.threshold}"

class LightRule(ConditionRule):

    def __init__(self, name, threshold):
        if not self.checkThreshold:
            raise ValueError("Light value must be between 0-100%") 
        super().__init__( name, threshold)

    def checkThreshold(self, threshold):
        return (threshold > 0 and threshold < 100)

class TemperatureRule(ConditionRule):

    def __init__(self, name, threshold):
        if not self.checkThreshold(threshold):
            raise ValueError("Temperature value must be between 15 and 30 °C")
        super().__init__( name, threshold)

    def updateThreshold(self, threshold):
        self.threshold = threshold
    
    def checkThreshold(self, threshold):
        return threshold > 15 and threshold < 30

