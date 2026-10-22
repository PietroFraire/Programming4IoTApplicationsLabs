from rules import TemperatureRule, LightRule

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
                pass
            case "evaluete":
                pass
            case "rules":
                pass
            case "exit":
                print("It was a pleasure ;)")
                break
            case _:
                print("Uknown command")