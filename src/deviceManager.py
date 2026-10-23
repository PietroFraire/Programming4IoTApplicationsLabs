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

    def DELETE():
        pass
