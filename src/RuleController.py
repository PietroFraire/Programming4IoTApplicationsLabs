from time import thread_time
from src.TemperatureRule import TemperatureRule
from src.LightRule import LightRule

class RuleController():
    def __init__(self):
        self.rules={}
    
    def create_rule(self, rule_type, threshold):
        if rule_type == "temperature":
            rule = TemperatureRule(threshold)
            return rule
        elif rule_type == "light":
            rule= LightRule(threshold)
            return rule
        else:
            print("invalid type")
            return False
    
    def input_data(self):
        name = input("insert name of rule: ")
        rule_type = input("insert the type of rule: ")
        threshold = float(input("insert threshold (must be a number)"))
        return name, rule_type, threshold

    def add(self):
        name, rule_type, threshold = self.input_data()
        rule = self.create_rule(rule_type, threshold)
        if rule:
            self.rules[name] = rule

    def update(self):
        name = input("insert name of rule: ")
        if name in self.rules:
            new_threshold = float(input("insert threshold (must be a number)"))
            self.rules[name].threshold=new_threshold
            print("updated")
        else:
            print("not updated")
    
    def delete(self):
        name = input("insert name of rule: ")
        if name in self.rules:
            del self.rules[name]
            print("deleted")
        else:
            print("not deleted")

    def evaluate(self, temperature, light):
        for name, rule in self.rules.items():
            if isinstance(rule, TemperatureRule):
                result = rule.evaluate(temperature)
                print(name, ":", result)
            elif isinstance(rule, LightRule):
                result = rule.evaluate(light)
                print(name, ":", result)

    def rules(self):
        for name, rule in self.rules.items():
            if isinstance(rule, TemperatureRule):
                print(name, "- Temperature - threshold:", rule.threshold)
            elif isinstance(rule, LightRule):
                print(name, "- Light - threshold:", rule.threshold)

if __name__ == "__main__":
    controller=RuleController()
    while(True):
        print("what do you want to do? ")
        print("add: add a new rule; ")
        print("update: update an existing rule; ")
        print("delete: delete an existing rule; ")
        print("evaluate: evaluate current temperature or light; ")
        print("rules: print the listing of rules; ")
        print("exit: close the program. ")
        choice=input("insert one word: ")
        if choice == "add":
            controller.add()
        elif choice == "update":
            controller.update()
        elif choice == "delete":
            controller.delete()
        elif choice == "evaluate":
            temperature = float(input("Enter current temperature: "))
            light = float(input("Enter current light level: "))
            controller.evaluate(temperature,light)
        elif choice == "rules":
            controller.rules()
        elif choice == "exit":
            break
        else:
            print("You entered an incorrect word, try again: ")
            choice = input("insert one word: ")