from google.appengine.ext import ndb
import logging

class Model(ndb.Model):
    @classmethod
    @ndb.transactional
    def add(cls, data):
        o = cls()

        for prop in data:
            setattr(o, prop, data[prop])

        ret = o.put()
		
        return o