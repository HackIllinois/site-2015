import os
import jinja2
import webapp2
import pickle

from db.Email import Email

import logging
from google.appengine.ext import ereporter

from google.appengine.api import users

from google.appengine.api import memcache

from db import constants

template_dir = os.path.join(os.path.dirname(__file__), os.pardir)
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)
jinja_env.filters.update({'is_list':lambda l: isinstance(l, list)})

#https://developers.google.com/appengine/articles/python/recording_exceptions_with_ereporter
ereporter.register_logger()


class BaseHandler(webapp2.RequestHandler):
    """ This is the Base Handler
        This is the parent of every other handler
        Most other handlers use functions defined in this hander
        This handler is the child of webapp2.RequestHandler which is pre-defined by webapp2"""

    def __init__(self, request, response):
        super(BaseHandler, self).__init__(request, response)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        page = t.render(params)

        return page

class BaseAdminHandler(BaseHandler):
    """
    This is for all /admin pages
    Overrides the dispatch method (called before get/post/etc.)
    Sends 401 (Unauthorized) if user is not an admin
    Ref: http://webapp-improved.appspot.com/guide/handlers.html
    """

    def __init__(self, request, response):
        super(BaseAdminHandler, self).__init__(request, response)

    def dispatch(self):
        """TODO: Change to new login system"""
        is_admin = False

        user = users.get_current_user()
        if not user:
            return self.abort(401)

        email = user.email()

        domain = email.split('@')[1] if len(email.split('@')) == 2 else None  # Sanity check

        if domain == 'hackillinois.org' or email in constants.TESTER_EMAILS:
            # Parent class will call the method to be dispatched
            # -- get() or post() or etc.
            logging.info('Admin user %s is online.', email)
            super(BaseHandler, self).dispatch()
        else:
            logging.info('%s attempted to access an admin page but was denied.', email)
            return self.abort(401)

class MemcacheHandler:
    """
    TODO: Stress Test Memcache with high volume and large strings
    """

    """http://stackoverflow.com/questions/7111068/split-string-by-count-of-characters"""
    def chunks(self, s, n):
        """Produce `n`-character chunks from `s`."""
        for start in range(0, len(s), n):
            yield s[start:start+n]

    """http://stackoverflow.com/questions/9127982/avoiding-memcache-1m-limit-of-values"""
    def store(self, key, value, chunksize=950000):
        serialized = pickle.dumps(value)
        values = {}
        i = 0
        data_chunks = self.chunks(serialized, chunksize)

        #sets groups of chucks each at most 32 MB
        for chunk in data_chunks:
            values['%s.%s' % (key, i)] = chunk
            i += 1
            if i % 32 == 0:
                memcache.set_multi(values, time=10800)
                values = {}
        if i % 32:
            memcache.set_multi(values, time=10800)
        #sets count of chunks
        memcache.set(key, i)

    """http://stackoverflow.com/questions/9127982/avoiding-memcache-1m-limit-of-values"""
    def retrieve(self, key):
        #gets count of chunks
        #returns None if it can't get count, or count is 0 (no chunks set)
        count = memcache.get(key)

        if count == 0 or count == None:
            return None

        #gets groups of chucks each at most 32 MB and concatinates the chunks
        #returns None if it can't get a chunk
        keys = []
        serialized = ''
        for i in range(count):
            keys.append('%s.%s' % (key, i))
            i += 1
            if i % 32 == 0:
                result = memcache.get_multi(keys)
                for x in range(32):
                    k = '%s.%s' % (key, i+x-32)
                    if k not in result or not result[k]:
                        #Memcache string is invalid
                        return None
                    serialized += result[k]
                keys = []
        if i % 32:
            result = memcache.get_multi(keys)
            for x in range(i%32):
                k = '%s.%s' % (key, i/32*32+x)
                if k not in result or not result[k]:
                    #Memcache string is invalid
                    return None
                serialized += result[k]
        data = None
        if serialized:
            data = pickle.loads(serialized)
        return data

    def set_email_memcache(self):
        data = {}
        emails = Email.search_database()
        for email in emails:
            data[email.email] = {
                'email': email.email}

        self.store('email', data)
        return data

    def get_email_memcache(self):
        data = self.retrieve('email')
        if data is None:
            logging.info('setting memcache')
            data = self.set_email_memcache()
        return data


class LogoutHandler(BaseHandler):
    """Delet after login system switch"""
    def get(self):
        self.redirect(users.create_logout_url("/"))