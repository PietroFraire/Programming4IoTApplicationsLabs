import cherrypy
import requests
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

    def POST(self, *uri, **_params):
        if (len(uri)) == 0:
            return json.dumps(self.devices)
        elif (len(uri)) == 1 and uri[0] == "addDevice":
            data = json.loads(cherrypy.request.body.read())
            self.devices["devicesList"].append(data)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.devices, f, indent=4, ensure_ascii=False)
            return json.dumps(self.devices)
        else: return cherrypy.HTTPError(400, "Invalid request")

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()  
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
            
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.devices, f, indent=4, ensure_ascii=False)
            return self.devices
        
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
