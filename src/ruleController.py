#manage and control temperature and lights of the home.
import json
import cherrypy
import requests
class ConditionRule:

    def __init__(self, rule_name, threshold):
        self.rule_name = rule_name
        self.threshold = float(threshold)


    def evaluate(self):
        pass

    def tojson(self):
        pass

class TemperatureRule(ConditionRule):

    def evaluate(self, current_temp):
        
        return current_temp > self.threshold

    def tojson(self):
        
        return json.dumps({
            "ruleName": self.rule_name,
            "ruleType": "temperature",
            "threshold": self.threshold
        })
        
    

class LightRule(ConditionRule):
        
    def evaluate(self, current_light):
      
        return current_light < self.threshold

    def tojson(self):
    
        return json.dumps({
            "ruleName": self.rule_name,
            "ruleType": "light",
            "threshold": self.threshold
        })


class RuleController:
    exposed = True
    def __init__(self):
        self.rules = {}
        self.readable_rules = {} 
        # TODO: is it necessarly to have 2 data structure with the same data? 
        # I think it is unconvinient for redundancy and discrepanciens
        # I suggest the function getDictRules that returns the rules as a dictionary from the rules attribute




    def GET(self, *uri, **param):
        if len(uri) == 0:
            if not self.rules:
                return json.dumps({"rules": []})
            else:
                return json.dumps(self.getDictRules()) 
        else:
            raise cherrypy.HTTPError(404, "Endpoint not found")

    def POST(self, *uri, **param):

        if len(uri) != 1:
            raise cherrypy.HTTPError(400, "Bad request")
        
        if uri[0] == "addRule":
            # {"rule": "Temperature", "rule_name": "living_room", "threshold": "45"} => example TODO: change "rule" => "rule_type"? -Pietro
            data = json.loads(cherrypy.request.body.read())

            rule_type = data.get("rule")
            rule_name = data.get("rule_name")
            threshold = float(data.get("threshold"))

            if rule_name in self.rules:
                raise cherrypy.HTTPError(400, "Rule name already exists")
            else:
                self.add(rule_name, rule_type, threshold)
            
            for current_name, rule_object in self.rules.items():
                self.readable_rules[current_name] = {
                    "type" : type(rule_object).__name__,
                    "threshold" : rule_object.threshold
                }

            result_dict = {
                "operation": uri[0],
                "rule_type": rule_type,
                "rule_name": rule_name,
                "threshold": threshold,
                "list_of_rules": self.readable_rules
            }

            return json.dumps(result_dict)

        elif uri[0] == "evaluate":
            #{"rule_name": "living_room", "value": "45"}
            data = json.loads(cherrypy.request.body.read())
            rule_name = data.get("rule_name")
            value = float(data.get("value"))
            result = self.evaluate(rule_name, value)
            
            return json.dumps(result) # TODO: I think we should return a json format -Pietro

        else:
            raise cherrypy.HTTPError(400, "Unknown request")

    def PUT(self, *uri, **param): # TODO: should we ask some specific uri path? -Pietro

        if len(uri) != 1:
            raise cherrypy.HTTPError(400, "Invalid request")

        data = json.loads(cherrypy.request.body.read())
        
        rule_name = uri[0]
        rule_type = data.get("rule")
        new_threshold = float(data.get("threshold"))

        if rule_name not in self.rules:
            raise cherrypy.HTTPError(404, "Rule Name not found")

        self.update(rule_name, new_threshold)

        return json.dumps({
            "operation": "update",
            "rule_type": rule_type,
            "rule_name": rule_name,
            "threshold": new_threshold,
            "list_of_rules": self.getDictRules()
            })

    def DELETE(self, *uri, **param):
        if len(uri) != 2: 
            # or uri[0] != "deleteRule": #Not sure this is needed
            # I removed this because I think it is not necessarly to add another word to the path, the function call is enought -Pietro 
            raise cherrypy.HTTPError(400, "Wrong URL type")

        rule_name = uri[1]
        if rule_name not in self.rules:
            raise cherrypy.HTTPError(404, "Rule not found")

        removed = self.rules.pop(rule_name)
        # TODO: small fix here -Pietro
        return json.dumps({
            "operation": "update",
            "rule_type": type(removed).__name__,
            "rule_name": rule_name,
            "threshold": removed.threshold,
            "list_of_rules": self.getDictRules()
            }) 

    def add(self, rule_name, rule_type, threshold):
        if rule_type.lower() == "temperature":
            self.rules[rule_name] = TemperatureRule(rule_name, threshold)
            print(f"Added Temperature rule: '{rule_name}' at {threshold}°")
        elif rule_type.lower() == "light":
            self.rules[rule_name] = LightRule(rule_name, threshold)
            print(f"Added Light rule: '{rule_name}' at {threshold}")
        else:
            raise cherrypy.HTTPError(404, "Error: Rule type must be 'temperature' or 'light'.")
    
    def update(self, rule_name, new_threshold):
        if rule_name in self.rules:
            self.rules[rule_name].threshold = float(new_threshold)
            print(f"Rule '{rule_name}' updated to new threshold: {new_threshold}")
        else:
            print(f"Error: Rule '{rule_name}' not found.")
    
    def delete(self, rule_name):
        if rule_name in self.rules:
            del self.rules[rule_name]
            print(f"Rule '{rule_name}' deleted.")
        else:
            print(f"Error: Rule '{rule_name}' not found.")

    def evaluate(self, rule_name, value):

        if rule_name in self.rules:

            rule = self.rules[rule_name]
            done = rule.evaluate(value)
            if done:
                return {
                    "operation": "evaluate",
                    "rule_name": rule_name, 
                    "value": value,
                    "status": "TRIGGERED"
                }
            else:
                return {
                    "operation": "evaluate",
                    "rule_name": rule_name,
                    "value": value,
                    "status": "NORMAL"
                }
        else:
            raise cherrypy.HTTPError(404, f"Rule '{rule_name}' not found")

    def getDictRules(self):

        r = {}
        for current_name, rule_object in self.rules.items():
            r[current_name] = {
                "type" : type(rule_object).__name__,
                "threshold" : rule_object.threshold
            }

        return r