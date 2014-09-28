import logging
from www.base.handlers import BaseAdminHandler

from db.Email import Email

from google.appengine.api import users

class AdminHandler(BaseAdminHandler):
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
