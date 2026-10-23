import cherrypy
import json

# main is the maincherrypy to check if it works, run maincherrypy
class DeviceManager:
    exposed=True

    def __init__(self, path = "../Data/devices.json"):
        self.path = path
        self.devices = json.load(open(path))

        with open(path, "r") as file:
            self.devices = json.load(file)

    def GET(self, *uri, **param):
        if len(uri)==0:
            return open("../Data/index.html") 
        elif len(uri) == 1 and uri[0] == "devicesList":
                return json.dumps(self.devices)
        else:
            raise cherrypy.HTTPError(400, "Bad Request")

    def POST():
        pass

    def PUT():
        pass

    def DELETE(self, *uri, **param):

        if len(uri)!=2 or uri[0] != "deleteDevice":
            raise cherrypy.HTTPError(400, "Bad request")
        
        dev = self.devices["devicesList"]
        id = uri[1]
        for d in dev:
            if d["deviceID"] == id:
                dev.remove(d)

                with open(self.path, "w", encoding="utf-8") as f:
                    json.dumps(self.devices, f)
                    
                return json.dumps(self.devices).encode()

        raise cherrypy.HTTPError(404, "Device not found")