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
    RedirectRoute('/register-success',
    handlers.RegisterSuccessHandler,
    name='register-success',
    strict_slash=True),
    RedirectRoute('/register-student',
        handlers.RegisterStudentHandler,
        name='register-student',
        strict_slash=True),
    RedirectRoute('/edit-student/<student_id>',
        handlers.EditStudentHandler,
        name='edit-student',
        strict_slash=True),
    RedirectRoute('/util/validate-student/<student_id>',
        handlers.ValidateStudentHandler,
        name='validate-student',
        strict_slash=True),
    RedirectRoute('/util/invite-student/<student_key>',
        handlers.InviteStudentEmailHandler,
        name='invite-student',
        strict_slash=True),
    RedirectRoute('/dashboard',
        handlers.DashboardHandler,
        name='dashboard',
        strict_slash=True),
    RedirectRoute('/student-activation',
        handlers.StudentActivationHandler,
        name='student-activation',
        strict_slash=True),
    RedirectRoute('/student-dashboard',
        handlers.StudentDashboardHandler,
        name='student-dashboard',
        strict_slash=True),
    RedirectRoute('/login',
        handlers.LoginHandler,
        name='login',
        strict_slash=True),
    RedirectRoute('/login-return',
        handlers.LoginReturnHandler,
        name='login-return',
        strict_slash=True),
##    RedirectRoute('/teacher-login',
##        handlers.TeacherLoginHandler,
##        name='teacher-login',
##        strict_slash=True),
    RedirectRoute('/logout',
        handlers.LogoutHandler,
        name='logout',
        strict_slash=True),

    RedirectRoute('/about',
        handlers.AboutHandler,
        name='about',
        strict_slash=True),
    RedirectRoute('/contact',
        handlers.ContactHandler,
        name='contact',
        strict_slash=True),
    RedirectRoute('/announcements',
        handlers.AnnouncementsHandler,
        name='announcements',
        strict_slash=True),
    RedirectRoute('/faqs',
        handlers.FAQsHandler,
        name='faqs',
        strict_slash=True),
    RedirectRoute('/resources',
        handlers.ResourcesHandler,
        name='resources',
        strict_slash=True),
    RedirectRoute('/news',
        handlers.NewsHandler,
        name='news',
        strict_slash=True),
    RedirectRoute('/privacy-policy',
        handlers.PrivacyHandler,
        name='privacy-policy',
        strict_slash=True),
    RedirectRoute('/rules',
        handlers.RulesHandler,
        name='rules',
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