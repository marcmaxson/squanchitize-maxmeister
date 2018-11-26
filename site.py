#!/usr/local/bin/python3.7
import cherrypy
import content

# initialize spacy at boot, since it takes a while.
import spacy
nlp = spacy.load('en_core_web_sm') # POS tagger

class Root(object):
    @cherrypy.expose
    def index(self):
        return content.index()

    @cherrypy.expose
    def save_content(self, **kw):
        return content.save_content(kw, nlp)
    
    @cherrypy.expose
    def login(self, **kw):
        return content.login(kw)
    
    @cherrypy.expose
    def dashboard(self, **kw):
        return content.dashboard(kw)
    
    @cherrypy.expose
    def admin(self, **kw):
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

cherrypy.session['this_user'] = None # prob need to make this a session cookie thing but just testing.
