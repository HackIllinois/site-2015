import logging
from www.base.BaseHandler import BaseHandler

from google.appengine.api import users

from db.Email import Email

from db import constants


class AdminHandler(BaseHandler):
    """Homepage for the admin section."""

    def get(self):
        data = {}
        data['logout_url'] = users.create_logout_url('/')
        #query = Email.query()
        #data['email'] = []
        #logging.error(query)
        #for obj in query:
        #    data['email'].append(obj)
        self.render("admin/default.html", data=data)

    def dispatch(self):
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