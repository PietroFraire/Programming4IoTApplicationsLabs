import json
from pprint import pprint
from Device import Device
from datetime import datetime

class FileManager:
    """
    class for managing json files \n
    file path for json sensorfile is hardcoded
    """
    def __init__(self, filePath = '../data/catalog.json'):
        self.filePath = filePath
        self.dictJFile = json.load(open(self.filePath))

        devicesList = self.dictJFile["devicesList"]
        self.devices = {d["deviceID"] : Device(d["deviceID"], d["deviceName"], d["measureType"],
                                                d["availableServices"], d["servicesDetails"], d["lastUpdate"]) for d in devicesList }
    

    def searchByName(self, name:str):
        """
        Function for searching for a device given the name\n
        Input param: str name \n
        Output: list value
        """
        l = []
        for d in self.devices.values():
            if d.deviceName == name:
                l.append(d)

        return l
        
    def searchByID(self, id:int):
        """
        Function for searching for sensor id in json file \n
        Input param: int id \n
        Output: str value
        """

        if id in self.devices:
            return self.devices[id] 
        return None
    
    def searchByService(self, service:str):

        l = []
        for d in self.devices.values():
            if service in d.avaiableServices:
                l.append[d]

        return l

    def searchByMeasureType(self, measureType):

        l= []
        for d in self.devices.values():
            if measureType in d.measureType:
                l.append(d)
        return l
    
    def insertDevice(self):

        new = False
        id = int(input("Device id <int>:"))
        if id in self.devices:
            d = self.devices[id]
            print(f"Id {id} already existing, update information:")
        else:
            print("New Device")
            d = Device(id, None, None, None, None, None)
            new = True

        d.deviceName = input("Name:")

        l = []
        while True:
            m = input("Add a measurement type, write 'done' when you have finished: ")
            if m == "done":
                break
            l.append(m)

        d.measureType = l

        l = []
        while True:
            m = input("Add a service avaiable, write 'done' when you have finished: ")
            if m == "done":
                break
            l.append(m)

        d.avaiableServices = l
        
        l = []
        while True:

            sd = {}
            m = input("Add a service type, write 'done' when you have finished: ")
            if m == "done":
                break

            sd["serviceType"] = m

            if m.upper() == "MQTT":
                topics = []
                while True:
                    t = input("Add a topic, write 'done' when you have finished: ")
                    if t.lower() == "done":
                        break
                    topics.append(t)

                sd["topic"] = topics

                l.append(sd)
                
            if m.upper() == "REST":
                ips = []

                while True:
                    t = input("Add a ip address, write 'done' when you have finished: ")
                    if t.lower() == "done":
                        break
                    ips.append(t)

                sd["ip"] = ips

                l.append(sd)
                
        d.servicesDetails = l
        d.lastUpdate = f"{datetime.now():%Y-%m-%d %H:%M}"
        if new:
            self.devices[id] = d
        # print(d.__str__())

    def printAll(self):
        for d in self.devices.values():
            print(d.__str__())

    def exit(self):

        self.dictJFile["devicesList"].clear()

        for d in self.devices.values():
            self.dictJFile["devicesList"].append(d.to_dict())
        
        with open(self.filePath, "w", encoding="utf-8") as f:
            json.dump(self.dictJFile, f, ensure_ascii=False, indent=2)
            

    def printMenu(self):
        print("---------Menu---------")
        print("Write the corrisponding number:")
        print("<1> Search by name ")
        print("<2> Search by ID ")
        print("<3> Search by service ")
        print("<4> Search by measure type ")
        print("<5> Insert device ")
        print("<6> Print all ")
        print("<7> Exit ")
    

if __name__ == "__main__":

    sensorFile = FileManager()

    while True:
        sensorFile.printMenu()

        c = input("Insert number: ")

        match c:
            case "1":
                s = input("Name: ")
                l = sensorFile.searchByName(s)
                if len(l)>0:
                    for d in l:
                        print(str(d))
                else:
                    print(f"Name {s} not found")
            case "2":
                n = int(input("ID: "))
                d = sensorFile.searchByID(n)
                if d == None:
                    print(f"ID {n} not found")
                else:
                    print(str(d))
            case "3":
                s = input("Service: ")
                sensorFile.searchByService(s)
                if len(l)>0:
                    for d in l:
                        print(str(d))
                else:
                    print(f"Service {s} not found")
            case "4":
                s = input("Measure Type")
                l = sensorFile.searchByMeasureType(s)
                if len(l)>0:
                    for d in l:
                        print(str(d))
                else:
                    print(f"Measure Type {s} not found")
            case "5":
                sensorFile.insertDevice()
            case "6":
                sensorFile.printAll()
            case "7":
                sensorFile.exit()
                print("It's been a pleasure ;)")
                break
            case _:
                print("Unknown command, try again")
