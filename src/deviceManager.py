import cherrypy
import json

# main is the maincherrypy to check if it works, run maincherrypy
class DeviceManager:
    exposed = True

    def __init__(self, path = "../Data/devices.json"):
        with open(path, "r") as file:
            self.devices = json.load(file)


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
