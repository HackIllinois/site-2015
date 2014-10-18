import urllib, logging
from www.base.handlers import BaseAdminHandler

from db.Email import Email
from db import constants

from third_party.sendgrid import SendGridClient
from third_party.sendgrid import Mail

from google.appengine.api import users

class EmailHandler(BaseAdminHandler):
    """Test Email for the admin section."""

    def get(self):
        self.render("admin/test_email/default.html")
    def post(self):
        email = str(urllib.unquote(self.request.get('email')))
        # make a secure connection to SendGrid
        sg = SendGridClient(constants.SENDGRID_API_USER, constants.SENDGRID_API_KEY, secure=True)

        message = Mail()
        message.set_subject('message subject')
        message.set_html('This is just a test')
        message.set_text('This is just a test')
        message.set_from('ben@hackillinois.org')
        message.add_category('sendback')
        # add a recipient
        message.add_to(email)

        # use the Web API to send your message
        sg.send(message)

