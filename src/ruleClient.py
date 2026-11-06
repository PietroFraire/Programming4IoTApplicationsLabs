import json
import cherrypy
import requests

URL = "http://127.0.0.1:8080"

class RuleClient:

    def __init__(self):
        pass

    def getRules(self):
        pass

    def addRule(self):
        pass

    def evaluate(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

if __name__ == "__main__":

    ruleClient = RuleClient()

    while True:

        print("1. Get Rules")
        print("2. add rule")
        print("3. evaluate")
        print("4. update")
        print("5. delete")
        print("6. exit")

        cmd = int(input("select:"))

        match cmd:
            case 1:
                ruleClient.getRules()
            case 2:
                ruleClient.addRule()
            case 3:
                ruleClient.evaluate()
            case 4:
                ruleClient.update()
            case 5:
                ruleClient.delete()
            case 6:
                print("Leaving...")
                break
            case _:
                print("Unknown Command")

        