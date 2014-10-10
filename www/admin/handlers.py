import logging
from www.base.handlers import BaseAdminHandler
from www.base.handlers import MemcacheHandler

from db.Email import Email

from google.appengine.api import users
from google.appengine.ext import ndb

class AdminHandler(BaseAdminHandler, MemcacheHandler):
    """Homepage for the admin section."""

    def get(self):
        data = {}
        data['logout_url'] = users.create_logout_url('/')
        data['email'] = self.get_memcache('email')
        data['email_count'] = len(data['email'])
        self.render("admin/default.html", data=data)
