# -*- coding: utf-8 -*-
import logging

# related third party imports
import webapp2
from google.appengine.api import users # we are using this for authentication
from google.appengine.ext import ndb

# local application/library specific imports
import models # we are using this for authorization and storing of further pii
from basehandler import BaseHandler
from decorators import teacher_required, student_required, user_required


class MainHandler(BaseHandler):

    def get(self):
        params = {}

        # not to self: move this into a LoginHandler that's set as the dest_url
        # in the login_url, maybe with an additional continue_url

        if self.user is not None: # user has logged in with their google account
            # teacher or student?
            # students should be pre-registered by the teachers, so we should
            # have some information to go on, right?

            teacher = models.Teacher.query(
                models.Teacher.user_id == self.user_id).get()

            student = models.Student.query(
                models.Student.email == self.email).get()

            if student is not None:

                # make sure parental consent has been received AND confirmed
                if not student.parental_consent_received or \
                    not student.parental_consent_confirmed:
                    message = 'Sorry, but your parental consent has not yet been verified.'
                    self.add_message(message, 'danger')
                    return self.render_template('home.html', **params)

                self.session['is_student'] = True
                self.session['teacher_key'] = student.teacher.urlsafe()
                self.session['student_key'] = student.key.urlsafe()

                #activate the student if this is their first time logging in
                if student.user_id is None:
                    student.active = True
                    student.user_id = self.user_id
                    student.put()

                    message = 'Welcome Student!'
                    self.add_message(message, 'info')

                # maybe check if we have a user_id for the student, and active is False
                # indicating a later-removed student record

            elif teacher is None:
                # send them to the register screen to gather further information
                self.redirect_to('register')

            else:
                message = 'Welcome Teacher!'
                self.add_message(message, 'info')

                self.session['is_teacher'] = True
                self.session['teacher_key'] = teacher.key.urlsafe()

                # send them to their dashboard
                return self.redirect_to('dashboard')

        else:
            # kill the session, in case its still active from previous login
            # this should be taken care of by the LogoutHandler though
            self.session.clear()

        return self.render_template('home.html', **params)


class LoginHandler(BaseHandler):
    def get(self):
        #self.redirect(self.auth_config['login_url'])
        # if we do this, the dest_url will be /login, so you'll
        # be stuck in an infinite loop
        self.redirect(users.create_login_url('/'))# home page
        #self.redirect(users.create_login_url('/login-return'))# LoginReturnHandler


##class LoginReturnHandler(BaseHandler):
##    def get(self, continue_url='/'):
##        """ Determine if returning login is Teacher or Student
##
##        based on Gmail address found:
##            in Teacher:
##                TeacherLoginHandler
##            in Student:
##                StudentLoginHandler
##        not found:
##            TeacherLoginHandler
##        """
##        params = {}
##        params['continue_url'] = continue_url
##
##        if self.user is not None: # user has logged in with their google account
##            # teacher or student?
##            # students should be pre-registered by the teachers, so we should
##            # have some information to go on, right?
##
##            student = models.Student.query(
##                models.Student.email == self.email).get()
##
##            if student is not None:
##                params['student'] = student
##                #return self.redirect_to('student-login')
##
##            teacher = models.Teacher.query(
##            models.Teacher.user_id == self.user_id).get()
##
##            params['teacher'] = teacher
##            #self.redirect('teacher-login', **params)
##            #return self.teacher_login_handler(teacher)
##            #TeacherLoginHandler.check_teacher(teacher)
##
##        return self.redirect_to('home')# no user, go home
##
##    @classmethod
##    def teacher_login_handler(self, teacher):
##        pass


##class TeacherLoginHandler(object):
##    def __init__(self, teacher):
##        self.teacher = teacher
##
##    def check_teacher(self):
##        logging.info(self.teacher.user_id)


class LogoutHandler(BaseHandler):
    def get(self):
        # clear session variables
        self.session.clear()
        # redirect to google account logout
        self.redirect(self.auth_config['logout_url'])


class RegisterHandler(BaseHandler):

    @user_required
    def get(self):
        # note to self: turn these two checks into another decorator?
        # unregistered_teacher_required or similar?
        # if a student logs in, we don't want them to be able to access this page
        if self.session.get('is_student') == True:
            self.redirect('/', abort=True)

        # if a teacher is logged in, and we already have their pii,
        # i don't think we want them to be able to access this page
        if self.session.get('is_teacher') == True and \
            self.session.get('teacher_key') is not None:
            self.redirect('dashboard', abort=True)

        params = {}
        return self.render_template('register.html', **params)

    @user_required
    def post(self):
        # if a student logs in, we don't want them to be able to access this page
        if self.session.get('is_student') == True:
            self.redirect('/', abort=True)

        # if a teacher is logged in, and we already have their pii,
        # i don't think we want them to be able to access this page
        if self.session.get('is_teacher') == True and \
            self.session.get('teacher_key') is not None:
            self.redirect('dashboard', abort=True)

        first_name = self.request.POST.get('first_name').strip()
        last_name = self.request.POST.get('last_name').strip()
        phone_number = self.request.POST.get('phone_number').strip()
        role_number = self.request.POST.get('role_number').strip()
        subject = self.request.POST.get('subject')# they should be able to select multi
        agree_to_terms = self.request.POST.get('agree_to_terms')
        logging.info('agree_to_terms: %s' % agree_to_terms)
        logging.info('agree_to_terms: %s' % bool(agree_to_terms))

        # validate role number - format, in accepted list, not used already

        # first validate all the inputs
        ok_to_proceed = True

        required_fields, error_fields = [
            'first_name',
            'last_name',
            'phone_number',
            'role_number',
            'subject'], []

        for field in required_fields:
##            logging.info('self.request.get(%s) = %s' % (field,
##                self.request.get(field)))
            if (self.request.POST.get(field) == None or
                self.request.POST.get(field) == ''):
                ok_to_proceed = False
                error_fields.append(field)

        if not bool(agree_to_terms):
            ok_to_proceed = False
            error_fields.append('agree_to_terms')

        if ok_to_proceed:

            teacher = models.Teacher(
                user_id = self.user_id,
                first_name = first_name,
                last_name = last_name,
                email = self.email,
                phone_number = phone_number,
                role_number = role_number,
                subjects = (subject,),
                active = True,
            )

            teacher.put()
            self.session['teacher_key'] = teacher.key.urlsafe()
            self.session['is_teacher'] = True

        else:
            # pass form arguments back to self and re-render template
            # seems like there should be a better way, tho
            params = {}
            for field in self.request.arguments():
                params[field] = self.request.POST.get(field)
            params['error_fields'] = error_fields
            return self.render_template('register.html', **params)

        self.redirect_to('dashboard')


class RegisterStudentHandler(BaseHandler):
    """ Teachers register the Students

    the logged-in user (Teacher) can pre-register Students
    with their first and last names, GMAIL email address, subject and cycle
    (grade level)
    additionally, they can pre-check that they've received a parental consent
    form for this student
    forms are bundled and sent to RealNation for additional confirmation
    they will need a login to then check AGAIN that the student's parental
    consent has been confirmed, at which point the Student will receive an
    invitation email
    """

    @teacher_required
    def get(self):
        params = {}
        self.render_template('register-student.html', **params)

    @teacher_required
    def post(self):
        first_name = self.request.POST.get('first_name').strip()
        last_name = self.request.POST.get('last_name').strip()
        email = self.request.POST.get('email').lower()
        school_cycle = self.request.POST.get('school_cycle')
        subject = self.request.POST.get('subject')
        parental_consent_received = self.request.POST.get('parental_consent_received')

        # validate fields for content, format, correct values
        # first validate all the inputs
        ok_to_proceed = True

        required_fields, error_fields = [
            'first_name',
            'last_name',
            'email',
            'school_cycle',
            'subject'], []

        for field in required_fields:
##            logging.info('self.request.get(%s) = %s' % (field,
##                self.request.get(field)))
            if (self.request.POST.get(field) == None or
                self.request.POST.get(field) == ''):
                ok_to_proceed = False
                error_fields.append(field)

        if ok_to_proceed:

            # check for this email already in the system somewhere
            student = models.Student.query(models.Student.email == email).get()
            teacher = models.Teacher.query(models.Teacher.email == email).get()

            if student is None and teacher is None:

                student = models.Student(
                    teacher = ndb.Key(urlsafe=self.session['teacher_key']),
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    school_cycle = school_cycle,
                    subject = subject,
                    parental_consent_received = bool(parental_consent_received),
                )

                student.put()

                message = ('%s %s has been registered.' % (first_name, last_name))
                self.add_message(message, 'success')

            else:
                message = ('%s has already been registered.' % (email))
                self.add_message(message, 'danger')

        else:
            # pass form arguments back to self and re-render template
            # seems like there should be a better way, tho
            params = {}
            for field in self.request.arguments():
                params[field] = self.request.POST.get(field)
            params['error_fields'] = error_fields
            return self.render_template('register-student.html', **params)

        return self.redirect_to('dashboard')


class EditStudentHandler(BaseHandler):

    @teacher_required
    def get(self, student_id):
        params = {}
        student = models.Student.get_by_id(long(student_id))
        #logging.info(student)
        if student is not None:
            # if student has already been parentally consented, then we don't
            # want them to be editable
            if student.parental_consent_confirmed == True:
                message = 'The selected student has already been confirmed, \
                and is no longer editable.'
                self.add_message(message, 'info')
                return self.redirect_to('dashboard')
            params['student'] = student
            return self.render_template('edit-student.html', **params)
        return self.redirect_to('dashboard')

    @teacher_required
    def post(self, student_id):
        # should incorporate same validation here as when registering
        student = models.Student.get_by_id(long(student_id))
        if student is not None:
            first_name = self.request.POST.get('first_name').strip()
            last_name = self.request.POST.get('last_name').strip()
            email = self.request.POST.get('email').lower()
            school_cycle = self.request.POST.get('school_cycle').strip()
            subject = self.request.POST.get('subject').strip()
            parental_consent_received = self.request.POST.get('parental_consent_received')
            student.first_name = first_name
            student.last_name = last_name
            student.school_cycle = school_cycle
            student.subject = subject
            student.parental_consent_received = bool(parental_consent_received)
            student.put()
            message = ('Student updated successfully.')
            self.add_message(message, 'success')
        return self.redirect_to('dashboard')


class DashboardHandler(BaseHandler):

    @teacher_required
    def get(self):
        params = {}
        # get teachers students
        students = models.Student.query(models.Student.teacher ==
            ndb.Key(urlsafe=self.session['teacher_key']))
        params['students'] = students
        return self.render_template('dashboard.html', **params)


class StudentDashboardHandler(BaseHandler):

    @student_required
    def get(self):
        params = {}
        return self.render_template('student-dashboard.html', **params)


## STATIC TEMPLATE HANDLERS ##
class AboutHandler(BaseHandler):
    def get(self):
        params = {}
        return self.render_template('about.html', **params)


class ContactHandler(BaseHandler):
    def get(self):
        params = {}
        return self.render_template('contact.html', **params)


class EventsHandler(BaseHandler):
    def get(self):
        params = {}
        return self.render_template('events.html', **params)


class FAQsHandler(BaseHandler):
    def get(self):
        params = {}
        return self.render_template('faqs.html', **params)


class NewsHandler(BaseHandler):
    def get(self):
        params = {}
        return self.render_template('news.html', **params)


class PrivacyHandler(BaseHandler):
    def get(self):
        params = {}
        return self.render_template('privacy.html', **params)


class RulesHandler(BaseHandler):
    def get(self):
        params = {}
        return self.render_template('rules.html', **params)
