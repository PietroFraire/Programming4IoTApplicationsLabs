import json
import cherrypy
import requests

URL = "http://127.0.0.1:8080"
#URL = "http://localhost:8080"

class RuleClient:

    def __init__(self):
        pass

    def getRules(self): 
        url = f"{URL}/rules"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

                all_rules = data.get('list_of_rules', {})
                print(f"All rules ({len(all_rules)}):")
                if all_rules:
                    for name, details in all_rules.items():
                        print(f"[{details.get('type')}] {name} -> Soglia: {details.get('threshold')}")
                else:
                    print("No rules listed.")

            else:
                print(f"\n Error of server (Code {response.status_code}): {response.text}")

        except requests.exceptions.ConnectionError:
            print("\n Error when connecting: Impossible to reach the server.")

    def addRule(self):
        print(f'\n--- Add a rule ---')
        rule_type = input("Insert the type of rule you want to add: ").strip().lower()
        rule_name = input("Insert the name of the rule you want to add: ").strip()
        rule_thrs_raw = input("Insert the threshold of the rule you added: ").strip()

        if not rule_type or not rule_name or not rule_thrs_raw:
            print("Error: missing input param")
            return 

        try:
            rule_thrs = float(rule_thrs_raw)
        except ValueError:
            print("Error: threshold must be a valid number")
            return

        data = {
            "rule_type": rule_type,
            "rule_name": rule_name,
            "threshold": rule_thrs
        }

        url = f"{URL}/rules/addRule"

        try:
            response = requests.post(url, json=data, timeout=5)
                    
            response.raise_for_status()
            print(response.json().get("message", "Rule added."))

        except requests.exceptions.ConnectionError:
            print("\n Error when connecting: Impossible to reach the server.")
        

    def evaluate(self):
        pass

    def update(self):
        pass

    def delete(self):
        print("\n--- Delete a rule ---")
        rule_name = input("Insert the name of the rule that you want to delete: ").strip()
        
        if not rule_name:
            print("Error: missing name.")
            return

        url = f"{URL}/rules/{rule_name}"

        try:
            response = requests.delete(url)
            
            if response.status_code == 200:
                data = response.json()
                print("\n Success: rule delete!")
                print(f"  - Rule name: {data.get('rule_name')}")
                print(f"  - Type: {data.get('rule_type')}")
                print(f"  - Previous threshold: {data.get('threshold')}")
                
                remaining_rules = data.get('list_of_rules', {})
                print(f"   - Remaining rule ({len(remaining_rules)}):")
                if remaining_rules:
                    for name, details in remaining_rules.items():
                        print(f"[{details.get('type')}] {name} -> Soglia: {details.get('threshold')}")
                else:
                    print("No rules remaining.")
                    
            elif response.status_code == 404:
                print(f"\n Error: the rule '{rule_name}' isn't find on the server.")
            else:
                print(f"\n Error of server (Code {response.status_code}): {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("\n Error of connession: Impossible to reach the server.")

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

        