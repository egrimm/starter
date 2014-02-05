"""
Using redirect route instead of simple routes since it supports strict_slash
Simple route: http://webapp-improved.appspot.com/guide/routing.html#simple-routes
RedirectRoute: http://webapp-improved.appspot.com/api/webapp2_extras/routes.html#webapp2_extras.routes.RedirectRoute
"""

from webapp2_extras.routes import RedirectRoute
import handlers

secure_scheme = 'https'

_routes = [
    RedirectRoute('/register',
        handlers.RegisterHandler,
        name='register',
        strict_slash=True),
    RedirectRoute('/dashboard',
        handlers.DashboardHandler,
        name='dashboard',
        strict_slash=True),
    RedirectRoute('/',
        handlers.MainHandler,
        name='home',
        strict_slash=True),
]

def get_routes():
    return _routes

def add_routes(app):
    if app.debug:
        secure_scheme = 'http'
    for r in _routes:
        app.router.add(r)