import cherrypy
import json

# main is the maincherrypy to check if it works, run maincherrypy
class DeviceManager:

    def __init__(self, path = "../Data/devices.json"):
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
                return json.dumps(self.devices).encode()

        raise cherrypy.HTTPError(404, "Device not found")