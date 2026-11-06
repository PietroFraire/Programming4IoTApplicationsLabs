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
                
            else:
                raise cherrypy.HTTPError(502, f"External API failed with status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise cherrypy.HTTPError(503, f"Network error when connecting to Bicing: {str(e)}")


        stations = bike_data.get('stations')
        if len(uri) == 0:
            raise cherrypy.HTTPError(400, "Endpoint not found")

        if uri[0] == 'slots':
            pass


        if uri[0] == 'bikes': 
            try:
                N = int(param.get('N', '10')) #check params else deault value
            except ValueError:
                raise cherrypy.HTTPError(400, "Params must be int")

            order = param.get('order', 'false').lower() not in ['false', 'f'] #else True or descending

            sorted_stations = sorted(stations, key=lambda item: item.get("bikes"), reverse=order)
            limited_stations = sorted_stations[:N]

            return json.dumps(limited_stations)

        if uri[0] == 'e_bikes':
                    pass
        

        if uri[0] == 'count':
                    pass

        else:
            raise cherrypy.HTTPError(400, "Wrong URI type")

