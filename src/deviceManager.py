import cherrypy
import json

# main is the maincherrypy to check if it works, run maincherrypy
class DeviceManager:
    exposed=True

    def __init__(self, path = "../Data/devices.json"):
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

    def DELETE():
        pass
