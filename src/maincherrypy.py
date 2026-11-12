import cherrypy
import os
from deviceManager import DeviceManager
from ruleController import RuleController 
from bikeSharingCatalog import BikeSharingCatalog
from fileManager import FileManager

if __name__ == "__main__":
    rest_conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        }
    }

    static_conf = {
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath('./css')
        }, 
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath('./js')
        }, 
    }

    cherrypy.tree.mount(FileManager(), '/fileManager', rest_conf)
    cherrypy.tree.mount(DeviceManager(), '/device', rest_conf)
    cherrypy.tree.mount(RuleController(), '/rules', rest_conf)
    cherrypy.tree.mount(BikeSharingCatalog(), '/bikeSharing', rest_conf)

    cherrypy.tree.mount(None, '/', static_conf)

    cherrypy.config.update({
        'engine.autoreload.on': False,
        'server.socket_host': 'localhost',
        'server.socket_port': 8080
    })
    
    print("Server avviato correttamente su http://localhost:8080")
    cherrypy.engine.start()
    cherrypy.engine.block()