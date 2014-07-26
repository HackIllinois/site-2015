from www.base.BaseHandler import BaseHandler
from db.Email import Email

class MainHandler(BaseHandler):
    def get(self):
        self.render("index/default.html")
    def post(self):
        Email.add({"email":self.request.get("email")})
        self.render("index/thank_you.html")
		