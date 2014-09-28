import os
import jinja2
import webapp2

import logging
from google.appengine.ext import ereporter

from google.appengine.api import users

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

class LogoutHandler(BaseHandler):
    """Delet after login system switch"""
    def get(self):
        self.redirect(users.create_logout_url("/"))