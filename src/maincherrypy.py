import cherrypy
import os
from deviceManager import DeviceManager
from ruleController import RuleController 
from bikeSharingCatalog import BikeSharingCatalog
import os

if __name__=="__main__":
    conf={

        '/':{
                'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
                'tools.staticdir.root': os.path.abspath(os.getcwd()),
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
                #'tools.json_out.on': True,
                'tools.sessions.on': True,
        }, 

        '/css':{
                'tools.staticdir.on': True,
                'tools.staticdir.dir':'./css'
        }, 
        '/js':{
                'tools.staticdir.on': True,
                'tools.staticdir.dir':'./js'
        }, 
    }

    device_conf = {
        '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        }
    }

    rest_conf = {
        '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        }
    }

    bike_conf = {
        '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        }
    }

    #cherrypy.tree.mount(DeviceManager(), '/', conf)
    cherrypy.tree.mount(BikeSharingCatalog(), '/bikeSharing', conf)
    #cherrypy.tree.mount(RuleController(), '/rules', rest_conf)
    cherrypy.tree.mount(BikeSharingCatalog(), '/', bike_conf)
    cherrypy.config.update({'engine.autoreload.on': False})
    cherrypy.engine.start()
    cherrypy.engine.block()
