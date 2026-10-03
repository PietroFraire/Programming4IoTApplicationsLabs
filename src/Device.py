class Device():

    def __init__(self, deviceID, deviceName, 
                 measureType, avaiableServices, servicesDetails, lastUpdate):

        self.deviceID = deviceID
        self.deviceName = deviceName
        self.measureType = measureType
        self.avaiableServices = avaiableServices
        self.servicesDetails = servicesDetails
        self.lastUpdate = lastUpdate

    def __str__(self):

        buf = [
            f"Device ID: {self.deviceID}",
            f"Device Name: {self.deviceName}",
            f"Measure Type: {', '.join(self.measureType)}",
            f"Avaiable Services: {', '.join(self.avaiableServices)}",
            "Service Details: "
        ]

        for s in self.servicesDetails:
            for key, value in s.items():
                if isinstance(value, list):
                    buf.append(f"\t{key:}")
                    for e in value:
                        buf.append(f"\t- {e}")
                else:
                    buf.append(f"\t{key}: {value}")

        buf.append(f"Last Update: {self.lastUpdate}")

        return "\n".join(buf)

    