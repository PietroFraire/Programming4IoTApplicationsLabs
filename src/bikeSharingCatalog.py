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
            if response.status_code != 200:
                raise cherrypy.HTTPError(502, f"External API failed with status: {response.status_code}")                               
            bike_data = response.json()
            cherrypy.response.headers['Content-Type'] = 'application/json'
        except requests.exceptions.RequestException as e:
            raise cherrypy.HTTPError(503, f"Network error when connecting to Bicing: {str(e)}")

        if len(uri) == 0:
            raise cherrypy.HTTPError(400, "Endpoint not found")

        stations = bike_data.get('stations', [])

        if uri[0] == 'slots':
            try:
                N = int(param.get('N', '10')) #check params else default value
            except ValueError:
                raise cherrypy.HTTPError(400, "Params must be int")
        
            order = param.get('order', 'descending')
            selected = []

            selected = stations[:N]
            
            if order == 'ascending':
                selected.sort(key=lambda x: int(x['slots']) - int(x['bikes']), reverse=True)
            elif order == 'descending':
                selected.sort(key=lambda x: int(x['slots']) - int(x['bikes']))
            
            print(json.dumps(selected))
            
            return json.dumps(selected).encode('utf-8')
            

        if uri[0] == 'bikes': 
            try:
                N = int(param.get('N', 10)) #check params else default value
            except ValueError:
                raise cherrypy.HTTPError(400, "Params must be int")

            order = param.get('order', 'false').lower() not in ['false', 'f'] #else True or descending

            sorted_stations = sorted(stations, key=lambda item: item.get("bikes"), reverse=order)
            limited_stations = sorted_stations[:N]

            return json.dumps(limited_stations).encode('utf-8')

        if uri[0] == 'e_bikes': # -Pietro

            avaiable_e_bikes = int(param.get("N", 10))
            free_slots = int(param.get("M", 5))
            selected_stations = []

            for station in stations:
               if station["electrical_bikes"] >= avaiable_e_bikes and (station["slots"]-station["bikes"]) >= free_slots:
                   selected_stations.append(station)

            return json.dumps(selected_stations).encode('utf-8')
        

        if uri[0] == 'count':
            total_available_bikes = 0
            total_free_slot = 0
            for station in stations:
                total_available_bikes += int(station["bikes"])
                total_free_slot += int(station["slots"])
            result = {
                "total_available_bikes": total_available_bikes,
                "total_free_slots": total_free_slot   
            }
            return json.dumps(result).encode('utf-8')
        
        else:
            raise cherrypy.HTTPError(400, "Wrong URI type")

