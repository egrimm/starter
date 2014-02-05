# -*- coding: utf-8 -*-
import logging

# related third party imports
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

# local application/library specific imports
import models
from basehandler import BaseHandler


class MainHandler(BaseHandler):

    def get(self):
        params = {}
        if self.user is not None:
            person = models.Person.query(models.Person.user_id == self.user_id).get()
            if person is None:
                self.redirect_to('register')
        return self.render_template('home.html', **params)


class RegisterHandler(BaseHandler):
    def get(self):
        params = {}
        return self.render_template('register.html', **params)
