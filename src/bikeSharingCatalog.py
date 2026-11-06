#manage bike sharing in Barcelona
import json
import cherrypy
import requests

class BikeSharingCatalog:
    exposed = True
    def __init__(self):
        pass

    def GET(self, *uri, **param):
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

