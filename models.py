from google.appengine.ext import ndb

class Person(ndb.Model):
    user_id = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    active = ndb.BooleanProperty(default=False)


class Teacher(Person):
    phone_number = ndb.StringProperty()
    role_number = ndb.StringProperty()
    subjects = ndb.StringProperty(repeated=True)


class Student(Person):
    teacher = ndb.KeyProperty(kind=Teacher)
    subject = ndb.StringProperty()
    school_cycle = ndb.StringProperty()
    parental_consent_received = ndb.BooleanProperty(default=False)
    parental_consent_confirmed = ndb.BooleanProperty(default=False)
    invitation_email_sent = ndb.BooleanProperty(default=False)
    invitation_email_sent_date = ndb.DateTimeProperty(default=None)
    competition_email_sent = ndb.BooleanProperty(default=False)
    competition_email_sent_date = ndb.DateTimeProperty(default=None)

    @classmethod
    def get_by_email(cls, email):
        """Returns a student object based on an email.

        :param email:
            String representing the student email. Examples:

        :returns:
            A student object.
        """
        return cls.query(cls.email == email).get()

    @classmethod
    def get_all(cls):
        """ get all students """
        return cls.query()

    @classmethod
    def get_consent_pending(cls):
        """ get students who havent returned parental consent """
        return cls.query(cls.parental_consent_received == False)

    @classmethod
    def get_consent_received(cls):
        """ get students who have return parental consent
        but havent been confirmed """
        return cls.query(
            ndb.AND(
                cls.parental_consent_received == True,
                cls.parental_consent_confirmed == False
            )
        )

    @classmethod
    def get_consent_confirmed(cls):
        """ get students with confirmed parental consent """
        return cls.query(
            ndb.AND(
                cls.parental_consent_received == True,
                cls.parental_consent_confirmed == True
            )
        )

    @classmethod
    def get_invite_email_pending(cls):
        """ get students with confirmed parental consent
        who havent received their invite email """
        students = cls.get_consent_confirmed().filter(
            cls.invitation_email_sent == False)
        return students


