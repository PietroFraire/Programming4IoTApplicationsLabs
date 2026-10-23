from rules import TemperatureRule, LightRule
import random

class RuleController():

    def __init__(self):
        self.rules = {}

    def add(self, type, name, threshold:float):

        if name in self.rules:
            print("Rule already existing")
            return None
        
        if type == "t":
            r = TemperatureRule(name, threshold)
            self.rules[name] = r
            return r
        elif type == "l":
            r = LightRule(name, threshold)
            self.rules[name] = r
            return r
        else:
            print("Unknown type")
            return None

    def update(self, name, threshold):

        if name not in self.rules:
            print("Unknown rule")
            return None 

        r = self.rules[name]
        r.updateThreshold(threshold)
        return r

    def delete(self, name):
        if name not in self.rules:
            print("Unknown rule")
            return None 
        
        return self.rules.pop(name)

    def printRules(self):
        for r in list(self.rules.values()):
            print(str(r))

    def evaluete(self, type, current):

        for r in self.rules.values():
            if isinstance(r, TemperatureRule) and type=="t":
                if r.evaluete(current):
                    print(f"Rule {r.name} respected")
                else:
                    print(f"Rule {r.name} not respected")
            if isinstance(r, LightRule) and type=="l":
                if r.evaluete(current):
                    print(f"Rule {r.name} respected")
                else:
                    print(f"Rule {r.name} not respected")

    def printMenu(self):
        print("--Menu-----------")
        print("- add: add anew rule")
        print("- update: update an existing rule")
        print("- delete: delete an existing rule")
        print("- evaluete: evaluete current temperature or light")
        print("- rules: print the existing rules")
        print("- exit: close the program")
            

if __name__ == "__main__":

    controller = RuleController()

    while True:

        controller.printMenu()

        command = input("select command: ")

        match command:
            case "add":
                type = input("Rule type <t/l>:")
                name = input("Rule name: ")
                thresh = float(input("Rule threshold: "))

                controller.add(type, name, thresh)
            case "update":
                name = input("Rule name: ")
                thresh = float(input("New rule threshold: "))

                controller.update(name, thresh)
            case "delete":
                name = input("Rule name: ")
                controller.delete(name)
            case "evaluete":
                type = input("Intert type <t/l>: ")
                if type == "t":
                    current = random.randint(15, 30)
                elif type =="l":
                    current = random.randint(0, 100)
                else:
                    print("Unknown command")
                    continue
                print(f"Current: {current}")
                controller.evaluete(type, current)
            case "rules":
                controller.printRules()
            case "exit":
                print("It was a pleasure ;)")
                break
            case _:
                print("Uknown command")