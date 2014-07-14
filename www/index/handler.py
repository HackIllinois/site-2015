import www.main_handler
import logging
from db.Email import Email

class default(www.main_handler.handler):
    def get(self):
        self.render("index/default.html")
    def post(self):
        Email.add({"email":self.request.get("email")})
        self.render("index/thank_you.html")