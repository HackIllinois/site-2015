from www.base.BaseHandler import BaseHandler
import urllib, logging
from db.Email import Email
import re

class MainHandler(BaseHandler):
    def get(self):
        self.render("index/default.html")
    def post(self):
        email = str(urllib.unquote(self.request.get('email')))
		#TODO: render pages
        if not re.match(r"^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$", email):
            self.write("invalid")
        elif(Email.add({"email":email})):
            self.write("success")
        else:
            self.write("indatabase")
