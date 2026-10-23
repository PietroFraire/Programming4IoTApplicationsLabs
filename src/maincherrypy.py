import cherrypy
from deviceManager import DeviceManager
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

    cherrypy.tree.mount(DeviceManager(),'/',conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
