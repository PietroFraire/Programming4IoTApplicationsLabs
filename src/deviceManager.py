import cherrypy
<<<<<<< HEAD
<<<<<<< HEAD
=======
import requests
>>>>>>> f316668c7341fe5ae98903c1aac13116847cb553
=======
import requests
>>>>>>> 39fae669a71f4ef964489e4201d6eb985c50136f
import json

# main is the maincherrypy to check if it works, run maincherrypy
class DeviceManager:
<<<<<<< HEAD
<<<<<<< HEAD
    exposed = True
=======
    exposed=True
>>>>>>> 39fae669a71f4ef964489e4201d6eb985c50136f

    def __init__(self, path = "../Data/devices.json"):
        with open(path, "r") as file:
            self.devices = json.load(file)
<<<<<<< HEAD


    def GET(self, *uri, **_params):
        pass

    def POST(self, *uri, **_params):
        if (len(uri)) == 0:
            return json.dumps(self.devices)
        elif (len(uri)) == 1 and uri[0] == "addDevice":
            data = json.loads(cherrypy.request.body.read())
            self.devices.append(data)
            with open(self.path, "w") as file:
                json.dump(self.devices, file)
            return json.dumps({"message": "Device added successfully"})
        else: return cherrypy.HTTPError(400, "Invalid request")

    def PUT(self, *uri, **_params):
        raise cherrypy.HTTPError(501, "PUT is not implemented")

    def DELETE(self, *uri, **_params):
        raise cherrypy.HTTPError(501, "DELETE is not implemented")
=======
    exposed=True

    def __init__(self, path = "../Data/devices.json"):
        self.path = path
        self.devices = json.load(open(path))

        with open(path, "r") as file:
            self.devices = json.load(file)
=======
>>>>>>> 39fae669a71f4ef964489e4201d6eb985c50136f

    def GET(self, *uri, **param):
        if len(uri)==0:
            return open("../Data/index.html") 
        elif len(uri) == 1 and uri[0] == "devicesList":
                return json.dumps(self.devices)
        else:
            raise cherrypy.HTTPError(400, "Bad Request")

    def POST(self, *uri, **_params):
        if (len(uri)) == 0:
            return json.dumps(self.devices)
        elif (len(uri)) == 1 and uri[0] == "addDevice":
            data = json.loads(cherrypy.request.body.read())
            self.devices["devicesList"].append(data)
            return json.dumps(self.devices)
        else: return cherrypy.HTTPError(400, "Invalid request")

    def PUT(self, *uri, **param):
        if len(uri) <= 0:
            raise cherrypy.HTTPError(400, "The URL is wrong. ")
        
        if len(uri) == 2 and uri[0] == "updateDevice":
            body = cherrypy.request.json            
            deviceID=uri[1]
            list = self.devices["devicesList"]
            found = False
            
            for d in list:
                if d["deviceID"] == deviceID:
                    d["deviceName"] = body["deviceName"] 
                    d["measureType"] = body["measureType"]
                    d["unit"] = body["unit"]
                    found = True
            
            if found:
                print(f"device with {deviceID} uploaded")
            else:
                raise cherrypy.HTTPError(404, "Device not found")            
            
            with open("device.json", "w", encoding="utf-8") as f:
                json.dump(self.devices, f)
            return self.deviceList
        
        raise cherrypy.HTTPError(400, "Wrong endpoint. ")

    def DELETE(self, *uri, **param):

        if len(uri)!=2 or uri[0] != "deleteDevice":
            raise cherrypy.HTTPError(400, "Bad request")
        
        dev = self.devices["devicesList"]
        id = uri[1]
        for d in dev:
            if d["deviceID"] == id:
                dev.remove(d)

                with open(self.path, "w", encoding="utf-8") as f:
                    json.dump(self.devices, f)
                    
                return json.dumps(self.devices).encode()

        raise cherrypy.HTTPError(404, "Device not found")
<<<<<<< HEAD
>>>>>>> f316668c7341fe5ae98903c1aac13116847cb553
=======
>>>>>>> 39fae669a71f4ef964489e4201d6eb985c50136f
