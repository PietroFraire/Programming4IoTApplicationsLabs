import json
import cherrypy
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
    exposed = True

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


    def GET(self, *uri, **param):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        
        if len(uri) > 0:
            raise cherrypy.HTTPError(404, "Endpoint not found")

        if not param:
            return self.printAll().encode('utf-8')

        if 'id' in param:
            res = self.searchByID(param['id'])
            if not res:
                raise cherrypy.HTTPError(404, "Device not found")
            device_dict = {
                "deviceID": res.deviceID, "deviceName": res.deviceName,
                "measureType": res.measureType, "availableServices": res.availableServices,
                "servicesDetails": res.servicesDetails, "lastUpdate": res.lastUpdate
            }
            return json.dumps(device_dict).encode('utf-8')

        elif 'sensname' in param:
            res = self.searchByName(param['sensname'])
            if not res:
                raise cherrypy.HTTPError(404, "Device not found")
            device_dict = {
                "deviceID": res.deviceID, "deviceName": res.deviceName,
                "measureType": res.measureType, "availableServices": res.availableServices,
                "servicesDetails": res.servicesDetails, "lastUpdate": res.lastUpdate
            }
            return json.dumps(device_dict).encode('utf-8')

        elif 'service' in param:
            results = self.searchByService(param['service'])
            dev_list = [{
                "deviceID": r.deviceID, "deviceName": r.deviceName,
                "measureType": r.measureType, "availableServices": r.availableServices,
                "servicesDetails": r.servicesDetails, "lastUpdate": r.lastUpdate
            } for r in results]
            return json.dumps(dev_list).encode('utf-8')

        elif 'measure' in param:
            results = self.searchByMeasureType(param['measure'])
            dev_list = [{
                "deviceID": r.deviceID, "deviceName": r.deviceName,
                "measureType": r.measureType, "availableServices": r.availableServices,
                "servicesDetails": r.servicesDetails, "lastUpdate": r.lastUpdate
            } for r in results]
            return json.dumps(dev_list).encode('utf-8')

        else:
            raise cherrypy.HTTPError(400, "Invalid query parameters")

    def POST(self, *uri, **_params):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        if len(uri) > 0:
            raise cherrypy.HTTPError(400, "Invalid request path")
        
        body = cherrypy.request.body.read()
        if not body:
            raise cherrypy.HTTPError(400, "Missing request body")
        
        data = json.loads(body)
        
        # Sfruttiamo il metodo insertDevice già scritto che gestisce controllo ID e data lastUpdate
        self.insertDevice(
            data.get("deviceID"),
            data.get("deviceName"),
            data.get("measureType"),
            data.get("availableServices"),
            data.get("servicesDetails")
        )
        
        # Aggiorniamo la lista in memoria degli oggetti Device
        self.devicelist = self.loading_devices()
        
        cherrypy.response.status = 201
        return json.dumps(self.catalog).encode('utf-8')

    def PUT(self, *uri, **param):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        # Utilizziamo l'URI per passare l'ID (es. /fileManager/1) oppure sfruttiamo la POST/insertDevice
        if len(uri) != 1:
            raise cherrypy.HTTPError(400, "Invalid URL. Use /fileManager/DEVICE_ID")
        
        deviceID = uri[0]
        existing = self.searchByID(deviceID)
        if not existing:
            raise cherrypy.HTTPError(404, "Device not found")
            
        body = cherrypy.request.body.read()
        if not body:
            raise cherrypy.HTTPError(400, "Missing request body")
            
        body_data = json.loads(body)
        
        # Aggiorna usando i dati del body (mantenendo quelli vecchi se non specificati)
        self.insertDevice(
            deviceID,
            body_data.get("deviceName", existing.deviceName),
            body_data.get("measureType", existing.measureType),
            body_data.get("availableServices", existing.availableServices),
            body_data.get("servicesDetails", existing.servicesDetails)
        )
        
        self.devicelist = self.loading_devices()
        return json.dumps(self.catalog).encode('utf-8')

    def DELETE(self, *uri, **param):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        if len(uri) != 1:
            raise cherrypy.HTTPError(400, "Invalid URL. Use /fileManager/DEVICE_ID")
        
        target_id = uri[0]
        existing = self.searchByID(target_id)
        if not existing:
            raise cherrypy.HTTPError(404, "Device not found")

        # Rimuove sia dalla lista in memoria che dal catalogo dict
        self.devicelist = [d for d in self.devicelist if str(d.deviceID) != str(target_id)]
        self.catalog["devicesList"] = [d for d in self.catalog["devicesList"] if str(d["deviceID"]) != str(target_id)]
        
        self.save_catalog()
            
        return json.dumps(self.catalog).encode('utf-8')