#manage and control temperature and lights of the home.
import json
import cherrypy
class ConditionRule:

    def __init__(self, rule_name, threshold):
        self.rule_name = rule_name
        self.threshold = float(threshold)


    def evaluate(self):
        pass

class TemperatureRule(ConditionRule):

    def evaluate(self, current_temp):
        if current_temp > self.threshold:
            return True 
        return False

class LightRule(ConditionRule):
        
    def evaluate(self, current_light):
        if current_light < self.threshold:
            return True
        return False


class RuleController:
    exposed = True
    def __init__(self):
        self.rules = {}

    def GET(self, *uri, **param):
        if len(uri) == 0:
            if not self.rules:
                return json.dumps({"rules": []})
            else:
                return json.dumps(self.rules) 
        else:
            raise cherrypy.HTTPError(404, "Endpoint not found")

    def POST(self, *uri, **param):
        pass

    def PUT(self, *uri, **param):
        pass

    def DELETE(self, *uri, **param):
        pass

    def add(self, rule_name, rule_type, threshold):
        if rule_type.lower() == "temperature":
            self.rules[rule_name] = TemperatureRule(rule_name, threshold)
            print(f"Added Temperature rule: '{rule_name}' at {threshold}°")
        elif rule_type.lower() == "light":
            self.rules[rule_name] = LightRule(rule_name, threshold)
            print(f"Added Light rule: '{rule_name}' at {threshold}")
        else:
            print("Error: Rule type must be 'temperature' or 'light'.")
    
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

    def evaluate(self, current_temp=None, current_light=None):
        print(f"\n--- Evaluating Sensor Data (Temp: {current_temp}, Light: {current_light}) ---")

        for name, rule in self.rules.items():
            if isinstance(rule, TemperatureRule) and current_temp is not None:
                triggered = rule.evaluate(current_temp)
                state = "TRIGGERED (TOO HOT)!" if triggered else "normal"
                print(f"Rule '{name}': {state}")
            elif isinstance(rule, LightRule) and current_light is not None:
                triggered = rule.evaluate(current_light)
                state = "TRIGGERED (TOO DARK!)" if triggered else "normal"
                print(f"Rule '{name}: {state}")


if __name__ == "__main__":

    controller = RuleController()

    while True:
        # 1. Print the menu options
        print("\n--- Rule controller Menu ---")
        print("1. add")
        print("2. update")
        print("3. delete")
        print("4. evaluate")
        print("5. rules")
        print("6. exit")
        
        command = input("Enter command: ").strip().lower()

        match command:
            case '1':
                name = input("Enter a name for this rule (e.g. 'LivingRoomTemp'): ").strip()
                r_type = input("Enter rule type ('temperature' or 'light'): ").strip()
                try:
                    threshold = float(input("Enter threshold value: ").strip())
                    controller.add(name, r_type, threshold)
                except ValueError:
                    print("Error: Threshold must be a number.")

            case '2':
                name = input("Enter the name of the rule to update: ").strip()
                try:
                    new_threshold = float(input("Enter new threshold value: ").strip())
                    controller.update(name, new_threshold)
                except ValueError:
                    print("Error: Threshold must be a number.")

            case '3':
                name = input("Enter the name of the rule to delete: ").strip()
                controller.delete(name)

            case '4':
                print("Enter sensor readings (Press ENTER to skip a sensor):")
                temp_input = input("Enter current temperature: ").strip()
                light_input = input("Enter current light level: ").strip()

                try:
                    cur_temp = float(temp_input) if temp_input else None
                    cur_light = float(light_input) if light_input else None
                    controller.evaluate(cur_temp, cur_light)

                    # Prevent them from skipping both
                    if cur_temp is None and cur_light is None:
                        print("Error: You must provide at least one measurement.")
                    else:
                        controller.evaluate(cur_temp, cur_light)

                except ValueError:
                    print("Error: Sensor readings must be numbers.")

            case '5':
                controller.print_rules()

            case '6':
                print("Closing program...")
                break
            case _:
                print("Invalid command. Please try again.")

