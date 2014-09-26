from www.base.BaseHandler import BaseHandler
import urllib
from google.appengine.api import users

class LogoutHandler(BaseHandler):
    def get(self):
        self.redirect(users.create_logout_url("/"))
