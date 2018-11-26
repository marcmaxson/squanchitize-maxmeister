#!/usr/local/bin/python3.7
import cherrypy
import content

class Root(object):
    @cherrypy.expose
    def index(self):
        return content.index()

    @cherrypy.expose
    def save_content(self):
        return content.save_content()

    @cherrypy.expose
    def dashboard(self):
        return content.dashboard()
    
    @cherrypy.expose
    def admin(self,**kw):
        if kw.get('obscure-password') == 'emskesmlk23': #quick way to RESET cherrypy whilst debugging
            cherrypy.engine.restart()
            return 'Yes SIR! CherryPy RESETTING! <br> requested by '+str(cherrypy.request.headers["X-Forwarded-For"])
    
# because of the 2-hour constraint, I am just using built-in user session feature of cherrypy to store user details.
    
cherrypy.config.update({
    'environment': 'production',
    'log.screen': False,
    'server.socket_host': '127.0.0.1',
    'server.socket_port': 29565,
    'request.show_tracebacks':True, #error messages return stack traces
    'tools.sessions.on': True, #user creds dictionary is at cherrypy.session['fieldname'] = 'fieldvalue' / cherrypy.session.get('fieldname')
    })
cherrypy.quickstart(Root())
