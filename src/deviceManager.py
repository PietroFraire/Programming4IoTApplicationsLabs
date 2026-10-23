import cherrypy
import requests
import json

# main is the maincherrypy to check if it works, run maincherrypy
class DeviceManager:

    def GET():
        pass

    def POST():
        pass

    def PUT(self, *uri, **param):
        if len(uri) <= 0:
            raise cherrypy.HTTPError(400, "The URL is wrong. ")
        
        if len(uri) == 2 and uri[0] == "updateDevice":
            body = cherrypy.request.json            
            deviceID=uri[1]
            list = self.deviceList["devicesList"]
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
                json.dump(self.deviceList, f, indent=4, ensure_ascii=False)        
            return self.deviceList

        raise cherrypy.HTTPError(400, "Wrong endpoint. ")
    
    def DELETE():
        pass
