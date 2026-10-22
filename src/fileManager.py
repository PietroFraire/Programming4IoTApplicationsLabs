import json

class Device:
    def __init__(self, deviceID, deviceName, measureType, availableServices, servicesDetails, lastUpdate):
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.measureType = measureType
        self.availableServices = availableServices
        self.servicesDetails = servicesDetails
        self.lastUpdate = lastUpdate
    
    def __str__(self):
        return f"""
                Device: {self.deviceName}, 
                ID: {self.deviceID},
                Type: {self.measureType}
                availableServices: {self.availableServices}
                servicesDetails: {self.servicesDetails}
                lastUpdate: {self.lastUpdate}
                """
    def __repr__(self):
        return self.__str__()

        

class FileManager:
    def __init__(self):
        self.filepath = "../Data/catalog.json"
        with open(self.filepath, "r") as file:
            self.catalog = json.load(file)
        self.devicelist = self.loading_devices()

    def loading_devices(self):
        loaded_devices = []
        device_list = self.catalog.get("devicesList", [])

        for device in device_list:
            d = Device(
                device.get("deviceID"),
                device.get("deviceName"),
                device.get("measureType"),
                device.get("availableServices"),
                device.get("servicesDetails"), 
                device.get("lastUpdate")
            )
            loaded_devices.append(d)
        return loaded_devices

    def searchByName(self, deviceName):
        for d in self.devicelist:
            if(d.deviceName == deviceName):
                return d
        return None
    
    def searchByID(self, deviceID):
        for d in self.devicelist:
            if(d.deviceID == deviceID):
                return d
        return None

        

if __name__ == "__main__":
    manager = FileManager()
    
    device_name = input("Enter device name: ").strip()
    result = manager.searchByName(device_name)
    if result is not None:
        print("Device found: ")
        print(result)
    else:
        print(f"Sorry, no device named '{device_name}' was found.")

    device_id = int(input("Enter device id: ").strip())
    result = manager.searchByID(device_id)
    if result is not None:
        print("Device found: ")
        print(result)
    else:
        print(f"Sorry, no device id '{device_id}' was found.")
