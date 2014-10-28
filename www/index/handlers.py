from www.base.handlers import BaseHandler
import urllib, logging
from db.Email import Email
from db import constants
from third_party.sendgrid import SendGridClient
from third_party.sendgrid import Mail
import re

class IndexHandler(BaseHandler):
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
            sg = SendGridClient(constants.SENDGRID_API_USER, constants.SENDGRID_API_KEY, secure=True)
            message = Mail()
            message.set_subject(constants.SENDGRID_INFO_SUBJECT)
            message.set_html(constants.SENDGRID_INFO_HTML)
            message.set_from(constants.SENDGRID_INFO_FROM)
            message.add_category(constants.SENDGRID_INFO_CATEGORY)

            message.add_to(email)

            # use the Web API to send your message
            sg.send(message)
            if self.request.get('js'):
                self.write("success")
            else:
                self.render("index/default.html", invalid=False, success=True, indatabase=False, user_email=email)
        else:
            if self.request.get('js'):
                self.write("indatabase")
            else:
                self.render("index/default.html", invalid=False, success=False, indatabase=True, user_email=email)
