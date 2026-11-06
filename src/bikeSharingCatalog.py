#manage bike sharing in Barcelona
import json
import cherrypy
import requests

class BikeSharingCatalog:
    exposed = True
    def __init__(self,  url = "https://www.bicing.barcelona/en/get-stations"):
        self.url = url

    def GET(self, *uri, **param):
        try:
            response = requests.get(self.url, timeout=10)
            if response.status_code == 200:
                bike_data = response.json()
                cherrypy.response.headers['Content-Type'] = 'application/json'
                return json.dumps(bike_data)
                
            else:
                raise cherrypy.HTTPError(502, f"External API failed with status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise cherrypy.HTTPError(503, f"Network error when connecting to Bicing: {str(e)}")



        if len(uri) == 0:
            raise cherrypy.HTTPError(400, "Endpoint not found")

        if uri[0] == 'slots':
            pass


        if uri[0] == 'bikes':
                    pass
        

        if uri[0] == 'e_bikes':
                    pass
        

        if uri[0] == 'count':
                    pass

        else:
            raise cherrypy.HTTPError(400, "Wrong URI type")

