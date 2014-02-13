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
        if users.get_current_user() is None:
            self.redirect(self.uri_for('home'), abort=True)
        elif self.session.get('is_teacher') is None \
            or self.session.get('is_teacher') != True:
            self.redirect(self.uri_for('register'), abort=True)
        return handler(self, *args, **kwargs)
    return check_session


def student_required(handler):
    def check_session(self, *args, **kwargs):
        if self.session.get('is_student') is None \
            or self.session.get('is_student') != True:
            self.redirect(self.uri_for('home'), abort=True)
        return handler(self, *args, **kwargs)
    return check_session


def active_student_required(handler):
    def check_session(self, *args, **kwargs):
        if self.session.get('is_student') is None \
            or self.session.get('is_student') != True \
            or self.session.get('active') is None \
            or self.session.get('active') != True:
            self.redirect(self.uri_for('home'), abort=True)
        return handler(self, *args, **kwargs)
    return check_session


def user_required(handler):
    def check_session(self, *args, **kwargs):
        if users.get_current_user() is None:
            self.redirect(login_url, abort=True)
        return handler(self, *args, **kwargs)
    return check_session