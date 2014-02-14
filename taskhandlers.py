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
#from google.appengine.api import taskqueue
from google.appengine.ext import ndb
import models
from basehandler import BaseHandler
from google.appengine.api import mail
import datetime

class InviteStudentHandler(BaseHandler):

    def get(self):
        """ send invite email to confirmed students

        validate header? should contain X-AppEngine-Cron: true

        get students with parental consent received and confirmed
        check that they haven't been sent the invite email
        send the invite email
        update their datastore record
        ???
        profit!
        """
        self.response.headers['Content-Type'] = 'text/plain'

        # note: we may end up customizing this for each student
        # we should probably also implement some email templating
        sender_address = 'Call to Code Support <EricGrimm500@gmail.com>'
        subject = 'Welcome to Call to Code!'
        body = """
Thank you for your interest in Call to Code!
Your parental consent has been confirmed, and you are ready to activate your account!
Please login at the link below:

http://www.calltocode.ie/

Thank you and good luck in the competition!

The Call to Code Support Team
"""

        students = models.Student.get_invite_email_pending()
        self.response.write('emails to send: %s\n' % students.count())

        for student in students:

            mail.send_mail(sender_address, student.email, subject, body)
            student.invitation_email_sent = True
            student.invitation_email_sent_date = datetime.datetime.now()
            student.put()

            self.response.write('Invitation email sent to %s.\n' % student.email)
            #self.response.write(body)


# note to self: this will probably go away, cause i'll use
# cron jobs (scheduled tasks) rather than queues
##class AddInviteStudentTask(BaseHandler):
##
##    def get(self):
##        # render a template with a button that posts back here
##        params = {}
##        self.render_template('add-invite-task.html', **params)
##
##    def post(self):
##        # add the task to the queue
##        # do i need to worry about the task already being in the queue? (yes!)
##        try:
##            #https://developers.google.com/appengine/docs/python/taskqueue/functions#add
##            taskqueue.add(queue_name='invite-email',
##                name='send-student-invite-email',
##                url='/tasks/invite-student',
##                method='POST')
##            message = 'Task added successfully.'
##            self.add_message(message, 'success')
##
##        except taskqueue.TombstonedTaskError, e:
##            message = 'oops!'
##            self.add_message(message, 'danger')
##
##        except taskqueue.TaskAlreadyExistsError, e:
##            message = 'Task already exists.'
##            self.add_message(message, 'danger')
##
##        return self.get()
