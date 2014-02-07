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
