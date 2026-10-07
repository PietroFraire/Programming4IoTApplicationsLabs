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
        Function for searching for a device \n
        Input param: str name \n
        Output: str value
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
        for d in self.devices.values():
            for s in d.avaiableServices:
                if s == service:
                    print(d)
                    print("----------------")

    def searchByMeasureType(self, measure:str):
        """
        Function for searching devices by measure type
        Input param: str measure (e.g., 'Temperature')
        """
        for d in self.devices.values():
            if measure in d.measureType:
                print(d)
                print("----------------")

    def insertDevice(self, device:Device):
        device.lastUpdate = datetime.now().strftime("%Y-%m-%d %H:%M")
        if device.deviceID not in self.devices:
            self.devices[device.deviceID] = device              
            self.dictJFile["devicesList"].append({
                "deviceID": device.deviceID,
                "deviceName": device.deviceName,
                "measureType": device.measureType,
                "availableServices": device.avaiableServices,
                "servicesDetails": device.servicesDetails,
                "lastUpdate": device.lastUpdate
            })


            return True
        else:
            print("Device already exists!")
            if input("Update existing device? (y/n): ").lower() == 'y':
                self.devices[device.deviceID] = device
                for d in self.dictJFile["devicesList"]:
                    if d["deviceID"] == device.deviceID:
                        d["deviceName"] = device.deviceName
                        d["measureType"] = device.measureType
                        d["availableServices"] = device.avaiableServices
                        d["servicesDetails"] = device.servicesDetails
                        d["lastUpdate"] = device.lastUpdate
                        break

                return True
            return False
    
    def printAll(self):
        for d in self.devices:
            print(self.devices[d])
            print("----------------")

    def exit(self):
        """
        Saves the catalog if changes have been made to dictJFile
        """
        try:
            with open(self.filePath, 'r') as f:
                disk_content = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            disk_content = None

        if self.dictJFile != disk_content:
            with open(self.filePath, 'w') as f:
                json.dump(self.dictJFile, f, indent=4)
            print("Catalog saved successfully.")
        else:
            print("No changes detected, skip saving.")

if __name__ == "__main__":

    sensorFile = FileManager(filePath = "C:/Users/lferr/OneDrive/Desktop/IoT/Programming4IoTApplicationsLabs/Data/catalog.json")

    d1 = sensorFile.searchByName('DHT11')
    for d in d1:
        print(d.__str__())
        print("---------------")
    d2 = sensorFile.searchByName('DHT1111')
    print(f"{d2}\n")
    
    d3 = sensorFile.searchByID(2)
    print(f"{d3}\n")

    d4 = sensorFile.searchByService("MQTT")