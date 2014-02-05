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
            # teacher or student?
            teacher = models.Teacher.query(models.Teacher.user_id == self.user_id).get()
            if teacher is None:
                self.redirect_to('register')
        else:
            # kill the session
            self.session.clear()
        #self.session['foo'] = 'snausages'
        return self.render_template('home.html', **params)


class RegisterHandler(BaseHandler):
    def get(self):
        if self.user is None:
            self.redirect_to('home')
        params = {}
        return self.render_template('register.html', **params)

    def post(self):
        if self.user is None:
            self.redirect_to('home')
        role_number = self.request.POST.get('role_number')
        subject = self.request.POST.get('subject')
        agree_to_terms = self.request.POST.get('agree_to_terms')

        person = models.Teacher(
            user_id = self.user_id,
            email = self.email,
            role_number = role_number,
            subjects = (subject,)
        )

        person.put()

        self.redirect_to('dashboard')


class DashboardHandler(BaseHandler):
    def get(self):
        params = {}
        return self.render_template('dashboard.html', **params)
