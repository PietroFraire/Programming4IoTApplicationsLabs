import json
from datetime import datetime

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

    def insertDevice(self, deviceID, deviceName, measureType, availableServices, servicesDetails):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        existing_device = self.searchByID(deviceID)

        if existing_device:
            existing_device.deviceName = deviceName
            existing_device.measureType = measureType
            existing_device.availableServices = availableServices
            existing_device.servicesDetails = servicesDetails
            existing_device.lastUpdate = current_time

            for d in self.catalog["devicesList"]:
                if d["deviceID"] == deviceID:
                    d["deviceName"] = deviceName
                    d["measureType"] = measureType
                    d["availableServices"] = availableServices
                    d["servicesDetails"] = servicesDetails
                    d["lastUpdate"] = current_time
                    break
        else:
            new_dev = Device(deviceID, deviceName, measureType, availableServices, servicesDetails, current_time)
            self.devicelist.append(new_dev)
            new_dict = {
                "deviceID": deviceID,
                "deviceName": deviceName,
                "measureType": measureType,
                "availableServices": availableServices,
                "servicesDetails": servicesDetails,
                "lastUpdate": current_time
                }
            self.catalog["devicesList"].append(new_dict)
        

        

if __name__ == "__main__":
    manager = FileManager()

    while True:
        # 1. Print the menu options
        print("\n--- Device Manager Menu ---")
        print("1. Search by Name")
        print("2. Search by ID")
        print("3. Search by Service")
        print("4. Search by Measure Type")
        print("5. Insert device")
        print("6. Print all devices")
        print("7. Save and Exit")


        choice = input("\nEnter your choice (1-7): ").strip()

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
                try:
                    device_ID = int(input("Enter device ID: ").strip())
                    
                    existing = manager.searchByID(device_ID)
                    
                    if existing:
                        print(f"\n--- Updating Existing Device: {existing.deviceName} ---")
                        print("(Press ENTER to keep the current value)")
                        
                        # 2. Use 'or' to keep the old data if the user just presses Enter
                        device_name = input(f"Enter name [{existing.deviceName}]: ").strip() or existing.deviceName
                        
                        m_input = input(f"Enter measuring types [{','.join(existing.measureType)}]: ").strip()
                        measureType = [m.strip() for m in m_input.split(",")] if m_input else existing.measureType
                        
                        s_input = input(f"Enter available services [{','.join(existing.availableServices)}]: ").strip()
                        availableServices = [s.strip().upper() for s in s_input.split(",")] if s_input else existing.availableServices

                        if s_input:
                            service_details = []
                            for service in availableServices:
                                if service == "MQTT":
                                    topics_input = input("Enter MQTT topics (separated by commas): ")
                                    topics_list = [t.strip() for t in topics_input.split(",")]
                                    service_details.append({"serviceType": "MQTT", "topic": topics_list})
                                elif service == "REST":
                                    ip_input = input("Enter REST service IP (e.g. 192.1.1.1:8080): ").strip()
                                    service_details.append({"serviceType": "REST", "serviceIP": ip_input})
                        else:
                            service_details = existing.servicesDetails
                    
                    else:
                        print(f"\n--- Creating New Device: {device_ID} ---")
                        device_ID = int(input("Enter device ID: ").strip())
                        device_name = input("Enter the device name: ").strip()

                        measures_input = input("Enter measuring types (separated by commas, e.g. Temperature,Humidity): ")
                        measureType = [m.strip() for m in measures_input.split(",")]

                        services_input = input("Enter available services (separated by commas, e.g. MQTT,REST): ")
                        availableServices = [s.strip().upper() for s in services_input.split(",")]

                        service_details = []
                        print("--- Service Details Configuration ---")
                        for service in availableServices:
                                if service == "MQTT":
                                    topics_input = input("Enter MQTT topics (separated by commas): ")
                                    topics_list = [t.strip() for t in topics_input.split(",")]
                                    serivce_details.append({
                                        "serviceType": "MQTT", 
                                        "topic": topics_list
                                    })
                                    
                                elif service == "REST":
                                    ip_input = input("Enter REST service IP (e.g. 192.1.1.1:8080): ").strip()
                                    serivce_details.append({
                                        "serviceType": "REST", 
                                        "serviceIP": ip_input
                                    })

                    manager.insertDevice(device_ID, device_name, measureType, availableServices, service_details)
                    print(f"Device {device_ID} successfully processed!")

                except ValueError:
                    print("the ID must be an integer")

            
            case '6':
                print(manager.printAll())

            case '7':
                manager.save_catalog()
                print("Catalog saved successfully. Exiting program...")
                break
        
            case _:
                print("Invalid choice. Please enter a number between 1 and 7.")