import json

class FileManager:
    """
    class for managing json files \n
    file path for json sensorfile is hardcoded
    """
    def __init__(self):
        self.filePath = '../data/catalog.json'
        self.dictJFile = json.load(open(self.filePath))
    

    def searchByName(self, name:str):
        """
        Function for searching for a device \n
        Input param: str name \n
        Output: str value
        """

        for i in range(len(self.dictJFile['devicesList'])):
            if self.dictJFile['devicesList'][i]['deviceName'] == name:

                print(f"Info sensor {self.dictJFile['devicesList'][i]['deviceID']}: {self.dictJFile['devicesList'][i]['deviceName']}")
                print(f'deviceName: {self.dictJFile['devicesList'][i]['deviceName']} \n')
                print(f'deviceID: {self.dictJFile['devicesList'][i]['deviceID']} \n')
                print(f'measureType: {self.dictJFile['devicesList'][i]['measureType']} \n')
                print(f'availableServices: {self.dictJFile['devicesList'][i]['availableServices']} \n')
                print(f'servicesDetails: {self.dictJFile['devicesList'][i]['servicesDetails']} \n')
                print(f'lastUpdate: {self.dictJFile['devicesList'][i]['lastUpdate']} \n')
                print("---------------------------")

        else:
            print(f"The sensor '{name}' does not exist in sensor list")

    def searchByID(self, id:int):
        """
        Function for searching for sensor id in json file \n
        Input param: int id \n
        Output: str value
        """

        for k, v in self.dictJFile.items():
            if (k=='deviceID' and v==id):
                print(f'{k} {v}')

if __name__ == "__main__":

    sensorFile = FileManager()

    sensorFile.searchByName('projectOwner')
    sensorFile.searchByName('DHT1111')