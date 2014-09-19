from www.base.BaseHandler import BaseHandler
import urllib, logging
from db.Email import Email
import re

class MainHandler(BaseHandler):
    def get(self):
        self.render("index/default.html", invalid=False, success=False, indatabase=False, user_email="")
    def post(self):
        email = str(urllib.unquote(self.request.get('email')))
		#TODO: render pages
        if not re.match(r"^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$", email):
            if self.request.get('js'):
                self.write("invalid")
            else:
                self.render("index/default.html", invalid=True, success=False, indatabase=False, user_email=email)
        elif(Email.add({"email":email})):
            if self.request.get('js'):
                self.write("success")
            else:
                self.render("index/default.html", invalid=False, success=True, indatabase=False, user_email=email)
        else:
            if self.request.get('js'):
                self.write("indatabase")
            else:
                self.render("index/default.html", invalid=False, success=False, indatabase=True, user_email=email)
 
class MainHandler2(BaseHandler):
    def get(self):
        self.render("index/default2.html", invalid=False, success=False, indatabase=False, user_email="")
    def post(self):
        email = str(urllib.unquote(self.request.get('email')))
        #TODO: render pages
        if not re.match(r"^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$", email):
            if self.request.get('js'):
                self.write("invalid")
            else:
                self.render("index/default2.html", invalid=True, success=False, indatabase=False, user_email=email)
        elif(Email.add({"email":email})):
            if self.request.get('js'):
                self.write("success")
            else:
                self.render("index/default2.html", invalid=False, success=True, indatabase=False, user_email=email)
        else:
            if self.request.get('js'):
                self.write("indatabase")
            else:
                self.render("index/default2.html", invalid=False, success=False, indatabase=True, user_email=email)
 
class MainHandler3(BaseHandler):
    def get(self):
        self.render("index/default3.html", invalid=False, success=False, indatabase=False, user_email="")
    def post(self):
        email = str(urllib.unquote(self.request.get('email')))
        #TODO: render pages
        if not re.match(r"^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$", email):
            if self.request.get('js'):
                self.write("invalid")
            else:
                self.render("index/default3.html", invalid=True, success=False, indatabase=False, user_email=email)
        elif(Email.add({"email":email})):
            if self.request.get('js'):
                self.write("success")
            else:
                self.render("index/default3.html", invalid=False, success=True, indatabase=False, user_email=email)
        else:
            if self.request.get('js'):
                self.write("indatabase")
            else:
                self.render("index/default3.html", invalid=False, success=False, indatabase=True, user_email=email)
 
 