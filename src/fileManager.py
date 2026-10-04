import json
from pprint import pprint
from Device import Device

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

if __name__ == "__main__":

    sensorFile = FileManager()

    d1 = sensorFile.searchByName('DHT11')
    for d in d1:
        print(d.__str__())
        print("---------------")
    d2 = sensorFile.searchByName('DHT1111')
    print(d2.__str__())


    d3 = sensorFile.searchByID(2)
    print(d3.__str__())

    d4 = sensorFile.searchByID(4)
    print(d4.__str__())