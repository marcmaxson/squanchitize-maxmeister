#!/usr/local/bin/python3.7
import cherrypy

class Root(object):
    @cherrypy.expose
    def index(self):
            return 'Hello, this is your default site.'

cherrypy.config.update({
    'environment': 'production',
    'log.screen': False,
    'server.socket_host': '127.0.0.1',
    'server.socket_port': 29565,
})
cherrypy.quickstart(Root())
