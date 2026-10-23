import cherrypy
import json

# main is the maincherrypy to check if it works, run maincherrypy
class DeviceManager:

    def __init__(self, path = "../Data/devices.json"):
        self.path = path
        self.devices = json.load(open(path))


    def GET():
        pass

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