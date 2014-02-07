#-------------------------------------------------------------------------------
# Name:        decorators
# Purpose:
#
# Author:      egrimm
#
# Created:     17/01/2014
# Copyright:   (c) egrimm 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import logging
from google.appengine.api import users
from config import config
from basehandler import BaseHandler


def teacher_required(handler):
    def check_session(self, *args, **kwargs):
        if self.session.get('is_teacher') is None \
            or self.session.get('is_teacher') != True:
            self.redirect(self.uri_for('home'), abort=True)
        return handler(self, *args, **kwargs)
    return check_session


def student_required(handler):
    def check_session(self, *args, **kwargs):
        if self.session.get('is_student') is None \
            or self.session.get('is_student') != True:
            self.redirect(self.uri_for('home'), abort=True)
        return handler(self, *args, **kwargs)
    return check_session


def user_required(handler):
    def check_session(self, *args, **kwargs):
        if users.get_current_user() is None:
            self.redirect(login_url, abort=True)
        return handler(self, *args, **kwargs)
    return check_session


##def user_required(handler):
##    """
##        Decorator for checking if there's a user associated
##        with the current session
##        Will also fail if there's no session present
##    """
##
##    def check_login(self, *args, **kwargs):
##        """
##            If handler has no login_url specified, invoke a 403 error
##        """
##        if self.request.query_string != '':
##            query_string = '?' + self.request.query_string
##        else:
##            query_string = ''
##
##        continue_url = self.request.path_url + query_string
##        login_url = self.uri_for('login', **{'continue': continue_url})
##
##        try:
##            auth = self.auth.get_user_by_session()
##            if not auth:
##                try:
##                    self.redirect(login_url, abort=True)
##                except (AttributeError, KeyError), e:
##                    self.abort(403)
##        except AttributeError, e:
##            # avoid AttributeError when the session was deleted from the server
##            logging.error(e)
##            self.auth.unset_session()
##            self.redirect(login_url)
##
##        return handler(self, *args, **kwargs)
##
##    return check_login