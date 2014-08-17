from google.appengine.ext import ndb
from Model import Model

class Email(Model):
    Model._automatically_add_event_as_ancestor()
	
    email = ndb.StringProperty(required=True)
	
    @classmethod
    def unique_properties(cls):
        return ['email']
