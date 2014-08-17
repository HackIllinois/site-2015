from google.appengine.ext import ndb

class Event(ndb.Model):
    name = ndb.StringProperty(required=True)

    @classmethod
    def unique_properties(cls):
        return ['name']
