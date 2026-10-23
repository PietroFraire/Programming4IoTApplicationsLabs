import cherrypy
import os
from deviceManager import DeviceManager
from ruleController import RuleController  # <-- DA AGGIUNGERE
import os

if __name__=="__main__":
    conf={

        '/':{
                'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
                'tools.staticdir.root': os.path.abspath(os.getcwd()),
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

    rest_conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        }
    }

    cherrypy.tree.mount(DeviceManager(),'/',conf)
    cherrypy.tree.mount(RuleController(), '/rules', rest_conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
