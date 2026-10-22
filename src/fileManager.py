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

    def searchByService(self, service):
        dev = []
        for d in self.devicelist:
            if service in d.availableServices:
                dev.append(d)
        return dev
    
    def searchByMeasureType(self, measureType):
        dev = []
        for d in self.devicelist:
            if measureType in d.measureType:
                dev.append(d)
        return dev
    
    def printAll(self):
        return json.dumps(self.catalog)
    
    def save_catalog(self):
        with open(self.filepath, "w") as file:
            json.dump(self.catalog, file, indent=4)

        

if __name__ == "__main__":
    manager = FileManager()

    while True:
        # 1. Print the menu options
        print("\n--- Device Manager Menu ---")
        print("1. Search by Name")
        print("2. Search by ID")
        print("3. Search by Service")
        print("4. Search by Measure Type")
        print("5. Print all devices")
        print("6. Save and Exit")


        choice = input("\nEnter your choice (1-6): ").strip()

        match choice:
            case '1':
                device_name = input("Enter device name: ").strip()
                result = manager.searchByName(device_name)
                if result is not None:
                    print("Device found: ")
                    print(result)
                else:
                    print(f"Sorry, no device named '{device_name}' was found.")
  
            case '2':
                try:
                    device_id = int(input("Enter device id: ").strip())
                    result = manager.searchByID(device_id)
                    if result is not None:
                        print("Device found: ")
                        print(result)
                    else:
                        print(f"Sorry, no device id '{device_id}' was found.")
                except ValueError:
                    print("Error: Please enter a valid integer.")

            case '3':
                service = input("Enter service: ").strip()
                listdev = manager.searchByService(service)
                print(listdev if listdev else f"No device with this service type {service}")

            case '4':
                measureType = input("Enter measure type: ").strip()
                listdev = manager.searchByMeasureType(measureType)
                print(listdev if listdev else f"No device with this measure type {measureType}")
            
            case '5':
                print(manager.printAll())

            case '6':
                manager.save_catalog()
                print("Catalog saved successfully. Exiting program...")
                break
        
            case _:
                print("Invalid choice. Please enter a number between 1 and 6.")