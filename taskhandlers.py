#-------------------------------------------------------------------------------
# Name:        taskhandler
# Purpose:     handlers for tasks
#
# Author:      Eric
#
# Created:     13/02/2014
# Copyright:   (c) Eric 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import webapp2
from google.appengine.api import taskqueue
from google.appengine.ext import ndb
import models
from basehandler import BaseHandler

class InviteStudentHandler(BaseHandler):

    def get(self):
        pass

    def post(self):
        pass


class AddInviteStudentTask(BaseHandler):

    def get(self):
        # render a template with a button that posts back here
        params = {}
        self.render_template('add-invite-task.html', **params)

    def post(self):
        # add the task to the queue
        # do i need to worry about the task already being in the queue? (yes!)
        try:
            #https://developers.google.com/appengine/docs/python/taskqueue/functions#add
            taskqueue.add(queue_name='invite-email',
                name='send-student-invite-email',
                url='/tasks/invite-student',
                method='POST')
            message = 'Task added successfully.'
            self.add_message(message, 'success')

        except taskqueue.TombstonedTaskError, e:
            message = 'oops!'
            self.add_message(message, 'danger')

        except taskqueue.TaskAlreadyExistsError, e:
            message = 'Task already exists.'
            self.add_message(message, 'danger')

        return self.get()
