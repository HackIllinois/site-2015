from www.base.BaseHandler import BaseHandler
import urllib, logging
from db.Email import Email

class MainHandler(BaseHandler):
    def get(self):
        self.render("index/default.html")
    def post(self):
		#TODO: verify email in db
        email = str(urllib.unquote(self.request.get('email')))
        if(Email.add({"email":email})):
            self.write("success");
        else:
            self.write("indatabase")
