from google.appengine.ext import ndb
from Model import Model

class Email(Model):
    email = ndb.StringProperty(required=True)